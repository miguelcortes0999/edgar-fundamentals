"""
pysec.py
Main class that integrates SEC API client with financial calculations.
"""

import pandas as pd
from .edgar_fundamentals.utils.sec_api import SECClient

class PySEC:
    """Handles SEC data retrieval and financial metric computations."""

    def __init__(self, user_email: str):
        """
        Initializes the PySEC class with SEC API client.

        Args:
            user_email (str): User email for SEC API requests.
        """
        self.client = SECClient(user_email)

    def compute_shares_metrics(self, ticker: str) -> pd.DataFrame:
        """
        Computes the circulation percentage of shares.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing calculated share metrics.
        """
        facts = self.client.get_company_facts(ticker)

        shares_outstanding = pd.DataFrame(facts["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"])
        public_float = pd.DataFrame(facts["dei"]["EntityPublicFloat"]["units"]["USD"])

        df = pd.merge(public_float, shares_outstanding, how="outer", on="end")[["end", "val_x", "val_y"]]
        df["end"] = pd.to_datetime(df["end"])
        df["year_month"] = df["end"].dt.to_period("M")

        df_last = df.sort_values("end").groupby("year_month").tail(1)
        df_last = df_last.set_index("end").resample("M").last().fillna(method="ffill").reset_index()

        df_grouped = df_last.groupby(df_last["end"].dt.to_period("M")).agg({"val_x": "max", "val_y": "max"}).reset_index()
        df_grouped = df_grouped.rename(columns={"val_y": "shares_circulation", "val_x": "shares_total"})
        df_grouped.sort_values("end", inplace=True)
        df_grouped["percent_circulation"] = df_grouped["shares_circulation"] / df_grouped["shares_total"]

        return df_grouped

    def get_company_filings(self, ticker: str) -> pd.DataFrame:
        """
        Retrieves SEC filings for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: DataFrame containing recent SEC filings.
        """
        return self.client.get_company_filings(ticker)