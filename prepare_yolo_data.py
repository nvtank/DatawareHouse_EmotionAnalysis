import pandas as pd
import random
import os
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
# !! QUAN TRỌNG: 
# !! 1. TÌM THƯ MỤC 'labels' CỦA BẠN (ví dụ: .../train/labels)
# !! 2. DÁN ĐƯỜNG DẪN ĐÓ VÀO BIẾN LABELS_DIR DƯỚI ĐÂY
LABELS_DIR = "/home/nvtank/year3/ki1/kdl/datawarehouse/data/archive/YOLO_format/train/labels" 

OUTPUT_FILE = 'data/affectnet_processed_results.csv'
MAX_FILES_TO_PROCESS = 5000 # Giới hạn 5000 file để chạy thử
# --- KẾT THÚC CẤU HÌNH ---

# Ánh xạ class (từ file data.yaml của bạn)
EMOTION_MAP = {
    0: "Anger",
    1: "Contempt",
    2: "Disgust",
    3: "Fear",
    4: "Happy",
    5: "Neutral",
    6: "Sad",
    7: "Surprise"
}

def simulate_ai_results(true_emotion):
    """Giả lập kết quả đầu ra của mô hình AI"""
    emotion_list = list(EMOTION_MAP.values())
    
    # 30% mô hình dự đoán sai
    if random.random() < 0.3: 
        predicted_emotion = random.choice([e for e in emotion_list if e != true_emotion])
    else:
        predicted_emotion = true_emotion
        
    confidence = random.uniform(0.6, 0.99)
    valence = random.uniform(-1.0, 1.0)
    arousal = random.uniform(-1.0, 1.0)
    model_version = random.choice(['V1_ResNet', 'V1_MobileNet'])
    
    return predicted_emotion, confidence, valence, arousal, model_version

def process_yolo_labels():
    print(f"Bắt đầu đọc file annotation thật từ: {LABELS_DIR}")
    
    results = []
    start_time = datetime(2025, 1, 1)
    
    try:
        all_files = [f for f in os.listdir(LABELS_DIR) if f.endswith('.txt')]
        print(f"Tìm thấy {len(all_files)} file annotation.")
        
        # Giới hạn số lượng file để chạy nhanh
        files_to_process = all_files[:MAX_FILES_TO_PROCESS]
        print(f"Sẽ xử lý {len(files_to_process)} file...")

        for index, filename in enumerate(files_to_process):
            image_id = filename.replace('.txt', '.jpg') # Tên file ảnh
            filepath = os.path.join(LABELS_DIR, filename)
            
            with open(filepath, 'r') as f:
                line = f.readline().strip()
                if not line:
                    continue
                    
                # Đọc dòng đầu tiên (file YOLO thường chỉ có 1 dòng)
                class_index = int(line.split()[0])
                true_emotion = EMOTION_MAP.get(class_index, "Unknown")
                
                if true_emotion == "Unknown":
                    continue
                
                # Giả lập kết quả AI
                pred_emotion, conf, val, aro, model = simulate_ai_results(true_emotion)
                
                # Giả lập metadata
                timestamp = start_time + timedelta(seconds=index)
                subject_id = f"Sub_{random.randint(1, 500)}"
                age_group = random.choice(['20-30', '30-40', '40-50'])
                
                results.append({
                    'image_id': image_id,
                    'capture_timestamp': timestamp,
                    'subject_id_anon': subject_id,
                    'model_version_name': model,
                    'true_emotion': true_emotion,
                    'predicted_emotion': pred_emotion,
                    'predicted_valence_score': val,
                    'predicted_arousal_score': aro,
                    'confidence_score': conf,
                    'age_group': age_group
                })

        # Chuyển kết quả thành DataFrame
        df_processed = pd.DataFrame(results)
        
        # Lưu ra file CSV (file này sẽ được dùng cho Bước 2)
        df_processed.to_csv(OUTPUT_FILE, index=False)
        
        print(f"\n--- THÀNH CÔNG! ---")
        print(f"Đã tạo file '{OUTPUT_FILE}' với {len(df_processed)} dòng dữ liệu THẬT (đã mô phỏng kết quả).")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy thư mục '{LABELS_DIR}'.")
        print("Vui lòng kiểm tra lại đường dẫn và cập nhật biến LABELS_DIR.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    process_yolo_labels()