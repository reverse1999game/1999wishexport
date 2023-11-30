import requests
from bs4 import BeautifulSoup
import json

character_dict = {}

response = requests.get("https://res1999.huijiwiki.com/wiki/%E8%A7%92%E8%89%B2%E5%88%97%E8%A1%A8")
print(response)
soup = BeautifulSoup(response.content, "html.parser")
all_child_divs = soup.find('div', {'class': 'character-list'})

for item in all_child_divs:
    url = item.findNext("div").find('a').get("href")
    character_url = requests.get("https://res1999.huijiwiki.com" + url)

    soup_ = BeautifulSoup(character_url.content, "html.parser")

    characterName = soup_.select('[style*="display: flex;flex-direction: column"]')
    
    characterID = soup_.find('div', attrs={'style':'display:block;','class':"infobox-box"}).select('[style*="padding-top:10px"]')

    print(characterName[0].text)
    print(characterID[0].text[5:])

    cName = characterName[0].text.split(" ",1)[0]
    character_dict.update({cName : characterID[0].text[5:]})

    print("================")

# print(character_dict)

j = json.dumps(character_dict, indent=4, ensure_ascii=False)
with open("configAll.json", "w", encoding="utf-8") as outfile: 
    print(j, file=outfile)
