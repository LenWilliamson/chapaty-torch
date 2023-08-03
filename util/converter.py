import datetime as dt

def posix_to_homan_readable_timestamp(time_stamp: float) -> str:
    """
    Accepts posix time stamp in milliseconds and converts it to human readable format
    :param time_stamp: posix time in milliseconds
    :return: %Y-%m-%d %H-%M-%S
    """

    date_time: str = dt.datetime.utcfromtimestamp(
        time_stamp / 1000).strftime('%Y-%m-%d %H-%M-%S')
    return date_time