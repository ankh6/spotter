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
    union_markets_set = MarketRetrieverUtils.find_union(left_container=kucoin_symbols, right_container=binance_symbols)
    mkdir("./reports")
    while True:
        print(f"Fetching highest bid and lowest ask on {kucoin.exchange_name}. . .")
        kucoin_tickers = kucoin.fetch_tickers(union_markets_set)
        print(f"Fetching highest bid and lowest ask on {binance.exchange_name}. . .")
        binance_tickers = binance.fetch_tickers(union_markets_set)
        print(f"Building reports. . .")
        MarketRetrieverUtils.generate_trading_report(kucoin_tickers, kucoin.exchange_name)
        MarketRetrieverUtils.generate_trading_report(binance_tickers, binance.exchange_name)
        print("Created reports located inside './reports' folder")
        # Wait for 1 minute
        sleep(frequency_in_seconds)

if __name__ == '__main__':
    run()