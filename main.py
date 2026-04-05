import json
import requests
from tqdm import tqdm


YANDEX_API_URL = "https://cloud-api.yandex.net/v1/disk/resources"
CATAAS_API_URL = "https://cataas.com/cat/says"


def get_cat_image_url(text):
    response = requests.get(f"{CATAAS_API_URL}/{text}?json=true")
    data = response.json()
    return f"https://cataas.com{data['url']}"


def get_file_size(url):
    response = requests.head(url)
    size_bytes = response.headers.get("Content-Length", 0)
    return round(int(size_bytes) / 1024, 2)


def create_folder(token, folder_name):
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": folder_name}
    requests.put(YANDEX_API_URL, headers=headers, params=params)


def upload_file_to_yadisk(token, file_url, disk_path):
    headers = {"Authorization": f"OAuth {token}"}
    params = {
        "path": disk_path,
        "url": file_url
    }

    requests.post(
        f"{YANDEX_API_URL}/upload",
        headers=headers,
        params=params
    )


def main():
    token = input("Введите токен Яндекс.Диска: ")
    text = input("Введите текст для картинки: ")
    folder_name = input("Введите название вашей группы Нетологии: ")

    create_folder(token, folder_name)

    result = []

    for i in tqdm(range(5), desc="Загрузка"):
        image_url = get_cat_image_url(text)
        file_size = get_file_size(image_url)

        file_name = f"{text}_{i + 1}.jpg"
        disk_path = f"{folder_name}/{file_name}"

        upload_file_to_yadisk(token, image_url, disk_path)

        result.append({
            "file_name": file_name,
            "size_kb": file_size
        })

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("Готово! Картинки загружены на Яндекс.Диск.")


if __name__ == "__main__":
    main()