"""
Description:
Author:qxy
Date: 2019/11/3 11:37 上午
File: filters 
"""
import datetime


def handle_time(time):
    """
    time看距离现在的时间间隔
    1.如果间隔时间小于1分钟，那么就显示"刚刚"
    2.如果是一小时以内，那么就显示"xxx分钟前"
    3.如果是24小事以内，那么就显示"xxx小时前"
    4.如果是大于24小时，小于30天以内，那么就显示"xxx天前"
    5.否则就显示具体时间
    """
    if isinstance(time, datetime.datetime):
        now = datetime.datetime.now()
        timestamp = (now-time).total_seconds()
        # total_seconds()是获取两个时间之间的总差。seconds()方法仅获取时间差的秒数，忽略天数
        if timestamp < 60:
            return "刚刚"
        elif 60 <= timestamp < 60 * 60:
            minutes = timestamp / 60
            return "%s分钟前" % int(minutes)
        elif 60 * 60 <= timestamp < 60 * 60 * 24:
            hours = timestamp / (60 * 60)
            return "%s小时前" % int(hours)
        elif 60 * 60 * 24 <= timestamp < 60 * 60 * 24 * 30:
            days = timestamp / (60 * 60 * 24)
            return "%s天前" % int(days)
        elif 60 * 60 * 24 * 30 <= timestamp < 60 * 60 * 24 * 30 * 12:
            days = timestamp / (60 * 60 * 24 * 30)
            return "%s月前" % int(days)

        elif 60 * 60 * 24 * 30 * 12 <= timestamp < 60 * 60 * 24 * 30 * 12 * 100:
            days = timestamp / (60 * 60 * 24 * 30 * 12)
            return "%s年前" % int(days)
        else:
            return time.strftime('%Y-%M-%d %H:%M')