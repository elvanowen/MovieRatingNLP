from TwitterSearch import *
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['Doctor Strange']) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'kbibzVdoRoKOwd3dlxZCobum5',
        consumer_secret = 'qEz32mJANlQ5hbFGacxmMfO2Pmyexs3WgPFeGq4QzA88qAOKe8',
        access_token = '1348353366-ofrMAMNiFfz102VY9c3MXdTrsAD2c4Dq91QiWVD',
        access_token_secret = 'Io7orEnOvE2Rv2sdiASLRkLTVFA93DmSyF4r1i9CYQCXn'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)