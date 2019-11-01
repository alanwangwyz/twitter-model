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

# this file recode all the developer account for our crawling use.

# Twitter API Yizhou Wang
twitter_1 = {}
twitter_1['consumer_key'] = 'rxbw7bzT55aGcAfwuGVhESbYO'
twitter_1['consumer_secret'] = 'k5roYh4ZRpefcKRpvbcICETWckxnzvVJsWGTMnwSRSzHLsrunm'
twitter_1['access_token'] = '1119404173794037760-MOlDKaPnJ9tRltnzmvXpjSm1K8YDYZ'
twitter_1['access_token_secret'] = 'WNSjFMUqIN5d2G9YI6WTy4b00AHZQBpfLAIRONXVXrLhD'

twitter_2 = {}
twitter_2['consumer_key'] = 'IebiFcbdxxg5sFHV3K1ADBxo9'
twitter_2['consumer_secret'] = 'OT0XQ9Cg0Ar4BQGT6REvFEmfDxsHYNdA1JGP9xHVihH6AvXk8x'
twitter_2['access_token'] = '1164754898296008706-kLJmU4e3fXPrToTQmQEhkuNCXFjYsY'
twitter_2['access_token_secret'] = 'KQPtlbF3BIuX5HYJentXHTjWEzfb9OPCx92lFuP4XWa53'

# Twitter API Tzu-Tung HSIEH
twitter_3 = {}
twitter_3['consumer_key'] = '3WR6H5KMRYKbmXl5qIxGAQzRt'
twitter_3['consumer_secret'] = 'Ha6q63iplvhQMtXMazzhQfumYst2U3TfmGOGrCgYJLWa5KqcGA'
twitter_3['access_token'] = '1164751815016980480-uqXol8z9NWh1itYfSJfgoZqgHybFAD'
twitter_3['access_token_secret'] = 'VEzYJVFtAGBo4WuxUIq8EpaGVqN48upK30NnQwN0guZgk'

twitter_4 = {}
twitter_4['consumer_key'] = 'um5EuNtKlMmVLMqRslD4gXlBu'
twitter_4['consumer_secret'] = 'NqBBQ4HZOtgmSIh20i0XdmiPTqVJPtus6UCs4R869uZJUcTN0S'
twitter_4['access_token'] = '2426803213-URMjRbwn9A7YrgU1CwHaRp1gnZ0Mw3M4b7xr5kk'
twitter_4['access_token_secret'] = 'PfgCMUVkdvh9atGjHHZ28tuOjg9XiqhzXSWYrCHDXehUf'

# Twitter API Yunqing Pu
twitter_5 = {}
twitter_5['consumer_key'] = 'n6LyNaP5EboggbbX54LI8V6NC'
twitter_5['consumer_secret'] = 'f5ZoX5k1hISAbW1LKjgQoemjP9RZ08TSpHexeuyiY2imsrojbN'
twitter_5['access_token'] = '863425363-t1toS1SzXZO3Y4OrOIYZZhN1adhXX8O2jzhDzOtj'
twitter_5['access_token_secret'] = 'PrL1I16jiVwqvO7HjbpdtADKAcGNu46Km4JT73KLxm3lI'

config = {}
for i in range(5):
    config[i + 1] = locals()["twitter_" + str(i + 1)]