import requests

class YandexDisk:
    host = 'https://cloud-api.yandex.net'
    def __init__(self, token):
        self.token = token
    
    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
    
    def create_folder(self, path):
        upload_url = f'{self.host}/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.put(upload_url, headers=headers, params=params)
        return response

    def upload_file_to_disk(self, path, url):
        upload_url = f'{self.host}/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': path, 'url': url}
        response = requests.post(upload_url, headers=headers, params=params)
        return response 
