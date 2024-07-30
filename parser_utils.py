import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import config
# import pdb

def log_into_goodreads(driver):
    driver.get(config.LOGIN_URL)
    access_sign_in_btn = driver.find_element(By.CLASS_NAME, "authPortalSignInButton")
    access_sign_in_btn.click()

    load_dotenv()
    email_field = driver.find_element(By.ID, "ap_email")
    password_field = driver.find_element(By.ID, "ap_password")
    email_field.send_keys(os.getenv("GR_EMAIL"))
    password_field.send_keys(os.getenv("GR_PASSWORD"))
    sign_in_btn = driver.find_element(By.ID,"signInSubmit")
    sign_in_btn.click()
    # pdb.set_trace() # to add if needing to enter the captcha

def selenium_request():
    driver = webdriver.Chrome()
    log_into_goodreads(driver)
    return driver

def soup_init(html):
    return BeautifulSoup(html, "html.parser")
