from instapy import InstaPy
import sys

insta_username = sys.argv[1]
insta_password = sys.argv[2]

# if you want to run this script on a server,
# simply add nogui=True to the InstaPy() constructor

usernames = []
#Read instagram_accounts from file
with open('instagram_accounts.csv','r') as file:
    temp = file.readlines()
    for user in temp:
        usernames.append(user.replace("\n",""))
print(usernames[:10])

session = InstaPy(username=insta_username, password=insta_password, nogui= True)
session.login()
#session.follow_by_list(usernames,times = 1,sleep_delay = 4743, interact = False)
limit_amount = 60
session.accounts_to_json(usernames,limit_amount)
#session.feeds_to_json()

# end the bot session
session.end()
