import json
import time
from pprint import pprint
from tqdm import tqdm
from yadisk import YandexDisk
from vk_class import VK
if __name__ == '__main__':
    with open('vktoken.txt', 'r') as file:
        token = file.read().strip()
    user_id = str(input('Введите ID профиля ВКонтаке: '))
    vk = VK(user_id, token)
    photos = vk.photos_list()
    
    # with open('tokenya.txt', 'r') as file:
    #     token = file.read().strip()
    vasya = YandexDisk(input('Введите токен с Полигона Яндекс.Диска:\n'))
    vasya.create_folder(user_id)
    list_for_json = [] # Список для записи в json-файл
    for photo in tqdm(photos):
        path = f"{user_id}/{photo['file_name']}"
        url = photo['url']
        vasya.upload_file_to_disk(path, url)
        json_dict = {'file_name': photo['file_name'], 'size': photo['size']}
        list_for_json.append(json_dict)
        with open(f'Фото профиля - {user_id}.json', 'w') as file:
            json.dump(list_for_json, file, indent=4)    
        time.sleep(0.08)    
    pprint(f'json-файл заргуженных фото: {list_for_json}')
    print(f'Фотографии загружены на Яндекс Диск в папку {user_id}')    