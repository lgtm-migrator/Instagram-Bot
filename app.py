import re
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class InstagramBot:
    """Class to define login and like photo methods"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        """User login using credentials"""
        bot = self.bot
        bot.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        email = bot.find_element_by_name("username")
        password = bot.find_element_by_name("password")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(4)

    def like_photos(self, hashtag):
        """Search hashtag URL and like first 50 posts"""
        time.sleep(1)
        count = 0
        bot = self.bot
        bot.get("https://www.instagram.com/explore/tags/" + hashtag)
        time.sleep(2)

        # simulate scroll for lazy loading
        for i in range(3):
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1+i)

        # Get all links, which will be later cleaned for the posts
        links = bot.find_elements_by_xpath('//div/a')
        links_hrefs = []
        for link in links:
            # if links have href tag, add it to the list
            try:
                links_hrefs.append(link.get_attribute('href'))
            except Exception as unhandled_exception:
                pass

        for image in links_hrefs:
            try:
                # Check if the links contains posts
                val = re.search(r'^https://www\.instagram\.com/p/', image)
                bot.get(val.string)

                # random sleep between 1 - 3 secs for any 'unusual activity'
                time.sleep(random.choice([1, 2, 3]))

                # Like post
                bot.find_element_by_class_name('wpO6b').click()
                count += 1

                # Don't like more than 50 posts
                if count > 49:
                    break
                time.sleep(1)
            except Exception as unhandled_exception:
                pass

        print("liked {} posts".format(count))
        bot.quit()


# Magic!
USER = InstagramBot(os.environ.get('username'), os.environ.get('pass'))
USER.login()
USER.like_photos('hashtag-to-search')
