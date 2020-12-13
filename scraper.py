import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import date
import sqlite3

# connect to sqldatabase
conn = sqlite3.connect('states.db')
c = conn.cursor()
# creates table one time
# c.execute('''CREATE TABLE states(state TEXT, programming_language TEXT, number_of_jobs INT)''')





# sets the scrapers options for chrome
#  and puts it in incognito mode to simplify scraping
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

PATH = './chromedriver'
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

# base url for job site
URL = 'https://www.indeed.com/'


# list of all states used
states = ['Alabama','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia', 'Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey', 'New York','North Carolina','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']


driver.get(URL)


# Keyword to search for and languages to search for
language_keywords = ['python', 'javascript', 'react javascript', 'java', 'c#', 'c++', 'visual basic']
engineer_keyword = 'software '

# searches landing page for text input area for location and language
# landing page is different from all other search languages
search_for_jobs = driver.find_element_by_id("text-input-what")
search_for_jobs.click()
search_for_jobs.send_keys(engineer_keyword)
search_for_location = driver.find_element_by_id("text-input-where")
search_for_location.click()
search_for_location.send_keys(Keys.CONTROL, "a")
search_for_location.send_keys(Keys.BACK_SPACE)
search_for_location.send_keys('Phoenix, AZ')
search_for_location.send_keys(Keys.RETURN)

# waits for page to load and searches for element
# that displays the amount of jobs
try:
    search = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, "searchCountPages"))
    )
finally:
    search_jobs = driver.find_element_by_id("searchCountPages")


# Function for extracing the number of jobs out of the text
def search_for_number_of_jobs(jobs_available):
    try:
        string_of_jobs = jobs_available.text.split("of ", 2)[1]
        split_jobs = string_of_jobs.split(" ", 2)[0]
        k_before_its_converted_to_int = split_jobs.replace(',', '')
        k= int(k_before_its_converted_to_int)
    except:
        k = 0
    return k


m = search_for_number_of_jobs(search_jobs)

## checks to make sure it was found for debugging purposes
# print("there are {} python engineer jobs in {} as of {} ".format(m, states[0], today))

# Iterates over all states
for state in states:
    # iterates over all languages for each state
    for language in language_keywords:
        search_for_jobs = driver.find_element_by_id("what")
        search_for_jobs.click()
        search_for_jobs.clear()
        search_for_jobs.send_keys(engineer_keyword, language)
        search_for_location = driver.find_element_by_id("where")
        search_for_location.click()
        search_for_location.clear()
        search_for_location.send_keys(state)
        search_for_location.send_keys(Keys.RETURN)

        # waits for element to load
        try:
            search_jobs = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, "searchCountPages"))
            )
            # if element can not be found, sets jobs to 0
        except:
            search_jobs = 'page 1 of 0 jobs'
        m = search_for_number_of_jobs(search_jobs)

        # adds each result into table
        c.execute('''INSERT INTO states values(?,?,?)''', (state, language, m))
        # commits the addition
        conn.commit()

        print("there are {0} {1} {2} jobs in {3} as of {4} ".format(m, engineer_keyword, language, state, today))



c.execute(''' SELECT * FROM states ''')
results = c.fetchall()
print(results)

conn.close()
