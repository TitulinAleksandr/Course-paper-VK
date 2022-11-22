import requests

import time

import json

from tqdm import tqdm

from pprint import pprint


class YandexDisk:
    
    host = 'https://cloud-api.yandex.net'
    
    def __init__(self, token):
        self.token = token
    
    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}
    
    def create_folder(self, path):
        upload_url = f'{self.host}/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.put(upload_url, headers=headers, params=params)
        return response

    def upload_file_to_disk(self, user_id, data):
        for var in tqdm(data):
            path = f"{user_id}/{var['file_name']}"
            url = var['url']
            upload_url = f'{self.host}/v1/disk/resources/upload'
            headers = self.get_headers()
            params = {'path': path, 'url': url}
            response = requests.post(upload_url, headers=headers, params=params)
            time.sleep(0.08)        
        print(f'Фотографии загружены на Яндекс Диск в папку {user_id}')
        return response.status_code

    def write_json(self, user_id, data):
        self.list_for_json = []
        for var in tqdm(data):
            json_dict = {'file_name': var['file_name'], 'size': var['size']}
            self.list_for_json.append(json_dict)
            with open(f'Фото профиля - {user_id}.json', 'w') as file:
                json.dump(self.list_for_json, file, indent=4)       
            time.sleep(0.03)            
        pprint(f'json-файл заргуженных фото: {self.list_for_json}')
        return self.list_for_json
    