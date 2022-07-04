from constants import BINANCE_WEBSOCKET_BASE_URL
from interfaces.Exchange import Exchange
from interfaces.MarketRetriever import MarketRetriever
from json import dumps
from typing import List
from utils import MarketRetrieverUtils
import websocket


class BinanceMarketRetriever(MarketRetriever):
    ''' Concrete class that implements methods from Abstract class MarketRetriever
    '''

    def __init__(self):
        self._trading_pairs: List[str] = None
        self.exchange_name: Exchange = Exchange.BINANCE
        self._websocket_connection: websocket.WebSocket = None
        self._websocket_id_counter: int = 0
        
    def _get_trading_pairs(self):
        ''' Returns the list of trading pairs on KuCoin
        '''
        return self._trading_pairs

    
    def _get_stream_id_counter(self) -> int :
        ''' Returns the current counter value used
        '''
        return self._websocket_id_counter
    
    def _get_websocket_connection(self) -> websocket.WebSocket:
        return self._websocket_connection

    
    def create_websocket_to_binance(self, base_websocket_endpoint=BINANCE_WEBSOCKET_BASE_URL, is_raw_stream:bool=True):
        if is_raw_stream:
            raw_stream = "ws"
        base_websocket_endpoint  = base_websocket_endpoint + "/" + raw_stream
        self._websocket_connection = websocket.create_connection(url=base_websocket_endpoint)
        return self._websocket_connection
    
    def subscribe_to_stream(self, connection: websocket.WebSocket, trading_pairs:List[str], stream_name: str):
        # Binance returns status code 101 if connection is established
        if connection.getstatus() != 101:
            raise Exception("Connection may not be establised/alive")
        request_id = self._get_stream_id_counter()
        request_id += 1
        trading_pairs: List[str] = MarketRetrieverUtils.standarize_trading_pairs_for_stream(trading_pairs)
        _trading_pairs = [trading_pair + "@" + stream_name for trading_pair in trading_pairs]
        payload = {"method":"SUBSCRIBE","params": _trading_pairs, "id": request_id }
        try:
            connection.send(dumps(payload))
        except Exception as e:
            print(e.args)
            raise e
        finally:
            self._websocket_id_counter = request_id