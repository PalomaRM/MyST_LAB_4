import asyncio
import ccxt.async_support as ccxta
import time
import numpy as np
import pandas as pd


async def async_client(exchange_id, run_time: int, symbol: str):
    orderbook = None
    exchange = getattr(ccxta, exchange_id)()
    time_1 = time.time()
    time_f = 0

    ob = []
    while time_f <= run_time:
        try:
            await exchange.load_markets()
            market = exchange.market(symbol)
            orderbook = await exchange.fetch_order_book(market["symbol"])
            datetime = exchange.iso8601(exchange.milliseconds())
            # Unpack values
            ask_price, ask_size = np.array(list(zip(*orderbook["asks"]))[0:2])
            bid_price, bid_size = np.array(list(zip(*orderbook["bids"]))[0:2])
            # Check length of ask_price & bid_price
            ask_price_len = len(ask_price)
            bid_price_len = len(bid_price)

            min_elems = min(ask_price_len, bid_price_len)
            # Remove extra elements in array with length >
            ask_price = ask_price[:min_elems]
            bid_price = bid_price[:min_elems]

            # Check length of ask_size & bid_size
            ask_size_len = len(ask_size)
            bid_size_len = len(bid_size)

            min_elems2 = min(ask_size_len, bid_size_len)
            # Remove extra elements in array with length >
            ask_size = ask_size[:min_elems2]
            bid_size = bid_size[:min_elems2]

            spread = np.round(ask_price - bid_price, 4)
            mid_price=np.round((ask_price[0]+bid_price[0])/2,4)
            vwap=np.round(((ask_price * ask_size).sum() + (bid_price * bid_size).sum())/(ask_size.sum()+bid_size.sum()),4)
            levels=len(ask_price)
            # Final data format for the results
            ob.append(
                {
                    "exchange": exchange_id,
                    "datetime": datetime,
                    #"orderbook": {
                    "ask_size": ask_size.sum(),
                    "ask": ask_price.sum(),
                    "bid": bid_price.sum(),
                    "bid_size": bid_size.sum(),
                    "spread": spread.sum(),
                    "mid_price":mid_price,
                    "vwap":vwap,
                    "levels":levels
                    #},
                }
            )
            # End time
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
            print(f"Added price - {market['symbol']}")
        except Exception as e:
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
            print(type(e).__name__, str(e))
    await exchange.close()
    return ob


async def multi_orderbooks(exchanges, run_time: int, symbol: str):
    input_coroutines = [
        async_client(exchange, run_time, symbol) for exchange in exchanges
    ]
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return orderbooks


if __name__ == "__main__":
     exchanges = ["bigone", "blockchaincom","bitso"]
     #exchanges = ["bigone", "blockchaincom", "bitforex"]
     run_time = 3600 # seconds
     symbol1 = "BTC/USDT"
     #symbol1 = "ETH/USDT"

     data1 = asyncio.get_event_loop().run_until_complete(multi_orderbooks(exchanges, run_time=run_time, symbol=symbol1))
     data1 = [item for sublist in data1 for item in sublist]
     data1 = pd.DataFrame(data1)

data1.to_csv('files/BTCUSDT.csv')
#data1.to_csv('files/ETHUSDT.csv')
