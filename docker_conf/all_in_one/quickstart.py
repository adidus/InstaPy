
import json
from instapy import InstaPy

insta_username = ''
insta_password = ''

# if you want to run this script on a server,
# simply add nogui=True to the InstaPy() constructor


session = InstaPy(username=insta_username, password=insta_password, nogui= True)
session.login()

browser = session.get_browser()

usernames = []
#Read instagram_accounts from file
with open('instagram_accounts.csv','r') as file:
    temp = file.readlines()
    for user in temp:
        usernames.append(user.replace("\n",""))

#SETTINGS:
#set limit of posts to analyze:
limit_amount = 12
    
print ("Waiting 10 sec")
browser.implicitly_wait(10)

try:

	for username in usernames:
		print('Extracting information from ' + username)
		information, user_commented_list = extract_information(browser, username, limit_amount)

		with open('./profiles/' + username + '.json', 'w') as fp:
			fp.write(json.dumps(information, indent=4))
                                                     
		print ("Number of users who commented on his/her profile is ", len(user_commented_list),"\n")
		file = open("./profiles/" + username + "_commenters.txt","w") 
		for line in user_commented_list:
			file.write(str(line))
			file.write('\t\n')
		file.close()     
		print ("\nFinished. The json file and nicknames of users who commented were saved in profiles directory.\n")

except KeyboardInterrupt:
    print('Aborted...')

# end the bot session
session.end()
