import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys

# Tải các biến môi trường từ file .env
load_dotenv()

def get_db_url():
    """Tạo URL kết nối database từ file .env"""
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    db = os.getenv('POSTGRES_DB')
    
    if not all([user, password, host, port, db]):
        print("Lỗi: Một vài biến môi trường (.env) bị thiếu.")
        sys.exit(1)
        
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def load_data_to_db():
    """Hàm chính: Đọc CSV và Tải vào PostgreSQL"""
    
    db_url = get_db_url()
    file_path = 'data/affectnet_processed_results.csv'
    table_name = 'stg_affectnet_raw' # Tên bảng Staging (thô)
    
    try:
        # 1. Extract (Đọc file CSV)
        print(f"Đang đọc dữ liệu từ {file_path}...")
        df = pd.read_csv(file_path)
        
        # 2. Xử lý nhỏ: Đảm bảo timestamp là kiểu datetime
        df['capture_timestamp'] = pd.to_datetime(df['capture_timestamp'])
        print(f"Đã đọc {len(df)} dòng dữ liệu.")

        # 3. Load (Tải vào PostgreSQL)
        print(f"Đang kết nối tới database {os.getenv('POSTGRES_DB')}...")
        engine = create_engine(db_url)
        
        print(f"Đang tải dữ liệu vào bảng '{table_name}' (Schema: public)...")
        # if_exists='replace': Xóa bảng cũ nếu tồn tại và tạo bảng mới
        df.to_sql(table_name, engine, if_exists='replace', index=False, schema='public')
        
        print("\n--- THÀNH CÔNG! ---")
        print(f"Dữ liệu đã được tải thành công vào bảng '{table_name}'.")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file CSV tại '{file_path}'.")
    except Exception as e:
        print(f"Lỗi trong quá trình E/L: {e}")

if __name__ == "__main__":
    load_data_to_db()