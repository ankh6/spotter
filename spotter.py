from constants import SPOTTER_RUNNING_FREQUENCY
from errors.Exception import UnsupportedExchangeError
from interfaces.Exchange import Exchange
from interfaces.MarketRetriever import MarketRetriever
from markets.BinanceMarketRetriever import BinanceMarketRetriever
from markets.KuCoinMarketRetriever import KuCoinMarketRetriever
from os import mkdir
from typing import Dict, List, Union
from utils import MarketRetrieverUtils
import asyncio

async def initialize():
    '''' Initialization of the spotter

    Returns:
    binance: the binance object
    kucoin: the kucoin object
    union_markets_set: the list of markets that are on both Binance and KuCoin
    '''
    binance: MarketRetriever = BinanceMarketRetriever()
    kucoin: MarketRetriever = KuCoinMarketRetriever()
    print("Fetching markets from Binance. . .")
    await binance.fetch_trading_pairs()
    print("Fetching markets from KuCoin. . .")
    await kucoin.fetch_trading_pairs()
    binance_symbols: List[str] = binance._get_trading_pairs()
    kucoin_symbols: List[str] = kucoin._get_trading_pairs()
    print("Fetching markets that are on both Binance and KuCoin. . .")
    union_markets_set: List[str] = MarketRetrieverUtils.find_union(left_container=kucoin_symbols, right_container=binance_symbols)
    mkdir("./reports")
    return (binance, kucoin, union_markets_set)


async def monitor_spread_on_exchanges(exchanges, trading_pairs: List[str]):
    ''' Given the exchanges and the trading pairs, it fetches the tickers that are
    time, trading pair, highest bid, lowest ask, spread percentage and the name of the exchange

    Arguments:
    exchanges: the list of exchanges that have been initialized by initialize()
    union_markets_set: the list of of markets that are on both Binance and KuCoin

    '''
    for exchange in exchanges:
        if exchange.exchange_name not in (Exchange.BINANCE, Exchange.KUCOIN):
            raise UnsupportedExchangeError(f"The exchange {exchange.exchange_name} is not supported")
        try:
            print(f"Fetching highest bid and lowest ask on {exchange.exchange_name}. . .")
            tickers: Dict[str,List[Union[int,str]]] = await exchange.fetch_tickers(trading_pairs)
            print(f"Building report. . .")
            MarketRetrieverUtils.generate_trading_report(tickers, exchange.exchange_name)
        except Exception as e:
            print(e.args)
            raise e
        print("Created reports located inside './reports' folder")


async def execute_monitoring(exchanges: List[MarketRetriever], union_markets_set: List[str]):
    '''
    Wrapper for the execution of the monitoring.
    Executes every minute, value of SPOTTER_RUNNING_FREQUENCY

    Arguments:
    exchanges: the list of exchanges that have been initialized by initialize()
    union_markets_set: the list of of markets that are on both Binance and KuCoin
    '''
    await monitor_spread_on_exchanges(exchanges=exchanges, trading_pairs=union_markets_set)
    while True:
        print(f"Waiting for {SPOTTER_RUNNING_FREQUENCY} seconds before next run")
        await asyncio.sleep(SPOTTER_RUNNING_FREQUENCY)
        await execute_monitoring(exchanges=exchanges, union_markets_set=union_markets_set)

if __name__ == '__main__':
    # Run coroutines
    binance, kucoin, markets = asyncio.run(initialize())
    asyncio.run(execute_monitoring([binance, kucoin], markets))