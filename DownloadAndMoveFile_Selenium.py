# -*- coding: utf-8 -*-
"""
Created on Fri May 14 16:50:14 2021

@author: Fabian Schlueter
"""

from selenium import webdriver
import glob
import time
import os
import shutil

# open webbrowser
driver = webdriver.Chrome(r"C:\Users\Fabian\Downloads\chromedriver_win32\chromedriver.exe") # path to chromedriver. Download file from https://chromedriver.chromium.org/

# open website
driver.get('https://github.com/FabianSchlueter/Crawler-autoscout24.de/blob/main/Porsche.xlsx')

# Only if needed on other websites: Insert credentials for login
# enter user, password and click on login
# user = '' # user name
# pw = '' # password
# driver.find_element_by_xpath('//*[@id="userNameInput"]').send_keys(user)
# driver.find_element_by_xpath('//*[@id="passwordInput"]').send_keys(pw)
# driver.find_element_by_xpath('//*[@id="submitButton"]').click()
# time.sleep(3)

# Click on download button. Download will start immediatley
driver.find_element_by_xpath('//*[@id="raw-url"]').click()
# Wait for download to finish
time.sleep(5)

#%% Move downloaded file to another directory.

def move_download(path_downloads, path_destination):
    # Get all files in downloads
    list_of_files = glob.glob(path_downloads) # * means all. if need specific format then *.csv
    # Identify just downloaded file by picking the newest
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    
    source = latest_file
    destination = path_destination + r'\\' + os.path.basename(latest_file)
    shutil.copy(source, destination)

# Path where downloads are autmatically saved
path_downloads = r'C:\Users\Fabian\Downloads\*'
# Path to move the downloaded file to
path_destination = r'C:\Users\Fabian\Desktop\\'

move_download(path_downloads, path_destination)
