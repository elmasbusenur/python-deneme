# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 06:41:50 2019

@author: PC
"""

import json
import requests 
from bs4 import BeautifulSoup 

#url ve request işlemleri :request veri çekmeye yarıyor

BEBEK_FORUMLARI_URL = "https://www.bebekforum.net.tr/forumlar/bebek-hastaliklari.24/"
BEBEK_FORUMLARI_REQUEST = requests.get(BEBEK_FORUMLARI_URL) 
#b.s request ile istediğimiz veri kısmını çekmemizi sağlıyor.buna parse işlemi deniyor

BEBEK_FORUMLARI_ICERIK = BeautifulSoup(BEBEK_FORUMLARI_REQUEST.content, "html.parser", from_encoding="utf-8") 
KONU_BASLIKLARI = BEBEK_FORUMLARI_ICERIK.findAll('a', attrs = {'data-tp-prbimary' : 'on'}, href=True) 


                                                                 #linkin class ı
BEBEK_FORUMLARI = {}
BEBEK_FORUMLARI['konular'] = [] #boş bir dizi oluşturdum konular adında

for KONU_BASLIGI in KONU_BASLIKLARI:
    
    KONU_ICERIGI_REQUEST = requests.get("https://www.bebekforum.net.tr" + KONU_BASLIGI['href']) 
    KONU_ICERIGI = BeautifulSoup(KONU_ICERIGI_REQUEST.content, "html.parser", from_encoding="utf-8") 
    KONU_DETAY = KONU_ICERIGI.find('article', attrs = {'class', 'message-body js-selectToQuote'}).text
    

     
    #json dosyaya yazma formatı
    BEBEK_FORUMLARI['konular'].append({  #append yeni eleman ekle
        'konu_basligi' : KONU_BASLIGI.text,
        'konu_adresi' : "https://www.bebekforum.net.tr" + KONU_BASLIGI['href'],
        'konu_icerigi' : KONU_DETAY.replace('\n','').replace('\t')
    })
    
    #json olarak dosya oluşturma
    with open('bebek.json', 'w') as outfile:
        json.dump(BEBEK_FORUMLARI, outfile, indent=4, ensure_ascii=True)
    