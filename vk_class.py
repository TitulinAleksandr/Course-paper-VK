import requests
import time

class VK:
    url = 'https://api.vk.com/method/'
    def __init__(self, user_id, token, version=5.131):
        self.params = {'owner_id': user_id, 'access_token': token, 'v': version}
    def photos_get(self):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {'album_id': 'profile', 'extended': '1', 'photo_sizes': True}
        response = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        print(f"В заданом профиле содержится {len(response['response']['items'])} фотографий.\nПо умолчанию будет загружено 5 штук.\nЖелаете загрузить другое количество? Да/Нет")
        user_input = input().lower()
        if user_input == 'нет':
            param = {'count': '5'}
            photos_get_params.update(param)
            response = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        elif user_input == 'да':
            get_number_photo = str(input(f'Введите количество фотографий для загрузки: '))
            param = {'count': get_number_photo}
            photos_get_params.update(param)
            response = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        else:
            print('Введите корректные данные.')
        return response
    
    def _max_size(self, size_dict): # Определяем максимальный размер
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']
    def _strftime(self, timestamp, format_string='%Y-%m-%d'): # Перевод даты с формата unix в читаемый для пользователя вид
        return time.strftime(format_string, time.localtime(timestamp))
    
    def photos_list(self):
        self.photos_list = [] # Список словарей с данными по фото для дальнейшей работы(определён максимальный размер, дата и т.д.)
        self.json_list = [] # Готовый список для загрузки фото на Ядиск и записи в json - файл 
        self.count_list = [] # Список технический для создания имени файла (лайки-дата загрузки) при повторении
        photos = self.photos_get()['response']['items']    
        for photo in photos: # Цикл для обработки полученных данных с сервиса ВК
            date = self._strftime(photo['date'])
            photo_dict = {'file_name': str(photo['likes']['count']), 'url_photo': None, 'size': None, 'date': date}
            sizes = photo['sizes']
            max_size = max(sizes, key=self._max_size)
            photo_dict['url_photo'] =  max_size['url']
            photo_dict['size'] = max_size['type']
            self.photos_list.append(photo_dict)
        for photo_dict in self.photos_list: # Цикл для записи self.json_list
            dict_ = {}
            if photo_dict.get('file_name') not in self.count_list:
                dict_ = {'file_name': f"{photo_dict['file_name']}.jpg", 'size': photo_dict['size'], 'url': photo_dict['url_photo']} 
                self.json_list.append(dict_)
                self.count_list.append(photo_dict['file_name'])
            else:
                dict_ = {'file_name': f"{photo_dict['file_name']}-{photo_dict['date']}.jpg", 'size': photo_dict['size'], 'url': photo_dict['url_photo']} 
                self.json_list.append(dict_)
        return self.json_list
       
    
