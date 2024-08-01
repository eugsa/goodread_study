"""Diverse specific methods used by the parser."""
import os
import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import config

def log_into_goodreads(driver, debug):
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

    if debug:
        pdb.set_trace()

def selenium_request(debug):
    driver = webdriver.Chrome()
    log_into_goodreads(driver, debug)
    return driver

def soup_init(html):
    return BeautifulSoup(html, "html.parser")
