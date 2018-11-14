import numpy as np
import pandas as pd

from textblob import TextBlob

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import sys, re, time
import datetime

def scrape_twitter_posts(crypto, date_1, no_of_days, url):
    options = Options()
	# if you want to run the program with chrome being visibly open, COMMENT the below line
    options.headless = True # make the chrome webdriver not visible
	
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    #url = 'https://twitter.com/search?l=en&q=ethereum%20OR%20eth'
    url_end = ''

    for _ in range(int(no_of_days)):
        date_2 = datetime.datetime.strftime(((datetime.datetime.strptime(date_1, "%Y-%m-%d")) + datetime.timedelta(days=1)),'%Y-%m-%d')
        url_end += url
        url_end += "%20since%3A" + str(date_1)
        url_end += "%20until%3A" + str(date_2) + "&src=typd" # url is appened properly
		# Note -> the date_1 will be substituted with date_2 at the end of the loop
        driver.get(url_end) # opening the url
        time.sleep(2)

        try:
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # scolls indifinitly till the bellow check point is true
                if(driver.find_element_by_xpath("//button[@class='btn-link back-to-top hidden']").is_displayed()):
                    print("true check 1")
                    lastHeight = driver.execute_script("return document.body.scrollHeight")
                    print("last height = " + str(lastHeight))

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(6)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("scrolled after true check 1")

                    newHeight = driver.execute_script("return document.body.scrollHeight")
                    print("new height = " + str(newHeight))
                    # does a comparison of body height is true to see whether the infinite scroll is actually completed
                    if newHeight == lastHeight:
                        print("true check 2")
                        break
                    else:
                        print("true check continue")
                        continue
            # end of infinte scroll

            tweets = driver.find_elements_by_class_name('tweet-text')
            print("----------------------\nDate = "+ date_1 + "\n----------------------")
            print("----------------------\nTotal no. of tweets collected = "+ str(len(tweets)) + "\n----------------------")

            df = pd.DataFrame(data=[tweet.text.encode('utf-8') for tweet in tweets], columns=['Tweets'])
            df['date'] = date_1
            df['polarity'] = np.array([TextBlob(tweet.text).sentiment.polarity for tweet in tweets])
            df.to_csv (crypto + date_1 + '.txt' , sep='\t', encoding='utf-8')
        except Exception as e:
                print(e)
                time.sleep(2)

        url_end = '' # removing url_end to make new url for next day
        date_1 = date_2
    
    driver.close()

def main():
    crypto = input("Enter the cryptocurrency ( Eg- bitcoin, bitcoincash, ethereum : ")
    since = input("Enter starting date (Eg: 2017-11-15 ): ")
    no_of_days = input("Enter no. of days : ")
	print("----------------------\n")
	print('Get the url from " https://twitter.com/search-advanced " after typing in all the necessary conditions\n')
	print('And paste it here without putting in date in the search and removing "&src=typd" from the end\n')
	print('Example -> " https://twitter.com/search?l=en&q=ethereum%20OR%20eth " \n')
    url = input("Enter the url : ")

    scrape_twitter_posts(crypto, since, no_of_days, url)

if __name__ == '__main__':
    main()