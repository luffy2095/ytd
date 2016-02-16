from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import base64
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])


driver.maximize_window()
driver.get("https://kissanime.to/Anime/Diamond-no-Ace-Second-Season/Episode-044?id=122513")
wait = WebDriverWait(driver, 30)
search = wait.until(EC.presence_of_element_located((By.ID, "selectQuality")))
a=driver.find_element_by_id("selectQuality")#.text
bodyText = driver.find_element_by_tag_name('body').text
x=a.find_elements_by_tag_name("option")

for k in x:
	print base64.b64decode(str(k.get_attribute("value")))


