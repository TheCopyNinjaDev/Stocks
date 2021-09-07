import asyncio
from datetime import datetime

from tinkoff.investments import (
    CandleResolution,
    Environment,
    TinkoffInvestmentsRESTClient,
)
from tinkoff.investments.utils.historical_data import HistoricalData
import pandas as pd

TOKEN = "t.OSXZNWhaTPOEYpt3FoCeqSegYPNtOgocRvmL0IX4c5rTQiSGP-pJ0ZHSIpmHGd5wTF_lt9P8tdW_PTSTXRIahw"
DATA = {}
times = []
price = []


async def get_minute_candles(ticker: str, period):
    # show 1 minute candles for AAPL in 1 year period of time
    async with TinkoffInvestmentsRESTClient(
        token=TOKEN, environment=Environment.SANDBOX
    ) as client:
        historical_data = HistoricalData(client)
        instruments = await client.market.instruments.search("AAPL")
        stock_figi = instruments[0].figi
        print(stock_figi)
        async for candle in historical_data.iter_candles(
            figi="BBG000B9XRY4",
            dt_from=datetime(2021, 6, 1),
            dt_to=datetime(2021, 8, 29),
            interval=CandleResolution.MIN_15,
        ):
            d = candle.to_dict()
            times.append(d['time'])
            price.append(d['c'])
            DATA['time'] = times
            DATA['price'] = price
            df = pd.DataFrame(data=DATA, index=range(len(DATA['time'])))
            df.to_csv(f"../data/{ticker}/{period}.csv")


asyncio.run(get_minute_candles())