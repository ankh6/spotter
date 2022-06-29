from typing import Dict, Iterable, List, Union
from services import reporter

def standardize_trading_pair(input: str):
    tmp_input = input.split("-")
    return tmp_input[0] + tmp_input[1]

def find_union(left_container: Iterable[str], right_container: Iterable[str], amount: int=20) -> List:
    union_container = list()
    try:
        for symbol in left_container:
            if len(union_container) == amount:
                print(f"Reached full size: {len(union_container)}")
                return union_container
            else:
                _symbol = standardize_trading_pair(symbol)
                if _symbol in right_container:
                    union_container.append(symbol)
                    print(f"Found {symbol}. Added to the list of markets\nNumer of markets: {len(union_container)}")
        return union_container
    except IndexError:
        raise IndexError("Container is empty !")
    except Exception as e:
        print(e.args)
        raise e

def compute_spread_percentage(bid, ask):
    return (abs(bid - ask) / ask) * 100

def generate_trading_report(trading_attributes: Dict[str,Union[List[str], List[int]]]):
    for trading_pair, values in trading_attributes.items():
        reporter._create_report(date=values[0], trading_pair=trading_pair, bid=values[1],ask=values[2],spread_percentage=values[3])
