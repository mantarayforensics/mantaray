import datetime


def Windows_Time_Converter_module (dt):
    print (dt)
    microseconds = int (dt, 16) / 10
    seconds, microseconds = divmod (microseconds, 1000000)
    days, seconds = divmod (seconds, 86400)

    # return datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, microseconds)
    time = datetime.datetime (1601, 1, 1) + datetime.timedelta (days, seconds, microseconds)
    #print(time)
    #print format(getFiletime(time), '%a, %d %B %Y %H:%M:%S %Z')

    return time
