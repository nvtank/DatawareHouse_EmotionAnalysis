import pandas as pd
import random
import os
from datetime import datetime, timedelta
from pathlib import Path


# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
LABELS_DIR = BASE_DIR / "data" / "archive" / "YOLO_format" / "train" / "labels"

OUTPUT_FILE = BASE_DIR / 'data' / 'affectnet_processed_results.csv'
MAX_FILES_TO_PROCESS = 5000 

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
    """Simulate AI model output results"""
    emotion_list = list(EMOTION_MAP.values())
    
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
    print(f"Starting to read real annotation files from: {LABELS_DIR}")
    
    # Create output directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    results = []
    start_time = datetime(2025, 1, 1)
    
    try:
        all_files = [f for f in os.listdir(LABELS_DIR) if f.endswith('.txt')]
        print(f"Found {len(all_files)} annotation files.")
        

        files_to_process = all_files[:MAX_FILES_TO_PROCESS]
        print(f"Will process {len(files_to_process)} files...")

        for index, filename in enumerate(files_to_process):
            image_id = filename.replace('.txt', '.jpg') # Image filename
            filepath = os.path.join(str(LABELS_DIR), filename)
            
            with open(filepath, 'r') as f:
                line = f.readline().strip()
                if not line:
                    continue
                    
                # Read the first line (YOLO files usually have only 1 line)
                class_index = int(line.split()[0])
                true_emotion = EMOTION_MAP.get(class_index, "Unknown")
                
                if true_emotion == "Unknown":
                    continue
                
                # Simulate AI results
                pred_emotion, conf, val, aro, model = simulate_ai_results(true_emotion)
                
                # Simulate metadata
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

        # Convert results to DataFrame
        df_processed = pd.DataFrame(results)
        
        # Save to CSV file (used for Step 2)
        df_processed.to_csv(str(OUTPUT_FILE), index=False)
        
        print(f"\n--- SUCCESS! ---")
        print(f"Created file '{OUTPUT_FILE}' with {len(df_processed)} rows of REAL data (with simulated results).")

    except FileNotFoundError:
        print(f"Error: Directory '{LABELS_DIR}' not found.")
        print("Please check the path and update the LABELS_DIR variable.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_yolo_labels()