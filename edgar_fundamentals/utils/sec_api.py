"""
sec_api.py
Handles API requests to SEC endpoints.
"""

import requests
import pandas as pd
from edgar_fundamentals.utils.constants import SEC_TICKERS_URL, SEC_SUBMISSIONS_URL, SEC_FACTS_URL, USER_AGENT_TEMPLATE

class SECClient:
    """Handles SEC API requests and company metadata retrieval."""

    def __init__(self, user_email: str):
        """
        Initializes the SECClient with user headers and retrieves company tickers.

        Args:
            user_email (str): Email to be used in request headers.
        """
        self.headers = {USER_AGENT_TEMPLATE: user_email}
        self.df_company_tickers = self._fetch_company_tickers()

    def _get_requests_json(self, url) -> dict:
        response = requests.get(url, headers=self.headers).json()
        return response

    def _fetch_company_tickers(self) -> pd.DataFrame:
        """Fetches and processes company tickers from SEC."""
        response = self._get_requests_json(SEC_TICKERS_URL)
        tickers = pd.DataFrame.from_dict(response, orient="index")
        tickers["cik_str"] = tickers["cik_str"].astype(str).str.zfill(10)
        tickers["title"] = tickers["title"].str.upper()
        tickers.index = tickers["ticker"].str.upper()
        tickers.drop('ticker', axis=1, inplace=True)
        return tickers

    def get_company_metadata(self, ticker: str) -> dict:
        """
        Fetches metadata for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
        dict: A dictionary containing the following keys and their descriptions:

            - cik (str): The Central Index Key (CIK) uniquely identifying the company. Example: '84112'.
            - entityType (str): The type of entity the company represents, such as its operational structure. Example: 'operating'.
            - sic (str): The Standard Industry Classification (SIC) code representing the companys primary business activity. Example: '3669'.
            - sicDescription (str): A textual description of the SIC code, detailing the companys industry sector. Example: 'Communications Equipment, NEC'.
            - insiderTransactionForOwnerExists (int): Indicates whether there are insider transactions involving the companys owners. Possible values: '0' (No transactions), '1' (Transactions exist). Example: '0'.
            - insiderTransactionForIssuerExists (int): Indicates whether there are insider transactions involving the issuer (the company itself). Possible values: '0' (No transactions), '1' (Transactions exist). Example: '1'.
            - name (str): The full corporate name of the company. Example: 'GEORGE RISK INDUSTRIES, INC.'.
            - tickers (str): The stock ticker symbol(s) used to identify the company in stock markets. Example: 'RSKIA'.
            - exchanges (str): The stock exchange(s) where the companys securities are traded. Example: 'OTC' (Over-the-Counter).
            - ein (str): Employer Identification Number (EIN) assigned to the company for tax purposes. Example: '840524756'.
            - description (str): A brief description of the company, which might be empty if not provided. Example: ''.
            - website (str): The companys primary website URL. Example: ''.
            - investorWebsite (str): The URL of the companys investor relations website, if available. Example: ''.
            - category (str): Category related to the companys SEC filings, such as its reporting status or size. Example: 'Non-accelerated filer<br>Smaller reporting company'.
            - fiscalYearEnd (str): The end date of the companys fiscal year in MMDD format. Example: '0430' (April 30).
            - stateOfIncorporation (str): The state where the company is incorporated. Example: 'CO' (Colorado).
            - stateOfIncorporationDescription (str): A description of the state where the company is incorporated. Example: 'CO' (Colorado).
            - addresses (dict): Mailing and business addresses of the company. Example: <{'mailing': 'address', 'business': 'address'}>.
            - phone (str): Contact phone number for the company. Example: '3082354645'.
            - flags (str): Flags or markers related to the companys filing or status. This might be empty if no flags are set. Example: ''.
            - formerNames (dict): Previous names of the company before its current name. Example: <{'lastName': 'RISK GEORGE INDUSTRIES INC'}>.
            - filings (str): Names of the reports or filings associated with the company. Example: 'files'.
        """
        cik_str = self.df_company_tickers.loc[ticker.upper(), "cik_str"]
        self.ticker_company_metadata_cache, self.ticker_company_cache = self._get_requests_json(SEC_SUBMISSIONS_URL.format(cik_str)), ticker.upper() 
        return self.ticker_company_metadata_cache

    def get_company_facts(self, ticker: str) -> dict:
        """
        Fetches structured financial data for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            dict: Structured financial data (XBRL facts).
        """
        cik_str = self.df_company_tickers.loc[ticker.upper(), "cik_str"]
        self.ticker_company_fact_cache, self.ticker_fact_cache = self._get_requests_json(SEC_FACTS_URL.format(cik_str)).get("facts", {}), ticker.upper()
        return self.ticker_company_fact_cache