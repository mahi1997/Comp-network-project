from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/usr/lib/chromium-browser')
url = driver.current_url
print (url)
