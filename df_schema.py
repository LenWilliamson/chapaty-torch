import os
from typing import Final, Dict, List

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