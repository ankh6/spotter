# spotter
A spotting bot that detects possible market opportunities on centralized exchanges

## Getting started

**You will need to have the latest version of [Python](https://www.python.org/downloads/) and [Visual Studio Code](https://code.visualstudio.com/download) installed !**

If you would still like to run the spotter from source please follow the instructions below 👇

#### Clone the repo
`git clone https://github.com/ankh6/spotter.git`


#### Install the requirements
`pip install -r requirements.txt `


#### Open your favorite terminal 
#### Navigate to the spotter folder

`cd spotter`


#### Run the spotter
`python spotter.py`

## Features

Supported exchanges: Binance, KuCoin

The spotter execution can be decomposed in three parts:

1. Initialization
2. Searching for shared markets/trading pairs between exchanges
3. Calculation of the spread percentage based on tickers

#### Initialization

Given the supported exchanges, the spotter initializes itself by retrieving **once** all the available markets on the exchanges. It does this by hitting the `exchangeInfo` endpoint on Binance and the `symbols` endpoint on KuCoin.

Once the spotter has stored all the available markets, it is time to find out which markets are shared between exchanges

#### Finding markets/trading pairs that are shared across the exchanges

The *find_union* function in the `utils/MarketRetrieverUtils` module handles this task. Consider two sets, the containers that store the markets, B(Binance) and K(KuCoin). We use the [membership test operation](https://docs.python.org/3.8/reference/expressions.html?highlight=membership#membership-test-operations) to evaluate whether a trading pair in set K is in the set B.
The base and quote assets on KuCoin are seperated by a dash, while this is not the case for trading pairs on Binance. To ensure that the evaluation works well, we apply a standardization process on the trading pairs on set K. If the trading pair is shared between exchanges, we add it to a container. We repeat this process an arbitrary amount of time (here, 20 times).

Once we have the shared markets, it is time to retrieve their tickers and compute the bid-ask spread percentage.


#### Calculation of the spread percentage given the tickers

We calculate the bid-ask spread percentage to compare the spread for different assets with different bid and ask prices. This helps us understand the true costs of the bid-ask spread and not to be biaised by the scale of the price. Indeed the same spread is much more expensive at low asset prices than at high asset prices. It is calculated by simply taking the bid-ask spread and dividing it by the ask price.

Once we have calculated the spread for all the trading pairs exposed by the exchanges, we create a `reports` folder in the current working directory and write the following values in a csv file that is named after the trading pair.

- date (in timestamp)
- trading pair name
- highest bid price
- lowest ask price
- bid-ask spread percentage
- the exchange (i.e. Binance or KuCoin)

Please note that:
1. We write all information into the csv file, even if the bid-ask spread percentage is 0.
2. As many csv files are written as there are trading pairs you are interested in: for a given trading pair, the tickers of Binance and KuCoin are written in the same csv file.


The spotter runs every minute. I deliberatively chose an low timeframe to maximise the arbitrage opportunities by having lots of data points.


## What is next ?
- Consume stream data with websockets
    - More efficient to open a websocket connect, subscribe to a topic for a specific timeframe
- Import the csv files and create Pandas dataframe for data analysis
- If needed, Use Adapter pattern for client transparency

## Disclaimer
This software is for educational purposes only. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. Do not risk money which you are afraid to lose. There might be bugs in the code - this software DOES NOT come with ANY warranty.
