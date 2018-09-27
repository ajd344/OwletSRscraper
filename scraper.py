import requests
import csv
from bs4 import BeautifulSoup
import re
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\Users\Andrew\Documents\client-secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("OWLET Master Spreadsheet").worksheet("Stage 4 Rosters")

listOfHashes = sheet.get_all_values()

finished = {}
btags = []
format = re.compile(".*[#]*\d")

for row in  listOfHashes:
    if format.match(row[2]):
        btags.append(row)
col = [i for i, n in enumerate(btags[0]) if n == ''][1]

for player in btags:
    name = player[2]
    if (len(name) > 0):
        tag = name
        cell = sheet.find(tag)
        tag = tag.replace('#', '-')
        tag = tag.replace(" ", "")
        link = 'https://playoverwatch.com/en-us/career/pc/' + tag

        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            ret = soup.find(class_="competitive-rank").get_text()
        except:
            ret = "ND"
        finished[name] = ret
        sheet.update_cell(cell.row, col+1, ret)
