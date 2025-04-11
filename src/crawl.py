import requests
import json
url = "https://api.thecatapi.com/v1/breeds"

response = requests.get(url)

if response.status_code == 200:
    breeds_data = response.json()

    cat_breeds = []
    for breed in breeds_data:
        cat_info = {
            "id": breed.get("id", ""),
            "name": breed.get("name", ""),
            "origin": breed.get("origin", ""),
            "temperament": breed.get("temperament", ""),
            "life_span": breed.get("life_span", ""),
            "image_url": breed.get("image", {}).get("url", "")
        }
        cat_breeds.append(cat_info)

    with open("cat_breeds.json", "w", encoding='utf-8') as f_json:
        json.dump(cat_breeds, f_json, indent=4, ensure_ascii=False)

    print("Dữ liệu đã được lưu vào 'cat_breeds.json''")
else:
    print(f"Lỗi khi gọi API: {response.status_code}")
