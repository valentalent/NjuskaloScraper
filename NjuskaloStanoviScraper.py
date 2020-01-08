import requests
from bs4 import BeautifulSoup
import re
import time
from csv import writer
import pandas as pd


def check_stan(br):
    URL = 'https://www.njuskalo.hr/prodaja-stanova/zagreb?page=' + str(br)
    print(URL)
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    sviStanovi = soup.find_all(attrs={"name": re.compile("[0-9]{8}")})

    data = pd.read_csv("nebitno.csv", encoding="ISO-8859-1")
    print(data)
    with open('nebitno.csv', 'a') as csv_file:
        csv_writer = writer(csv_file)
        for stan in sviStanovi:
            str_stan = str(stan)
            allIDs = re.findall("[0-9]{8}", str_stan)
            filterIDs = allIDs[0]
            if('30373' in filterIDs):
                continue
            if(data['ID'].str.contains(filterIDs).any()):
                continue
            else:
                csv_writer.writerow([filterIDs])


br = 1

while(True):
    check_stan(br)
    br += 1
    if(br > 12):
        br = 1
        time.sleep(120)
