from constants import SPOTTER_RUNNING_FREQUENCY
from markets.BinanceMarketRetriever import BinanceMarketRetriever
from markets.KuCoinMarketRetriever import KuCoinMarketRetriever
from os import mkdir
from time import sleep
from utils import MarketRetrieverUtils


def run(frequency_in_seconds: int=SPOTTER_RUNNING_FREQUENCY):
    '''
    Main routine
    '''
    binance = BinanceMarketRetriever()
    kucoin = KuCoinMarketRetriever()
    print("Fetching markets from Binance. . .")
    binance.fetch_trading_pairs()
    print("Fetching markets from KuCoin. . .")
    kucoin.fetch_trading_pairs()
    binance_symbols = binance._get_trading_pairs()
    kucoin_symbols = kucoin._get_trading_pairs()
    print("Fetching markets that are on both Binance and KuCoin. . .")
    union_markets = MarketRetrieverUtils.find_union(left_container=kucoin_symbols, right_container=binance_symbols)
    mkdir("./reports")
    while True:
        print("Fetching highest bid and lowest ask on KuCoin. . .")
        last_values = kucoin.fetch_tickers(union_markets)
        MarketRetrieverUtils.generate_trading_report(last_values)
        print("Created reports located inside './reports' folder")
        # Wait for 1 minute
        sleep(frequency_in_seconds)

if __name__ == '__main__':
    run()