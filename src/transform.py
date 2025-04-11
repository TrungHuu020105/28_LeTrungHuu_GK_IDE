import requests
import csv

url = 'https://api.thecatapi.com/v1/breeds'
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    breeds = response.json()
    data = []
    
    for breed in breeds:
        breed_id = breed.get('id', '')
        name = breed.get('name', '')
        origin = breed.get('origin', '')
        temperament = breed.get('temperament', '')
        life_span = breed.get('life_span', '')
        
        image_url = breed.get('image', {}).get('url', '')
        if not image_url:
            image_response = requests.get(f'https://api.thecatapi.com/v1/images/search?breed_id={breed_id}', headers=headers)
            if image_response.status_code == 200 and image_response.json():
                image_url = image_response.json()[0].get('url', '')
        
        data.append([breed_id, name, origin, temperament, life_span, image_url])
        
        print(f"ID: {breed_id}")
        print(f"Tên: {name}")
        print(f"Nguồn gốc: {origin}")
        print(f"Đặc tính: {temperament}")
        print(f"Tuổi thọ: {life_span}")
        print(f"Link ảnh: {image_url}")
        print("-" * 40)
    
    with open('cat_breeds.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'origin', 'temperament', 'life_span', 'image_url'])
        writer.writerows(data)
    
    print("Dữ liệu đã được lưu vào cat_breeds.csv")
else:
    print("Lỗi khi lấy dữ liệu từ API, mã lỗi:", response.status_code)