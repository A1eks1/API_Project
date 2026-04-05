import requests
import json
import time
from tqdm import tqdm


class CataasToYandex:
    def __init__(self, ya_token, group_name):
        self.ya_token = ya_token
        self.group_name = group_name
        self.base_ya_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Authorization": f"OAuth {self.ya_token}"
        }

    def create_folder(self):
        params = {"path": self.group_name}
        response = requests.put(self.base_ya_url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f"Папка '{self.group_name}' успешно создана.")
        elif response.status_code == 409:
            print(f"Папка '{self.group_name}' уже существует.")
        return response.status_code

    def get_cat_url(self, text):
        return f"https://cataas.com/cat/says/{text}"

    def upload_to_disk(self, text):
        cat_url = self.get_cat_url(text)
        upload_url = f"{self.base_ya_url}/upload"

        file_path = f"{self.group_name}/{text}.jpg"

        params = {
            "path": file_path,
            "url": cat_url
        }

        response = requests.post(upload_url, headers=self.headers, params=params)

        if response.status_code == 202:
            time.sleep(2)
            meta_params = {"path": file_path}
            meta_res = requests.get(self.base_ya_url, headers=self.headers, params=meta_params).json()

            return {
                "file_name": f"{text}.jpg",
                "size": meta_res.get("size", "unknown")
            }
        return None


def main():

    text_input = input("Введите текст для картинки: ")
    ya_token = input("Введите ваш Яндекс.Диск токен: ")
    group_name = "PYAPI-146"  

    uploader = CataasToYandex(ya_token, group_name)
    uploader.create_folder()

    results = []

    print("Начинаю загрузку...")
    for _ in tqdm(range(1), desc="Загрузка котика"):
        info = uploader.upload_to_disk(text_input)
        if info:
            results.append(info)

    with open("upload_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("\nЗагрузка завершена. Информация сохранена в upload_results.json")


if __name__ == "__main__":
    main()
