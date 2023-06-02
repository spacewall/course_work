import json
import os
from datetime import date
from dotenv import dotenv_values
from ya_disk import YaUploader
import requests


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})

        return response.json()
   
    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        photo_data = list()

        if "img" not in os.listdir():
            os.mkdir("img")
        elif os.listdir("img") != []:
            for photo in os.listdir("img"):
                os.remove(f"img/{photo}")

        for item in response.json()['response']['items']:
            file_name = f"{item['likes']['count']}.jpg"
            binary_photo = requests.get(item['sizes'][-1]['url'])
            size = item['sizes'][-1]['type']

            if file_name in os.listdir("img"):
                file_name = f"{item['likes']['count']}_{date.fromtimestamp(item['date'])}.jpg"

            with open(f"img/{file_name}", 'wb') as photo:
                photo.write(binary_photo.content)

            photo_data.append({
                "file_name": file_name,
                "size": size
            })

        with open("result.json", 'w') as file:
            json.dump(photo_data, file, indent=4)


def main():
    config = dotenv_values(".env")
    access_token = config["VK_TOKEN"]
    disk_token = config["YA_TOKEN"]
    # user_id = "335149787"
    user_id = input('Введите id пользователя: ')

    vk = VK(access_token, user_id)
    vk.get_photos()

    print("# Фотографии получены, информация выведена в result.json")

    uploader = YaUploader(disk_token)
    print("# Начало загрузки на Яндекс.Диск…")
    for photo in os.listdir("img"):
        result = uploader.upload(f"img/{photo}")
    print("# Загрузка завершена!")

if __name__ == '__main__':
    main()
