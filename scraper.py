"""
OWLET SR Scraper
Created by ajd344

Revision 1.0
Added while loop and made it to move to new columns
"""

import requests
import csv
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

print('Hello! Import checks successful.')

while 1:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'client-secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("OWLET Master Spreadsheet").worksheet("Myst: TEST")
    botCode = client.open("OWLET Master Spreadsheet").worksheet("Bot Code")

    print('Successfully logged into 2 sheets!')

    column = int(botCode.cell(2, 2).value)

    listOfHashes = sheet.get_all_values()
    print(listOfHashes)

    finished = {}
    btags = []

    for row in listOfHashes:
        btags.append(row)

    print('Successfully appended btags.')

    for name in btags:
        if len(name) > 0:
            tag = name[2]
            print(tag)
            try:
                cell = sheet.find(tag)
                tag = tag.replace('#', '-')
                tag = tag.replace(" ", "")
                player = f'https://playoverwatch.com/en-us/career/pc/{tag}'
                try:
                    page = requests.get(player)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    ret = soup.find(class_="competitive-rank").get_text()

                    print(f'Player SR found: {tag} at {ret} SR')
                except:
                    ret = ""
                finished[name[0]] = ret
                sheet.update_cell(cell.row, column, ret)
                print(f'Player {tag} with {ret} SR successfully updated to sheet')
            except gspread.exceptions.CellNotFound:
                print('gspread.exceptions.CellNotFound')
    print(f'Column {str(column)} completed.')
    column = column + 1
    print(f'Moving onto column {str(column)}')
    #  botCode.update_cell(2, 2, str(column))
    print('Slumbering...')
    time.sleep(252900)
    print('New cycle starting.')
