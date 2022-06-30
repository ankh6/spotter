from constants import BINANCE_API_BASE_URL, BINANCE_API_VERSION, SUPPORTED_STABLECOINS
from interfaces.Exchange import Exchange
from interfaces.MarketRetriever import MarketRetriever
from requests import get
from time import time
from typing import List, Tuple
from utils import MarketRetrieverUtils

class BinanceMarketRetriever(MarketRetriever):
    ''' Concrete class that implements methods from Abstract class MarketRetriever
    '''

    def __init__(self):
        self._trading_pairs: List[str] = None
        self.exchange_name: Exchange = Exchange.BINANCE
    
    async def fetch_resources(self, url: str, version: str, endpoint: str, params: List[Tuple[str,str]] = None):
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
    
    async def fetch_trading_pairs(self):
        ''' Wrapper function that encapsulates the logic of interacting with Binance's API to retrieve the trading pairs
        that have a supported stablecoin (BUSDC, USDC, USDT) as a quote asset
        '''
        try:
            response = await self.fetch_resources(url=BINANCE_API_BASE_URL, version=BINANCE_API_VERSION, endpoint="exchangeInfo")
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
    
    async def fetch_tickers(self, trading_pairs: List[str]):
        ''' Wrapper function that encapsulates the logic of interacting with KuCoin's API to retrieve
        the tickers of the trading pairs that are passed as an argument

        Arguments:
        trading_pairs, a list of trading pairs in the format base_asset - quote_asset
        '''
        trading_attributes = dict()
        for trading_pair in trading_pairs:
            _trading_pair = MarketRetrieverUtils.standardize_trading_pair(trading_pair)
            response = await self.fetch_resources(url=BINANCE_API_BASE_URL, version=BINANCE_API_VERSION, endpoint="ticker/bookTicker", params=[("symbol", _trading_pair)])
            highest_bid = float(response["bidPrice"])
            lowest_ask = float(response["askPrice"])
            print(f"Binance - Computing spread percentage for symbol {_trading_pair}. . .")
            try:
                spread_percentage = MarketRetrieverUtils.compute_spread_percentage(highest_bid, lowest_ask)
                trading_attributes[_trading_pair] = [time(), highest_bid, lowest_ask, spread_percentage]
            except ZeroDivisionError:
                print(f"There is no demand for the pair {_trading_pair}. Reasons might be that either bid or ask are 0")
                trading_attributes[_trading_pair] = [time(), highest_bid, lowest_ask, spread_percentage]
            except Exception:
                print(Exception.args)
                print(Exception)
        return trading_attributes
