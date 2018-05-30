
import json
from instapy import InstaPy

insta_username = 'zeusfsx'
insta_password = 'instagrambot'

# if you want to run this script on a server,
# simply add nogui=True to the InstaPy() constructor

usernames = []

with open('instagram_accounts.csv','r') as file:
    temp = file.readlines()
    for user in temp:
        usernames.append(user.replace("\n",""))

session = InstaPy(username=insta_username, password=insta_password, nogui= True)
session.login()

#Read instagram_accounts from file

# end the bot session
session.end()
