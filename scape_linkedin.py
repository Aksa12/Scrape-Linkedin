from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


COMPANY = 222852511 #careem company code
COUNTRY = "pk" #location pakistan
EMAIL = input("Email: ")
PASSWORD =  input("Password: ")
EMPLOYEE = 1000  # number of results
linkedin = 'https://www.linkedin.com'

# Open browser
browser = webdriver.Chrome(executable_path='C:/Users/Aksa/Downloads/chromedriver_win32/chromedriver.exe')
browser.get(linkedin)
time.sleep(6)


# Login to the website
email = browser.find_element_by_name('session_key')
password = browser.find_element_by_name('session_password')
email.send_keys(EMAIL + Keys.RETURN)
password.send_keys(PASSWORD + Keys.RETURN)

time.sleep(3)


search = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%"+ str(COMPANY) +"%22%5D&facetGeoRegion=%5B%22" + str(COUNTRY) + "%3A0%22%5D&origin=FACETED_SEARCH"
browser.get(search)
time.sleep(3)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
current_url = 'url_placeholder'  # this is a placeholder for the URL check

# Create empty dataframe
df = pd.DataFrame(columns=['name', 'title', 'location', 'profile'])

# Go through pages and download data
while True:
    # Check to see if url is the 100th page in search
    if current_url.find('page=100') != -1:
        break
    # Check to see if this is the end of the search
    previous_url = current_url
    current_url = browser.current_url
    if current_url == previous_url:
        break

    # Start scraping and filling in the dataframe
    time.sleep(5)
    page = BeautifulSoup(browser.page_source, 'html.parser')
    page_names = page.find_all('span', class_='actor-name')
    page_titles = page.find_all('p', class_='subline-level-1')
    page_locations = page.find_all('p', class_='subline-level-2')
    page_profiles = page.find_all('a', class_='search-result__result-link')

    # Put scraped data into a dataframe
    names = list(map(lambda x: x.text, page_names))
    titles = list(map(lambda x: x.text.replace('\n', ''), page_titles))
    locations = list(map(lambda x: x.text.replace('\n', ''), page_locations))
    profiles = list(map(lambda x: linkedin + x['href'], page_profiles))[::2]
    temp = pd.DataFrame({'name': names, 'title': titles, 'location': locations, 'profile': profiles})

    # Filter out members who do not provide information
    temp = temp[temp['name'] != 'LinkedIn Member']

    # Append new data to df
    df = df.append(temp)

    # Stop appending if the number of retrieved records exceeds the limit
    if df.shape[0] >= EMPLOYEE:
        break

    #going to the next page
    nextt = browser.find_elements_by_css_selector("button span.artdeco-button__text")[-2]
    browser.execute_script("arguments[0].click();", nextt)
    time.sleep(5)
# Reset dataframe index
df.reset_index()

# save the results into a csv file
df.to_csv("output_search.csv", index=False)

# Close browser
browser.quit()