import asyncio
from datetime import datetime
from tinkoff.investments import (
    CandleResolution,
    Environment,
    TinkoffInvestmentsRESTClient,
)
from tinkoff.investments.utils.historical_data import HistoricalData
import pandas as pd
import os

TOKEN = "t.OSXZNWhaTPOEYpt3FoCeqSegYPNtOgocRvmL0IX4c5rTQiSGP-pJ0ZHSIpmHGd5wTF_lt9P8tdW_PTSTXRIahw"
DATA = {}
times = []
price = []


async def get_minute_candles(ticker: str, start: datetime, end: datetime):
    async with TinkoffInvestmentsRESTClient(
        token=TOKEN, environment=Environment.SANDBOX
    ) as client:
        historical_data = HistoricalData(client)
        instruments = await client.market.instruments.search(ticker)
        stock_figi = instruments[0].figi
        async for candle in historical_data.iter_candles(
            figi=stock_figi,
            dt_from=start,
            dt_to=end,
            interval=CandleResolution.MIN_15,
        ):
            d = candle.to_dict()
            times.append(d['time'])
            price.append(d['c'])
        DATA['time'] = times
        DATA['price'] = price
        df = pd.DataFrame(data=DATA, index=range(len(DATA['time'])))
        os.mkdir(f'../data/{ticker}')
        df.to_csv(f"../data/{ticker}/{str(start)[:10]} - {str(end)[:10]}.csv")


start = pd.to_datetime('2021.03.01')
end = pd.to_datetime('2021.09.01')

asyncio.run(get_minute_candles('ATVI', start, end))