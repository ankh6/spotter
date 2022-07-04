from interfaces.Exchange import Exchange
from typing import Dict, List, Union
from services import reporter

def standardize_trading_pair(input: str):
    tmp_input: List[str] = input.split("-")
    return tmp_input[0] + tmp_input[1]


def standarize_trading_pairs_for_stream(list_of_trading_pairs: str):
    return [trading_pair.lower() for trading_pair in list_of_trading_pairs]

def find_union(left_container: List[str], right_container: List[str], amount: int=20) -> List:
    union_container = list()
    try:
        for symbol in left_container:
            if len(union_container) == amount:
                print(f"Reached full size: {len(union_container)}")
                return union_container
            else:
                # Converting format of trading pair from KuCoin to format on Binance
                _symbol = standardize_trading_pair(symbol)
                if _symbol in right_container:
                    union_container.append(symbol)
                    print(f"Added {symbol} to the list of markets. #{len(union_container)} markets")
        return union_container
    except IndexError:
        raise IndexError("Container is empty !")
    except Exception as e:
        print(e.args)
        raise e

def compute_spread_percentage(bid, ask):
    return (1 - (bid / ask)) * 100

def generate_trading_report(trading_attributes: Dict[str,List[Union[int,str]]], exchange: Exchange):
    for trading_pair, values in trading_attributes.items():
        if exchange == exchange.KUCOIN:
            trading_pair = standardize_trading_pair(trading_pair)
        reporter._create_report(date=values[0], trading_pair=trading_pair, bid=values[1],ask=values[2],spread_percentage=values[3], exchange=exchange.name)
