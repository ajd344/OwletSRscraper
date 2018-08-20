import requests
import csv
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import timer


while(1):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\Users\Andrew\Documents\client-secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("OWLET Master Spreadsheet").worksheet("Map Count Code")

    listOfHashes = sheet.get_all_values()

    finished = {}
    btags = []

    for row in listOfHashes:
        btags.append(row)

    for name in btags:
        if (len(name) > 0):
            tag = name[0]
            cell = sheet.find(tag)
            tag = tag.replace('#', '-')
            tag = tag.replace(" ", "")
            player = 'https://playoverwatch.com/en-us/career/pc/' + tag
            try:
                page = requests.get(player)
                soup = BeautifulSoup(page.content, 'html.parser')
                ret = soup.find(class_="competitive-rank").get_text()
            except:
                ret = ""
            finished[name[0]] = ret
            sheet.update_cell(cell.row, 5, ret)
    timer.sleep(252900)
