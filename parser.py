# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 18:51:07 2023

@author: Sonya
"""
from scrapy import Selector
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()

driver.get("https://www.marvel.com/characters")
time.sleep(2)

#close ckoockies banner
err=driver.find_element(by=By.ID, value="onetrust-close-btn-container")
err.click()

#create list of characrets link

list_of_href=[]
for i in range(78):
    # check elements
    info = driver.find_element(by=By.CLASS_NAME, value=
    "full-content")
    el = info.find_elements(By.CLASS_NAME,
    "explore__link")
    for elems in el:
        list_of_href.append(elems.get_attribute('href'))

    
    #find button and change page

    butt=driver.find_element(by=By.CLASS_NAME, value=
    'pagination')
    bitt = butt.find_elements(By.TAG_NAME, value = 'li')
    actions = ActionChains(driver)
    actions.move_to_element(bitt[-1]).perform()
    if bitt[-1]:
        bitt[-1].click()
        time.sleep(1)        
key_search_err=[]
error_list_no_key=[]
error_list_2=[]
dataset=[]
for e in list_of_href:
    print(e)
    microset={}
    try:
        html = requests.get(e).content
        sel = Selector( text = html )
        key=sel.xpath('//*[@class="railBioInfoItem__label"]/text()').extract()
        text=sel.xpath('//*[@class="railBioLinks"]//text()').extract()
        if not key:
            try:
                href=sel.xpath('//*[@class="masthead__tabs__link\n                      "]//@href').extract()
                for elem in href:
                    if '/in-comics'in elem and 'profile' not in elem:
                        href_a="https://www.marvel.com"+elem
                            
                html = requests.get(href_a).content
                sel = Selector( text = html )
                key=sel.xpath('//*[@class="railBioInfoItem__label"]/text()').extract()
                text=sel.xpath('//*[@class="railBioLinks"]//text()').extract()
            except:
                print("   Key search error   ")
                key_search_err.append(e)
                
        if not key:
            error_list_no_key.append(e)
        name=sel.xpath('//*[@class="masthead__eyebrow"]/text()').get()        
        if not name:
            name=sel.xpath('//*[@class="masthead__container masthead__container_playing-false "]//text()').get()
        microset["name"]=name
        microset["link"]=e        
        if key:
            d={}
            for i in range(len(key)):
                d[key[i].lower()]=text[i]
                
            if "universe" in d.keys():
                if d["universe"]=='Marvel Universe':
                    for elem in d:
                        if elem in ["universe", "other aliases", "education", "place of origin", "identity", "know relatives"]:
                            microset[elem] = d[elem]
                                              
                    dataset.append(microset)    
    except:
        error_list_2.append(e)
#create dataset        
scv_file=pd.DataFrame(data=dataset)
scv_file.to_csv('final_list.csv') 

