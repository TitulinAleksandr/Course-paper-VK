import configparser

from yadisk import YandexDisk

from vk_class import VK


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    token = config['vk_token']['vktoken']
    user_id = str(input('Введите ID профиля ВКонтаке: '))
    
    vk = VK(user_id, token)
    data = vk.photos_list()
    
    user = YandexDisk(input('Введите токен с Полигона Яндекс.Диска:\n'))
    user.create_folder(user_id)
    user.upload_file_to_disk(user_id, data)
    user.write_json(user_id, data)
