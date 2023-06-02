import requests

class YaUploader:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"OAuth {token}",
            "Content-type": "application/json"
        }

    def get_link_to_upload(self, disk_file_path: str) -> str:
        """Метод возвращает ссылку на загрузку в диск"""
        headers = self.headers
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": disk_file_path, "overwrite": "true"}

        responce = requests.get(upload_url, headers=headers, params=params)
        
        return responce.json()
    
    def upload(self, file_path: str) -> None:
        """Метод загружает файлы по списку file_path на яндекс диск"""
        upload_url = self.get_link_to_upload(file_path.split("/")[1])["href"]

        with open(file_path, "rb") as file:
            src = file.read()

        responce = requests.put(upload_url, data=src)

        if responce.status_code == 201:
            file_name = file_path.split("/")[1]
            print(f"# {file_name} загружен успешно")
