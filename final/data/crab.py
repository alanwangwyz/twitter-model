#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crontab import CronTab

cron = CronTab(user='wangyizhou')
# submit the daily analysis job at 14:05 UTC time(Melbourne time 0:05)
job = cron.new(command='sh data_execute.sh > /Users/wangyizhou/Desktop/cron_error.log', comment='daily job for price!')


job.hour.on(14)

cron.write()

for item in cron:
    print(item)

print(job.is_valid())


