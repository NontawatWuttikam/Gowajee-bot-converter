from logging import error
from selenium import webdriver
import selenium
from webdriver_manager.chrome import ChromeDriverManager
import time
import numpy as np
import os
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import requests
import json
from json import JSONDecodeError
import pandas as pd
import tqdm
import soundfile as sf
import pandas as pd

options = webdriver.ChromeOptions() 

options.add_argument('--user-data-dir=C:/Users/PM-COMPUTER/AppData/Local/Google/Chrome/User Data')
options.add_argument('--profile-directory=Profile 1')
# options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

df = pd.read_excel('output.xlsx')

# df["Gowajee"] = ''

save_every = 10
for i,row in df.iterrows():
    file_name = rf'VoiceLog-20211111T044542Z-001\VoiceLog\{row["File"]}'
    try:
        data = np.memmap(file_name, dtype='h', mode='r')
    except FileNotFoundError:
        continue
    speech_array = np.array(data/data.max())
    sf.write(r'temp.wav', speech_array, 16000, 'PCM_16')

    driver.get("http://20.198.242.235/")
    upload = driver.find_element_by_xpath('/html/body/div/section/section/main/div/div/div/div[1]/div/div/div/div/div/div/form/div/div[1]/div[2]/div/div/div/div/div/div[1]/div/div/div[2]/div/span/div[1]/span/input')
    upload.send_keys(r"D:\Gowajee_asr_selenium\temp.wav")
    time.sleep(3)
    generate_butt = driver.find_element_by_xpath('/html/body/div[1]/section/section/main/div/div/div/div[2]/div/div/div/div/button')
    generate_butt.click()
    time.sleep(3)
    text_area = driver.find_element_by_xpath('/html/body/div[1]/section/section/main/div/div/div/div[1]/div/div/div/div/div/div/form/div/div[3]/div[2]/div/div/div/textarea')

    df.iloc[i, df.columns.get_loc('Gowajee')]  = text_area.text
    print(text_area.text)
    if i % 10 == 0:
        df.to_excel("output.xlsx",sheet_name="Sheet1")
        print("save", i)

df.to_excel("output.xlsx",sheet_name="Sheet1")


