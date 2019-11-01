#University of Melbourne
#School of computing and information systems
#Master of Information Technology
#Semester 2, 2019
#2019-SM2-COMP90055: Computing Project
#Software Development Project
#Cryptocurrency Analytics Based on Machine Learning
#Supervisor: Prof. Richard Sinnott
#Team member :Tzu-Tung HSIEH (818625)
#             Yizhou WANG (669026)
#             Yunqiang PU (909662)

from crontab import CronTab

cron = CronTab(user='ubuntu')
# doing the daily job at 15:00 UTC time(Melbourne time 1AM)
job = cron.new(command='sh data_execute.sh > /Users/ubuntu/final/cron_error.log', comment='daily job!')
job.hour.on(15)

cron.write()

for i in cron:
    print(i)

print(job.is_valid())


