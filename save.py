import os
import psycopg2
import pandas as pd
import requests

db_config = {
    'host': 'postgres',     
    'port': 5432,
    'dbname': 'postgres',
    'user': 'airflow',
    'password': 'airflow'
}

df = pd.read_csv('cat_breeds.csv')

default_img = 'https://cdn2.thecatapi.com/images/aae.jpg'
df['image_url'] = df['image_url'].fillna(default_img)
df['image_url'] = df['image_url'].replace('nan', default_img)

df['temperament'] = df['temperament'].astype(str).str.strip()

image_dir = 'data/images'
os.makedirs(image_dir, exist_ok=True)

conn = psycopg2.connect(**db_config)
cur = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS trunghuu_cat (
    id TEXT PRIMARY KEY,
    name TEXT,
    origin TEXT,
    temperament TEXT,
    life_span TEXT,
    image_url TEXT
);
"""
cur.execute(create_table_query)
conn.commit()

insert_query = """
INSERT INTO trunghuu_cat (id, name, origin, temperament, life_span, image_url)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

for _, row in df.iterrows():
    cat_id = row['id']
    image_url = row['image_url']
    image_path = os.path.join(image_dir, f"{cat_id}.jpg")

    try:
        if not os.path.exists(image_path):
            img_response = requests.get(image_url, timeout=10)
            if img_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
            else:
                print(f"⚠️ Không tải được ảnh cho {cat_id}: {img_response.status_code}")
    except Exception as e:
        print(f"Lỗi khi tải ảnh {cat_id}: {e}")

    # --- Insert metadata ---
    cur.execute(insert_query, (
        row.get('id'),
        row.get('name'),
        row.get('origin'),
        row.get('temperament'),
        row.get('life_span'),
        row.get('image_url')
    ))

conn.commit()
cur.close()
conn.close()

print("Đã lưu metadata vào PostgreSQL và tải ảnh về thư mục data/images/")
