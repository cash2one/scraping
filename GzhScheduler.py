#!/usr/bin/env python
#coding:utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from BaiduHotwords import SearchByBaiduHotwords
def searchByBaiduHotwords():
    search = SearchByBaiduHotwords()


scheduler = BlockingScheduler()
scheduler.add_job(searchByBaiduHotwords,'cron',minute="37")
scheduler.start()