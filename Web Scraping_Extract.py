from splinter import Browser
from bs4 import BeautifulSoup
listings = {}
def init_browser():
    '''
    Create path for google chrome driver and use Browser to execute the driver
    '''
    executable_path = {"executable_path":"Resources/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    '''
    Call the init_browser fuction to initiate chrome browser,
    use google chrome to surf the web about canadian mining companies and scrape info about those
    top 40 company names. Transform it and save it as csv file for later loading step.
    '''
    browser = init_browser()
   # listings = {}
    url = "http://www.canadianminingjournal.com/features/who-are-the-top-40/"
    browser.visit(url)
    html = browser.html
    title = []
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("strong")
    for item in titles:
        title.append(item.text.replace("\xa0","")) # scrape all wanted info from the website and modify them by replacing any \xa0 with blank
    listings["miningco"] = title # store the title in a dict
    browser.quit() # exit browser when finished
    return listings # choose the listings which contains all top 40 companies as the returned value of this function

# call function to execute it so we get the listings of top 40 mining companies
scrape()

import pandas as pd
titles_2 = []
for item in listings["miningco"]:
    item = item[5:-9] # only get the company name and revenue from the string
    item = item.split(" (") # split name and revenue so can create two data frame columns later
    titles_2.append(item) # store each list of company name and revenue in a list
df = pd.DataFrame(titles_2) # create dataframe using the list of all company names and revenues
df.columns = ["Company","Revenue (Million)"] # give columns names
df.to_csv("Resources/Top 40 Mining Companies by Revenue.csv") # export it as a csv file