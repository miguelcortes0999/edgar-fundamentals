"""
constants.py
Stores reusable constants such as API endpoints and headers.
"""

SEC_TICKERS_URL = 'https://www.sec.gov/files/company_tickers.json'
SEC_SUBMISSIONS_URL = 'https://data.sec.gov/submissions/CIK{}.json'
SEC_FACTS_URL = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'
USER_AGENT_TEMPLATE = 'User-Agent'