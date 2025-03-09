"""
pysec.py
Main class that integrates SEC API client with financial calculations.
"""

import pandas as pd
from edgar_fundamentals.utils.sec_api import SECClient

class PySEC(SECClient):
    """Handles SEC data retrieval and financial metric computations."""

    def __init__(self, user_email: str):
        """
        Initializes the PySEC class with SEC API client.

        Args:
            user_email (str): User email for SEC API requests.
        """
        super().__init__(user_email)  # Llamar al constructor de la clase padre

    def get_company_filings(self, ticker: str) -> pd.DataFrame:
        """
        Retrieves SEC filings for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: DataFrame containing recent filings.
        """
        if hasattr(self, "ticker_company_cache") and ticker.upper() == self.ticker_company_cache:
            df_fillings = pd.DataFrame(self.ticker_company_metadata_cache["filings"]["recent"])
        else:
            df_fillings = pd.DataFrame(self.get_company_metadata(ticker)["filings"]["recent"])
        return df_fillings

    def get_company_shares(self, ticker: str) -> pd.DataFrame:
        """
        Computes the circulation percentage of shares, including report details.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing calculated share metrics.
        """
        if hasattr(self, "ticker_fact_cache") and ticker.upper() == self.ticker_fact_cache:
            facts = self.ticker_company_fact_cache
        else:
            facts = self.get_company_facts(ticker.upper())
        # Retrieve shares outstanding and public float data with error handling
        shares_outstanding = pd.DataFrame(facts["dei"].get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", []))
        public_float = pd.DataFrame(facts["dei"].get("EntityPublicFloat", {}).get("units", {}).get("USD", []))
        # Check if there is sufficient data before proceeding
        if shares_outstanding.empty and public_float.empty:
            raise ValueError(f"Insufficient financial data available for {ticker}")
        # Merge data and keep relevant columns
        df = pd.merge(public_float, shares_outstanding, how="outer", on=["end"], suffixes=("_public", "_shares"))
        df["date"] = pd.to_datetime(df["end"])
        df["filed_shares"] = pd.to_datetime(df["filed_shares"], errors='coerce')
        df["year_month"] = df["date"].dt.to_period("M")
        df["filed_year_month"] = df["filed_shares"].dt.to_period("M")
        df_last = df.sort_values("date").groupby("year_month").tail(1)
        df_last = df_last.set_index("date").resample("M").last().ffill().reset_index()
        df_grouped = df_last.groupby(df_last["date"].dt.to_period("M")).agg({
            'form_shares': 'first',
            'fp_shares': 'first',
            'frame_shares': 'first',
            'accn_shares': 'first',
            'filed_shares': 'first',
            'val_public': 'max', 
            'val_shares': 'max'
        }).sort_values("date", inplace=False).reset_index(inplace=False)
        df_grouped = df_grouped[df_grouped["date"] == df_grouped["filed_shares"].dt.to_period("M")]
        df_grouped = df_grouped.rename(columns={
            'val_shares': 'shares_circulation', 
            'val_public': 'shares_total'
        })
        df_grouped["percent_circulation"] = df_grouped["shares_circulation"] / df_grouped["shares_total"]
        return df_grouped

    def get_financial_statements(self, ticker: str, report_type: str = "K") -> pd.DataFrame:
        """
        Retrieves key financial statements from SEC filings.

        Args:
            ticker (str): The stock ticker symbol.
            report_type (str, optional): "K" for annual reports (10-K) or "Q" for quarterly reports (10-Q). Defaults to "K".

        Returns:
            pd.DataFrame: A DataFrame containing key financial data, including balance sheet and income statement metrics.
        """
        # Check if the data is already cached
        if hasattr(self, "ticker_fact_cache") and ticker.upper() == self.ticker_fact_cache:
            facts = self.ticker_company_fact_cache
        else:
            facts = self.get_company_facts(ticker.upper())
        # Check fiscal end year
        if report_type=='K':
            fiscal_month = 'fiscalYearEnd'[0:2]
        # Define key financial metrics
        financial_keys = {
            # Balance sheet
            'Assets': 'Assets',
            'AssetsCurrent': 'AssetsCurrent',
            'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents': 'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents',
            'CashAndCashEquivalentsAtCarryingValue': 'CashAndCashEquivalentsAtCarryingValue',
            'AccountsReceivableNetCurrent': 'AccountsReceivableNetCurrent',
            'InventoryNet': 'InventoryNet',
            'AssetsNoncurrent': 'AssetsNoncurrent',
            'Liabilities': 'Liabilities',
            'LiabilitiesCurrent': 'LiabilitiesCurrent',
            'DebtCurrent': 'DebtCurrent',
            'LiabilitiesNoncurrent': 'LiabilitiesNoncurrent',
            'LongTermDebtNoncurrent': 'LongTermDebtNoncurrent',
            'StockholdersEquity': 'StockholdersEquity',
            'AccountsPayableAndAccruedLiabilitiesCurrent': 'AccountsPayableAndAccruedLiabilitiesCurrent',
            # Income statment
            'RevenueFromContractWithCustomerExcludingAssessedTax': 'SalesNet',
            'OperatingIncomeLoss': 'OperatingIncomeLoss',
            'ShortTermInvestments':'ShortTermInvestments',
            'InterestExpense': 'InterestExpense',
            'IncomeTaxExpenseBenefit': 'IncomeTaxExpenseBenefit',
            # Cashflow
            'DepreciationAndAmortization':'DepreciationAndAmortization',
            'Goodwill': 'Goodwill',
        }
        financial_keys = dict(zip(self.get_company_facts(ticker)['us-gaap'].keys(), 
                             self.get_company_facts(ticker)['us-gaap'].keys()))
        # Extract data for each financial metric
        df_financials = pd.DataFrame()
        for key, sec_key in financial_keys.items():
            df = pd.DataFrame(facts["us-gaap"].get(sec_key, {}).get("units", {}).get("USD", []))
            df["metric"] = key
            df_financials = pd.concat([df_financials, df], ignore_index=True)
        # Convert 'end' to a period-based date format (Monthly)
        df_financials["date"] = pd.to_datetime(df_financials["end"]).dt.to_period("M")
        # Select the most recent filing for each metric and reporting period
        df_financials = (
            df_financials.sort_values(["metric", "end", "filed"], ascending=[True, True, False])
            .groupby(["metric", "date"])
            .first()
            .reset_index(inplace=False)
        )
        # Filter reports based on the selected type (Annual 10-K or Quarterly 10-Q)
        if report_type == 'K':
            if hasattr(self, "ticker_company_cache") and ticker.upper() == self.ticker_company_cache:
                fiscal_month = self.ticker_company_metadata_cache['fiscalYearEnd'][0:2]
            else:
                fiscal_month = self.get_company_metadata(ticker)['fiscalYearEnd'][0:2]
            df_financials = df_financials[df_financials["date"].dt.month == int(fiscal_month)]
        elif report_type == 'Q':
            df_financials = df_financials[df_financials["form"].str.contains(report_type, na=False)]
        else:
            raise ValueError(f'El valor {report_type} no es válido, solo "K" o "Q"')
        return df_financials