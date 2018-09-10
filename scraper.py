"""
OWLET SR Scraper
Created by ajd344
Revised by RainbowLegend

Revision 1.0
Added while loop and made it to move to new columns
"""

import requests
import datetime
import csv
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

while 1:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'client-secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("OWLET Master Spreadsheet").worksheet("S4_stats")

    column = int(sheet.cell(1, 1).value)

    listOfHashes = sheet.get_all_values()

    finished = {}
    btags = []

    for row in listOfHashes:
        btags.append(row)

    print(datetime.date.today())
    sheet.update_cell(2, column, f'SR@{str(datetime.date.today())}')

    for name in btags:
        if len(name) > 0:
            tag = name[0]
            print(tag)
            cell = sheet.find(tag)
            tag = tag.replace('#', '-')
            tag = tag.replace(" ", "")
            player = f'https://playoverwatch.com/en-us/career/pc/{tag}'
            try:
                page = requests.get(player)
                soup = BeautifulSoup(page.content, 'html.parser')
                ret = soup.find(class_="competitive-rank").get_text()

            except:
                try:
                    ret = soup.find(class_='header-masthead').get_text()
                    newTag = tag.split("-")
                    if ret.lower() == newTag[0].lower():
                        ret = 'ND'
                except:
                    ret = ' '
            finished[name[0]] = ret
            if cell.row == 2:
                pass
            else:
                sheet.update_cell(cell.row, column, ret)
    sheet.update_cell(2, column, f'SR@{str(datetime.date.today())}')
    column = column + 1
    sheet.update_cell(1, 1, str(column))
    time.sleep(252900)
