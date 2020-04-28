import requests
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(text, to_lang):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """
    file_name = input("Введите имя файла для перевода из имеющихся: ")

    new_file_name = file_name[:2] + "-RU." + file_name[3:]

    with open(file_name, encoding="utf-8") as f:
        data = f.read()
        # print(data)

    params = {
        'key': API_KEY,
        'text': data,
        'lang': 'ru',
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    
    with open(new_file_name, 'w', encoding="utf-8") as f:
        b = json_['text']
        for element in b:
            f.write(element)

    headers = {"Authorization": "OAuth AgAAAAAp25VPAADLWxVyTv1sVkOppvnWwL3HS88"}
    params = {'path': new_file_name, 'overwrite': 'True'}

    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)
    # print(response.json())
    send_url = response.json()['href']
    # print(send_url)
    files = {'file': open(new_file_name, 'rb')}
    requests.put(send_url, files=files)

    return ''.join(json_['text'])


# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
    print(translate_it('text', 'ru'))
