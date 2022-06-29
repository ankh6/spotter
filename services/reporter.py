from csv import Error, writer
import sys

def _create_report(date, trading_pair: str, bid, ask, spread_percentage):
    with open(f"./reports/{trading_pair}.csv", mode="a", newline="\n") as file:
        try:
            _writer = writer(file)
            row = [date,trading_pair,bid,ask,spread_percentage]
            _writer.writerow(row)
        except Error as csv_error:
            sys.exit(f"file {file}\n{csv_error}")
        except Exception as e:
            print(e.args)
            raise e