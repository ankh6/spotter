from constants import BINANCE_API_BASE_URL, BINANCE_API_VERSION, SUPPORTED_STABLECOINS
from interfaces.MarketRetriever import MarketRetriever
from requests import get
from typing import List, Tuple

class BinanceMarketRetriever(MarketRetriever):
    ''' Concrete class that implements methods from Abstract class MarketRetriever
    '''

    def __init__(self):
        self._trading_pairs: List[str] = None
    
    
    def fetch_resources(self, url: str, version: str, endpoint: str, params: List[Tuple[str,str]] = None):
        ''' Implementation of abstract function fetch_resources

        Arguments:
        url, the base_url of the API
        version, the version of the API
        endpoint, the endpoint of the API
        params, optional, the query parameters that are appended to the full path

        Returns:
        The resources in a json format
        '''

        request_parameters = params
        full_path = url + "/" +version + "/" + endpoint
        response = get(url=full_path, params=request_parameters)
        return response.json()

    
    def _get_trading_pairs(self):
        ''' Returns the list of trading pairs on KuCoin
        '''
        return self._trading_pairs
    
    def fetch_trading_pairs(self):
        ''' Wrapper function that encapsulates the logic of interacting with Binance's API to retrieve the trading pairs
        that have a supported stablecoin (BUSDC, USDC, USDT) as a quote asset
        '''
        try:
            response = self.fetch_resources(url=BINANCE_API_BASE_URL, version=BINANCE_API_VERSION, endpoint="exchangeInfo")
            symbols = response["symbols"]
            symbol_container = list()
            for quote in symbols:
                if quote["quoteAsset"] in SUPPORTED_STABLECOINS:
                    symbol_container.append(quote["symbol"])
            self._trading_pairs = symbol_container
            self._get_trading_pairs()
        except Exception as e:
            print(e.args)
            raise e
    
    def fetch_tickers(self):
        pass