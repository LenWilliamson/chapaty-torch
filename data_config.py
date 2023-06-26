# Configuration file for data
import os
from typing import Final, Dict, List
import sys

# Set working directory to the directory containing the script that was used to invoke the Python interpreter
CWD: Final[str] = 'gs://trust-data/strategy'

# Data paths to directories (external drive): /media/len/ExterneFestplateLenCewa/DataBase
OHLC_DP: Final[str] = os.path.join(CWD, 'ppp', '6e', '2022', 'day', 'ohlc-1h')
VOLP_DP: Final[str] = os.path.join(CWD, 'ppp', '6e', '2022', 'day', 'vol')


# Ninja
# Column names. These list should only be used for initialization of data frames. Use the corresponding dicts
OHLC_CNL: Final[List[str]] = ['ots', 'open', 'high',
                              'low', 'close', 'cts', 'cw', 'weekday', 'in_interval']
AGTR_CNL: Final[List[str]] = ['atid', 'px',
                              'qx', 'ftid', 'ltid', 'ts', 'bm', 'btpm']
VOL_CNL: Final[list[str]] = ['px', 'qx']

# Reference dictionaries
OHLC_CN: Final[Dict[str, str]] = {
    'openTime': 'ots',
    'open': 'open',
    'high': 'high',
    'low': 'low',
    'close': 'close',
    'closeTime': 'cts',
}
VOLP_CN: Final[Dict[str, str]] = {
    'price': 'px',
    'quantity': 'qx',
}


# Test Data
# Column names. These list should only be used for initialization of data frames. Use the corresponding dicts
T_OHLC_CNL: Final[List[str]] = ['ots', 'open', 'high', 'low',
                                'close', 'vol', 'cts', 'qav', 'not', 'tbbav', 'tbqav', 'ignore', 'cw', 'in_interval']
T_AGTR_CNL: Final[List[str]] = ['atid', 'px',
                                'qx', 'ftid', 'ltid', 'ts', 'bm', 'btpm']
T_VOL_CNL: Final[list[str]] = ['px', 'qx']

# Reference dictionaries
T_OHLC_CN: Final[Dict[str, str]] = {
    'openTime': 'ots',
    'open': 'open',
    'high': 'high',
    'low': 'low',
    'close': 'close',
    'volume': 'vol',
    'closeTime': 'cts',
    'quoteAssetVol': 'qav',
    'numberOfTrades': 'not',
    'takerBuyBaseAssetVol': 'tbbav',
    'takerBuyQuoteAssetVol': 'tbqav',
    'ignore': 'ignore',
    'calendarWeek': 'cw',
    'inInterval': 'in_interval',
}
T_AGTR_CN: Final[Dict[str, str]] = {
    'aggTradeId': 'atid',
    'price': 'px',
    'quantity': 'qx',
    'firstTradeId': 'ftid',
    'lastTradeId': 'ltid',
    'timestamp': 'ts',
    'buyerMaker': 'bm',
    'bestTradPriceMatch': 'btpm',
}
T_VOLP_CN: Final[Dict[str, str]] = {
    'price': 'px',
    'quantity': 'qx',
}
