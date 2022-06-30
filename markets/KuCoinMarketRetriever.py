from constants import KUCOIN_API_BASE_URL, KUCOIN_API_VERSION, SUPPORTED_STABLECOINS
from interfaces.Exchange import Exchange
from interfaces.MarketRetriever import MarketRetriever
from requests import get
from typing import List, Tuple
from utils import MarketRetrieverUtils


class KuCoinMarketRetriever(MarketRetriever):
    def __init__(self):
        self.exchange_name: Exchange = Exchange.KUCOIN
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
        ''' Wrapper function that encapsulates the logic of interacting with KuCoin's API to retrieve the trading pairs
        that have a supported stablecoin (BUSDC, USDC, USDT) as a quote asset
        '''
        try:
            response = self.fetch_resources(url=KUCOIN_API_BASE_URL, version=KUCOIN_API_VERSION, endpoint="symbols")
            data: List = response["data"]
            symbol_container = list()
            for single_data in data:
                if single_data["quoteCurrency"] in SUPPORTED_STABLECOINS:
                    symbol_container.append(single_data["symbol"])
            self._trading_pairs = symbol_container
        except Exception as e:
            print(e.args)
            print(e)
    
    def fetch_tickers(self, trading_pairs: List[str]):
        ''' Wrapper function that encapsulates the logic of interacting with KuCoin's API to retrieve
        the tickers of the trading pairs that are passed as an argument

        Arguments:
        trading_pairs, a list of trading pairs in the format base_asset - quote_asset
        '''
        trading_attributes = dict()
        for trading_pair in trading_pairs:
            response = self.fetch_resources(url=KUCOIN_API_BASE_URL, version=KUCOIN_API_VERSION, endpoint="market/orderbook/level1", params=[("symbol", trading_pair)])
            data: List = response["data"]
            highest_bid = float(data["bestBid"])
            lowest_ask = float(data["bestAsk"])
            print(f"KuCoin - Computing spread percentage for symbol {trading_pair}. . .")
            try:
                spread_percentage: float = MarketRetrieverUtils.compute_spread_percentage(highest_bid, lowest_ask)
                res = [data["time"], highest_bid, lowest_ask, spread_percentage]
                trading_attributes[trading_pair] = res
            except ZeroDivisionError as e:
                print(f"There is no demand for the pair {trading_pair}. Reasons might be that either bid or ask are 0")
                trading_attributes[trading_pair] = [data["time"], highest_bid, lowest_ask, spread_percentage]
            except Exception:
                print(Exception.args)
                raise Exception
        return trading_attributes