import requests

import time


class VK:
    
    url = 'https://api.vk.com/method/'
    
    def __init__(self, user_id, token, version=5.131):
        self.params = {'owner_id': user_id, 'access_token': token, 'v': version}
    
    def photos_get(self):
        get_url = self.url + 'photos.get'
        get_params = {'album_id': 'profile', 'extended': '1', 'photo_sizes': True}
        respons = requests.get(get_url, params={**self.params, **get_params}).json()
        print('В заданом профиле содержится', len(respons['response']['items']),
              'фотографий.\n'
              'По умолчанию будет загружено 5 штук.\n'
              'Желаете загрузить другое количество? Да/Нет'
              )
        user_input = input().lower()
        if user_input == 'нет':
            param = {'count': '5'}
            get_params.update(param)
            response = requests.get(get_url, params={**self.params, **get_params}).json()
        elif user_input == 'да':
            get_number_photo = str(input(f'Введите количество фотографий для загрузки: '))
            param = {'count': get_number_photo}
            get_params.update(param)
            response = requests.get(get_url, params={**self.params, **get_params}).json()
        else:
            print('Введите корректные данные.')
        return response
    
    def _max_size(self, size_dict): 
        '''Auxiliary function for determining 
           maximum photo size'''
        
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']
    
    def _strftime(self, timestamp, format_string='%Y-%m-%d'):
        return time.strftime(format_string, time.localtime(timestamp))
    
    def photos_list(self):
        self.photos_list = []
        self.json_list = []
        self.count_list = []
        photos = self.photos_get()['response']['items']  
        
        '''A loop for creating a list of received data from the VK service,
           sorted (maximum size, date, url) for further processing'''
        for photo in photos:
            date = self._strftime(photo['date'])
            photo_dict = {'file_name': str(photo['likes']['count']),
                          'url_photo': None, 'size': None, 'date': date}
            sizes = photo['sizes']
            max_size = max(sizes, key=self._max_size)
            photo_dict['url_photo'] =  max_size['url']
            photo_dict['size'] = max_size['type']
            self.photos_list.append(photo_dict)
        
        '''A loop for creating a list with the necessary names,
           file sizes for uploading photos to YADisk and writing to a json-file'''
        for photo_dict in self.photos_list:
            dict_ = {}
            if photo_dict.get('file_name') not in self.count_list:
                dict_ = {'file_name': f"{photo_dict['file_name']}.jpg",
                         'size': photo_dict['size'], 'url': photo_dict['url_photo']} 
                self.json_list.append(dict_)
                self.count_list.append(photo_dict['file_name'])
            else:
                dict_ = {'file_name': f"{photo_dict['file_name']}-{photo_dict['date']}.jpg",
                         'size': photo_dict['size'], 'url': photo_dict['url_photo']} 
                self.json_list.append(dict_)
        return self.json_list
