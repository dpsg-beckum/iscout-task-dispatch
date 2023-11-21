from datetime import datetime as dt


def formatDatetime(timestamp : dt) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp.date() == dt.today().date() else timestamp.strftime("%m/%d/%Y, %H:%M:%S")