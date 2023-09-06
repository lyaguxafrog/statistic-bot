from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver2 as uc



from selenium.webdriver import Chrome


driver = Chrome()



url = str(f'https://t.me/s/makridos')

driver.get(url)

views = driver.find_element(By.CLASS_NAME,'tgme_widget_message_views' )

print(views)