"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : screenshot_test.py
 @Time    : 2019/4/23 16:05
"""
from selenium import webdriver


with webdriver.Chrome("./chromedriver.exe") as driver:
    driver.get("https://google.com")
    driver.save_screenshot("./baidu.png")