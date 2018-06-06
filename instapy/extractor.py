"""Methods to extract the data for the given usernames profile"""
from time import sleep
from re import findall
import math
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
from datetime import datetime
import json

def difference_between_two_list(list_1,list_2):
  index = 0
  if list_1 and list_2:
    if list_2[0] in list_1:
      first_element = list_2[0]
      for idx,item in enumerate(list_1):
        if item == first_element:
          index = idx
          break
      return list_1[:index]
    else:
      return list_1
  else:
    return list_1

def get_user_info(browser):
  """Get the basic user info from the profile screen"""
  data = browser.find_element_by_xpath("/html/body/script[1]").get_attribute("outerHTML")
  data =  data.replace('<script type="text/javascript">window._sharedData = ', '')\
                .replace(';</script>','')
  data = json.loads(data)
  alias_name = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["full_name"]
  bio = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["biography"]
  prof_img = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["profile_pic_url"]
  num_of_posts = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
  followers = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
  following = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_follow"]["count"]
  
  return alias_name, bio, prof_img, num_of_posts, followers, following


def all_extract_post_info(browser):
  """
  Get the information from the current post
  """
  data  = json.loads(browser.find_element_by_tag_name("pre").text)
  return data

def extract_information(browser, username, limit_amount):
    """Get all the information for the given username"""

    browser.get('https://www.instagram.com/' + username)

    try:
        alias_name, bio, prof_img, num_of_posts, followers, following  = get_user_info(browser)
        if limit_amount <1 :
            limit_amount = 999999
        num_of_posts = min(limit_amount, num_of_posts)
    except:
        print ("\nError: Couldn't get user profile.")

      #prev_divs = browser.find_elements_by_class_name('_70iju')


    try:
        body_elem = browser.find_element_by_tag_name('body')

        #load_button = body_elem.find_element_by_xpath\
        #  ('//a[contains(@class, "_1cr2e _epyes")]')
        #body_elem.send_keys(Keys.END)
        #sleep(3)

        #load_button.click()

        links = []
        links2 = []

        #list links contains 30 links from the current view, as that is the maximum Instagram is showing at one time
        #list links2 contains all the links collected so far

        previouslen = 0
        breaking = 0

        print ("Getting only first",12*math.ceil(num_of_posts/12),"posts only, if you want to change this limit, change limit_amount value in crawl_profile.py\n")  
        while (len(links2) < num_of_posts):

            prev_divs = browser.find_elements_by_tag_name('main')      
            links_elems = [div.find_elements_by_tag_name('a') for div in prev_divs]  
            links = sum([[link_elem.get_attribute('href')
            for link_elem in elems] for elems in links_elems], [])
            for link in links:
              if "/p/" in link:
                links2.append(link) 
            links2 = list(set(links2))   
            print ("Scrolling profile ", len(links2), "/", 12*math.ceil(num_of_posts/12))
            body_elem.send_keys(Keys.END)
            sleep(1.5)

          ##remove bellow part to never break the scrolling script before reaching the num_of_posts
            if (len(links2) == previouslen):
                breaking += 1
                print ("breaking in ",4-breaking,"...\nIf you believe this is only caused by slow internet, increase sleep time in line 149 in extractor.py")
            else:
                breaking = 0
            if breaking > 3:
                print ("\nNot getting any more posts, ending scrolling.") 
                sleep(2)
                break
            previouslen = len(links2)   
          ##

    except NoSuchElementException as err:
        print('- Something went terribly wrong\n')

    post_infos = []

    counter = 1  
    
    for link in links2:
      print ("\n", counter , "/", len(links2))
      counter = counter + 1
      template = str('?taken-by=' + username)
      link = link.replace(template,'?__a=1')
      browser.get(link)
      sleep(2)
      print ("\nScrapping link: ", link)
      try:
        post = all_extract_post_info(browser)
        post_infos.append(post)
      except NoSuchElementException:
        print('- Could not get information from post: ' + link)
        
    time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    information = {
            'full_name': alias_name,
            'username': username,
            'bio': bio,
            'prof_img': prof_img,
            'num_of_posts': num_of_posts,
            'followers': followers,
            'following': following,
            'time_of_scrapping':time,
            'posts': post_infos     
    }

    return information
