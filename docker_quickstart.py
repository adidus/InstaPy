from instapy import InstaPy

# Write your automation here
# Stuck ? Look at the github page or the examples in the examples folder

insta_username = 'zeusfsx'
insta_password = 'instagrambot'

dont_like = ['food', 'girl', 'hot']
ignore_words = ['pizza']
friend_list = ['friend1', 'friend2', 'friend3']

# If you want to enter your Instagram Credentials directly just enter
# username=<your-username-here> and password=<your-password> into InstaPy
# e.g like so InstaPy(username="instagram", password="test1234")

bot = InstaPy(username=insta_username, password=insta_password, selenium_local_session=False)
bot.set_selenium_remote_session(selenium_url='http://selenium:4444/wd/hub')
bot.login()
bot.set_relationship_bounds(enabled=True,
             potency_ratio=-1.21,
              delimit_by_numbers=True,
               max_followers=4590,
                max_following=5555,
                 min_followers=45,
                  min_following=77)
bot.follow_by_list(followlist=['_s_vadim'], times=1, sleep_delay=600, interact=False)
bot.end()
