from bs4 import BeautifulSoup
from selenium import webdriver
import statistics
import requests


PATH = r'/usercode/chromedriver'
driver = webdriver.Chrome(PATH)

driver.get("https://boxrec.com/en/ratings?r%5Brole%5D=box-pro&r%5Bsex%5D=M&r%5Bstatus%5D=a&r%5Bdivision%5D=Heavyweight&r%5Bcountry%5D=&r_go=");

soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup.prettify())

