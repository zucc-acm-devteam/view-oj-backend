import datetime


def timestamp_to_str(timestamp):
    return datetime.datetime.strftime(
        datetime.datetime.fromtimestamp(
            timestamp, datetime.timezone(datetime.timedelta(hours=8))), '%Y-%m-%d %H:%M:%S')


def str_to_datetime(raw):
    return datetime.datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
