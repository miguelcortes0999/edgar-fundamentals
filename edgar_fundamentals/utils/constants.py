"""
constants.py
Stores reusable constants such as API endpoints and headers.
"""

SEC_TICKERS_URL = 'https://www.sec.gov/files/company_tickers.json'
SEC_SUBMISSIONS_URL = 'https://data.sec.gov/submissions/CIK{}.json'
SEC_FACTS_URL = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'
USER_AGENT_TEMPLATE = 'User-Agent'
SEC_KEYS_FINANCIAL_STATEMENTS = [
    # Balance sheet
    'CashAndCashEquivalentsAtCarryingValue',
    'InventoryGross',
    'InventoryRawMaterials',
    'InventoryWorkInProcess',
    'InventoryFinishedGoods',
    'InventoryValuationReserves',
    'InventoryWriteDown',
    'InventoryAdjustments',
    'InventoryNet',
    'AccountsReceivableNetCurrent',
    'ContractWithCustomerAssetNetCurrent',
    'AssetsCurrent',
    'ContractWithCustomerAssetNetNoncurrent',
    'PropertyPlantAndEquipmentTransfersAndChanges',
    'PropertyPlantAndEquipmentDisposals',
    'PropertyPlantAndEquipmentAdditions',
    'PropertyPlantAndEquipmentGrossPeriodIncreaseDecrease',
    'PropertyPlantAndEquipmentGross',
    'PropertyPlantAndEquipmentNet',
    'Goodwill',
    'AssetsNoncurrent',
    'Assets',
    'DebtCurrent',
    'AccountsPayableAndAccruedLiabilitiesCurrent',
    'LiabilitiesCurrent',
    'LongTermDebtNoncurrent',
    'LiabilitiesNoncurrent',
    'Liabilities',
    'StockholdersEquity',
    'LiabilitiesAndStockholdersEquity',
    # Income statment
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'OperatingIncomeLoss',
    'ShortTermInvestments',
    'InterestExpense',
    'IncomeTaxExpenseBenefit',
    # Cashflow
    'DepreciationAndAmortization',
    'Goodwill',
]
BALANCE_SHEET = {
            'CashAndCashEquivalentsAtCarryingValue': 'Cash And Cash Equivalents At Carrying Value\t\t',
                'InventoryGross': 'Inventory Gross\t\t\t',
                    'InventoryRawMaterials': 'Inventory Raw Materials\t\t\t\t',
                    'InventoryWorkInProcess': 'Inventory Work In Process\t\t\t\t',
                    'InventoryFinishedGoods': 'Inventory Finished Goods\t\t\t\t',
                'InventoryValuationReserves': 'Inventory Valuation Reserves\t\t\t',
                'InventoryWriteDown': 'Inventory Write Down\t\t\t',
                'InventoryAdjustments': 'Inventory Adjustments\t\t\t',
            'InventoryNet': 'Inventory Net\t\t',
                'AccountsReceivableNetCurrent': 'Accounts Receivable Net Current\t\t\t',
            'ContractWithCustomerAssetNetCurrent': 'Contract With Customer Asset Net Current\t\t',
        'AssetsCurrent': 'Assets Current\t',
            'ContractWithCustomerAssetNetNoncurrent': 'Contract With Customer Asset Net Non Current\t\t',
                'PropertyPlantAndEquipmentTransfersAndChanges': 'Property Plant And Equipment Transfers And Changes\t\t\t',
                    'PropertyPlantAndEquipmentDisposals': 'Property Plant And Equipment Disposals\t\t\t\t',
                    'PropertyPlantAndEquipmentAdditions': 'Property Plant And Equipment Additions\t\t\t\t',
                    'PropertyPlantAndEquipmentGrossPeriodIncreaseDecrease': 'Property Plant And Equipment Gross Period Increase Decrease\t\t\t\t',
                'PropertyPlantAndEquipmentGross': 'Property Plant And Equipment Gross\t\t\t',
            'PropertyPlantAndEquipmentNet': 'Property Plant And Equipment Net\t\t',
            'Goodwill': 'Goodwill\t\t',
        'AssetsNoncurrent': 'Assets Non Current\t',
    'Assets': 'Assets',
            'DebtCurrent': 'Debt Current\t\t',
            'AccountsPayableAndAccruedLiabilitiesCurrent': 'Accounts Payable And Accrued Liabilities Current\t\t',
        'LiabilitiesCurrent': 'Liabilities Current\t',
            'LongTermDebtNoncurrent': 'Long Term Debt Non Current\t\t',
        'LiabilitiesNoncurrent': 'Liabilities Non Current\t',
    'Liabilities': 'Liabilities',
    'StockholdersEquity': 'Stockholders Equity',
    'LiabilitiesAndStockholdersEquity': 'Liabilities And Stockholders Equity',
}
