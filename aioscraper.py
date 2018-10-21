from bs4 import BeautifulSoup
import aiohttp
import re
import aiospread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Andrew\Documents\client-secret.json', scope)
client = aiospread.authorize(creds)


async def scraper(client):
    sheet = await client.open("OWLET Master Spreadsheet").worksheet("Stage 4 Rosters")

    list_of_hashes = await sheet.get_all_values()

    finished = {}
    btags = []
    fmt = re.compile(".*[#]*\d")

    for row in list_of_hashes:
        if fmt.match(row[2]):
            btags.append(row)
    col = [i for i, n in enumerate(btags[0]) if n == ''][1]

    for player in btags:
        name = player[2]
        if len(name) > 0:
            tag = name
            cell = await sheet.find(tag)
            tag = tag.replace('#', '-')
            tag = tag.replace(" ", "")
            link = f'https://playoverwatch.com/en-us/career/pc/{tag}'

            try:
                async with aiohttp.ClientSession() as cs:
                    page = cs.get(link)
                soup = BeautifulSoup(page.content, 'html.parser')
                ret = soup.find(class_="competitive-rank").get_text()
            except aiospread.CellNotFound:
                ret = "ND"
            finished[name] = ret
            await sheet.update_cell(cell.row, col + 1, ret)
