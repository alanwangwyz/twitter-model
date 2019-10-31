# Twitter API Yizhou Wang
processor_1 = {}
# processor_1['mongodb_address'] = ""
# processor_1['mongodb_db_name'] = ""
# processor_1['mongodb_username'] = ""
# processor_1['mongodb_password'] = ""
processor_1['keyword']='₿'
processor_1['consumer_key'] = 'rxbw7bzT55aGcAfwuGVhESbYO'
processor_1['consumer_secret'] = 'k5roYh4ZRpefcKRpvbcICETWckxnzvVJsWGTMnwSRSzHLsrunm'
processor_1['access_token'] = '1119404173794037760-MOlDKaPnJ9tRltnzmvXpjSm1K8YDYZ'
processor_1['access_token_secret'] = 'WNSjFMUqIN5d2G9YI6WTy4b00AHZQBpfLAIRONXVXrLhD'
processor_1['task'] = "Listener"

processor_2 = {}
# processor_2['mongodb_address'] = ""
# processor_2['mongodb_db_name'] = ""
# processor_2['mongodb_username'] = ""
# processor_2['mongodb_password'] = ""
processor_2['keyword']='XBT'
processor_2['consumer_key'] = 'IebiFcbdxxg5sFHV3K1ADBxo9'
processor_2['consumer_secret'] = 'OT0XQ9Cg0Ar4BQGT6REvFEmfDxsHYNdA1JGP9xHVihH6AvXk8x'
processor_2['access_token'] = '1164754898296008706-kLJmU4e3fXPrToTQmQEhkuNCXFjYsY'
processor_2['access_token_secret'] = 'KQPtlbF3BIuX5HYJentXHTjWEzfb9OPCx92lFuP4XWa53'
processor_2['task'] = "Listener"

processor_3 = {}
# processor_3['mongodb_address'] = ""
# processor_3['mongodb_db_name'] = ""
# processor_3['mongodb_username'] = ""
# processor_3['mongodb_password'] = ""
processor_3['keyword'] = 'BTC'
processor_3['consumer_key'] = '3WR6H5KMRYKbmXl5qIxGAQzRt'
processor_3['consumer_secret'] = 'Ha6q63iplvhQMtXMazzhQfumYst2U3TfmGOGrCgYJLWa5KqcGA'
processor_3['access_token'] = '1164751815016980480-uqXol8z9NWh1itYfSJfgoZqgHybFAD'
processor_3['access_token_secret'] = 'VEzYJVFtAGBo4WuxUIq8EpaGVqN48upK30NnQwN0guZgk'
processor_3['task'] = "Listener"

processor_4 = {}
# processor_4['mongodb_address'] = ""
# processor_4['mongodb_db_name'] = ""
# processor_4['mongodb_username'] = ""
# processor_4['mongodb_password'] = ""
processor_4['keyword'] = 'cryptocurrency'
processor_4['consumer_key'] = 'um5EuNtKlMmVLMqRslD4gXlBu'
processor_4['consumer_secret'] = 'NqBBQ4HZOtgmSIh20i0XdmiPTqVJPtus6UCs4R869uZJUcTN0S'
processor_4['access_token'] = '2426803213-URMjRbwn9A7YrgU1CwHaRp1gnZ0Mw3M4b7xr5kk'
processor_4['access_token_secret'] = 'PfgCMUVkdvh9atGjHHZ28tuOjg9XiqhzXSWYrCHDXehUf'

processor_5 = {}
# processor_5['mongodb_address'] = ""
# processor_5['mongodb_db_name'] = ""
# processor_5['mongodb_username'] = ""
# processor_5['mongodb_password'] = ""
processor_5['keyword'] = 'BTC'
processor_5['consumer_key'] = 'n6LyNaP5EboggbbX54LI8V6NC'
processor_5['consumer_secret'] = 'f5ZoX5k1hISAbW1LKjgQoemjP9RZ08TSpHexeuyiY2imsrojbN'
processor_5['access_token'] = '863425363-t1toS1SzXZO3Y4OrOIYZZhN1adhXX8O2jzhDzOtj'
processor_5['access_token_secret'] = 'PrL1I16jiVwqvO7HjbpdtADKAcGNu46Km4JT73KLxm3lI'

config = {}
for i in range(5):
    config[i + 1] = locals()["processor_" + str(i + 1)]