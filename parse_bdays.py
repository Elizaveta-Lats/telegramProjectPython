import requests
import json


def parse_resp_json(char_url,lang):
    # Get character info as a proper dictionary
    char_page_request = requests.get(char_url, headers={"x-rpc-language": lang})
    char_info = json.loads(char_page_request.text)["data"]["page"]["modules"][0]["components"][0]["data"]
    char_info_list = json.loads(char_info)['list']
    #print("char_info_list: ", char_info_list)

    char_dict = {}
    for dictionary in char_info_list:
        #print(dictionary)
        key = str(dictionary['key']).replace(":", "").replace("<span style=\"color: rgba(255, 255, 255, 0.85)\">", "")
        value = str(dictionary['value']).replace("<p>", "").replace("</p>", "")
        char_dict[key] = value

    return char_dict

page_url = "https://sg-wiki-api.hoyolab.com/hoyowiki/wapi/get_entry_page_list"

try:
    header = {"path": "/hoyowiki/wapi/get_entry_page_list",
              "accept": "application/json, text/plain, */*",
              #"accept-language": "ru-RU,ru;q=0.9,en-US;q==0.8,en;q=0.7",
              "content-type": "application/json;charset=UTF-8",
              "cookie": "_MHYUUID=fe71f53d-6774-48f1-b32c-750e719895c9; ltoken=B9HNO5uj6BXGvKKBbTUdSCqd8ZtjeYrizg0kQljL; ltuid=97814507; mi18nLang=ru-ru; DEVICEFP_SEED_ID=277f89e6cfc17165; DEVICEFP_SEED_TIME=1660477079623; DEVICEFP=38d7ea78f5da4; _gid=GA1.2.803865553.1661080410; _ga_GEYW4HC0FV=GS1.1.1661115999.5.1.1661116000.0.0.0; _ga=GA1.2.384733250.1660477079; _gat_gtag_UA_206868027_17=1",
              "origin": "https://wiki.hoyolab.com",
              "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
              "x-rpc-language": "ru-ru"
              }
    pl = {"menu_id": "2",
          "page_num": 1,
          "page_size": 1000,
          "use_es": True,
          "filters": []
          }
    #with requests.Session() as session:
        #session.get(page_url)
    response = requests.post(page_url, data=json.dumps(pl))
    content = json.loads(response.text)
    #print(content)
    char_ids = [char['entry_page_id'] for char in content['data']['list']]
    #print(char_ids)
    birthdays = {}
    for id in char_ids:
        url = "https://sg-wiki-api-static.hoyolab.com/hoyowiki/wapi/entry_page?entry_page_id={}".format(id)
        char_info_en = parse_resp_json(url, 'en-us')
        char_info_ru = parse_resp_json(url, 'ru-ru')
        #print(char_info_ru)
        #print(char_info_ru["Имя:"], " ", char_info_en["Birthday"])
        try:
            name = char_info_ru["Имя"][2:-2]
            #print("ИМЯ: \n", char_info_ru["Имя"], "\nprocessed:", name)
            bday_split = char_info_en["Birthday"][2:-2].split("/")
            #print("BDAY: \n", char_info_en["Birthday"], "\nprocessed:", bday_split)
            bday = str(bday_split[1] + "." + bday_split[0])
            if bday in list(birthdays.keys()):
                birthdays[bday] = birthdays[bday].append(name)
            else:
                birthdays[bday] = [name]
        except (KeyError, IndexError):
            continue

    with open('birthdays.json', 'w') as f:
    # because of russian language the win-1251 encoding is used
        json.dump(birthdays, f, ensure_ascii=False)

except ValueError:
    print("Ой.")

