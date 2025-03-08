"""
sec_api.py
Handles API requests to SEC endpoints.
"""

import requests
import pandas as pd
from utils.constants import SEC_TICKERS_URL, SEC_SUBMISSIONS_URL, SEC_FACTS_URL, USER_AGENT_TEMPLATE

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
        return tickers[["cik_str", "title"]]

    def get_company_metadata(self, ticker: str) -> dict:
        """
        Fetches metadata for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            dict: Metadata of the company.
        """
        cik_str = self.df_company_tickers.loc[ticker.upper(), "cik_str"]
        response = self._get_requests_json(SEC_SUBMISSIONS_URL.format(cik_str))
        return response

    def get_company_facts(self, ticker: str) -> dict:
        """
        Fetches structured financial data for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            dict: Structured financial data (XBRL facts).
        """
        cik_str = self.df_company_tickers.loc[ticker.upper(), "cik_str"]
        response = self._get_requests_json(SEC_FACTS_URL.format(cik_str))
        return response.get("facts", {})

    def get_company_filings(self, ticker: str) -> pd.DataFrame:
        """
        Retrieves SEC filings for a given company.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: DataFrame containing recent filings.
        """
        metadata = self.get_company_metadata(ticker)
        return pd.DataFrame(metadata["filings"]["recent"])