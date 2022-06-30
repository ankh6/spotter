from csv import Error, writer
from interfaces.Exchange import Exchange
import sys

def _create_report(date, trading_pair: str, bid: float, ask: float, spread_percentage: float, exchange: Exchange):
    with open(f"./reports/{trading_pair}.csv", mode="a", newline="\n") as file:
        try:
            _writer = writer(file)
            row = [date,trading_pair,bid,ask,spread_percentage, exchange]
            _writer.writerow(row)
        except Error as csv_error:
            sys.exit(f"file {file}\n{csv_error}")
        except Exception as e:
            print(e.args)
            raise e