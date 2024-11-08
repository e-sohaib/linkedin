import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidCookieDomainException as ICDE
import json
from selenium.webdriver.common.keys import Keys
# Create a driver instance
driver = webdriver.Chrome()
#driver.delete_all_cookies()
if not os.path.isfile('cookies.json'):
    email = "linked in email"
    password = "limked in password"
    # Navigate to a website
    driver.get("https://www.linkedin.com/login")
    time.sleep(10)
    #elements = driver.find_element("//div[@class='content']")
    email_field = driver.find_element(By.XPATH, '//*[@id="username"]')
    email_field.send_keys(email)
    password_field =driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.send_keys(password)
    signin_button = driver.find_element(By.XPATH , '//html/body/div[1]/main/div[2]/div[1]/form/div[3]/button')
    signin_button.click()
    time.sleep(30)
    # Save cookies to a file
    k = driver.get_cookies()
    with open('cookies.json', 'w') as file:
        json.dump(k, file) 
    file.close()
else: 
    # Load cookies from a file
    with open('cookies.json', 'r') as file:
        cookies = json.load(file)

# Goto the same URL
driver.get('https://www.linkedin.com/')
time.sleep(1)
# Set stored cookies to maintain the session
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()        
time.sleep(3)

serch_word = "search "
serch_box = driver.find_element(By.XPATH ,  "/html/body/div[6]/header/div/div/div/div[1]/input")
serch_box.send_keys(serch_word)
serch_box.send_keys(Keys.ENTER)
time.sleep(10)
filter_serch = driver.find_element(By.XPATH , "/html/body/div[6]/div[3]/div[2]/section/div/nav/div/ul/li[3]/button").click()
time.sleep(10)
#result_pages_len = driver.find_element(By.XPATH , '/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[4]/div/div/ul').find_elements(By.TAG_NAME ,"li")
#loop_time = len(result_pages_len)
url = driver.current_url.split("&sid")[0]
def write_it(any:list):
    with open("result.txt" , 'a' , encoding = 'utf-8') as my:
        for item in any:
            my.write(item[0] + ':' +item[1]+'\n')
for k in range(2,10):
    print(url)
    list_company = []
    for i in range(1,11):
        link = driver.find_element(By.XPATH , f"/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{i}]/div/div/div/div[2]/div/div[1]/div/span/span/a")
        comany_name = link.get_attribute('innerHTML').strip().replace("<!---->",'')
        company_page = link.get_attribute('href')
        list_company.append([comany_name , company_page])
    write_it(list_company)
    driver.get(url +'&page='+ str(k))
    time.sleep(10)