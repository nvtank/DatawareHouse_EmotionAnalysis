# 🚀 Emotion Analysis Data Warehouse

This project builds a complete **Data Warehouse** for facial emotion analysis.

The entire **ELT (Extract, Load, Transform) + Visualization** pipeline is implemented from start to finish:

- **Extract**: Read raw data (.txt files) from the AffectNet dataset (YOLO format) and simulate AI results using Python.
- **Load**: Load processed data into PostgreSQL (staging table).
- **Transform**: Use DBT to run SQL models, clean and transform raw data into a **Star Schema** (1 Fact Table, 4 Dimension Tables).
- **Visualization**:
  - **Business Intelligence (BI)** analysis through an interactive Dashboard using Streamlit.
  - **Technical Analysis (Lineage)** through DBT Docs.

---

## 🛠️ Technologies Used

- **Database**: PostgreSQL (running via Docker)
- **Data Transformation**: DBT (dbt-postgres)
- **ELT & Web App**: Python 3
  - `pandas`, `sqlalchemy`, `psycopg2-binary` (for E/L)
  - `streamlit` (for Dashboard)
  - `python-dotenv` (environment variable management)

---

## 🏗️ Project Structure

```
DataWarehouse_EmotionAnalysis/
│
├── .venv/                   # Python virtual environment
├── data/
│   ├── archive/
│   │   └── YOLO_format/     # Raw AffectNet dataset (with train/labels)
│   └── affectnet_processed_results.csv  # Output from preparation script
│
├── emotion_dw/              # DBT Project (Phase 2 - Transform)
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_emotion_features.sql
│   │   ├── dimensions/
│   │   │   ├── dim_emotion.sql
│   │   │   ├── dim_model.sql
│   │   │   ├── dim_subject.sql
│   │   │   └── dim_time.sql
│   │   ├── facts/
│   │   │   └── fact_emotion_analysis.sql
│   │   └── sources.yml
│   └── dbt_project.yml
│
├── app.py                   # Streamlit Dashboard Script (Phase 3)
├── load_affectnet.py        # Python Script (Phase 1 - Load)
├── prepare_yolo_data.py     # Python Script (Phase 1 - Extract)
├── .env                     # Environment variables file (MUST CREATE)
├── .gitignore               # Ignore unnecessary files
└── README.md                # This file
```

---

## ⚙️ Installation & Running Guide

### 1. Environment Setup

```bash
# 1. Clone this project
git clone <your-repo-url>
cd DataWarehouse_EmotionAnalysis

# 2. Start Database (running with Docker)
docker run --name emotion-db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=emotion_dw \
  -p 5432:5432 \
  -d postgres

# 3. Create .env file in the root directory with the following content
cat > .env << EOF
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=emotion_dw
EOF

# 4. Create Python virtual environment
python -m venv .venv

# 5. Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows

# 6. Install all required Python packages
pip install pandas sqlalchemy psycopg2-binary dbt-postgres python-dotenv streamlit

# 7. Configure DBT (it will ask for database information)
# Run this command, select [1] postgres and enter information from .env file
dbt init emotion_dw
# (If you already have emotion_dw directory, ensure your ~/.dbt/profiles.yml is correct)
```

### 2. Running the Pipeline (Required Order)

> **IMPORTANT NOTE**: Always ensure you have activated the virtual environment (`source .venv/bin/activate`) before running any commands.

#### **Step 1: Prepare Data (Extract)**

Read .txt files from `data/archive/YOLO_format/train/labels` and create `affectnet_processed_results.csv`.

```bash
python prepare_yolo_data.py
```

**Expected Output:**
```
Starting to read real annotation files from: /path/to/data/archive/YOLO_format/train/labels
Found XXXX annotation files.
Will process 5000 files...

--- SUCCESS! ---
Created file 'data/affectnet_processed_results.csv' with 5000 rows of REAL data (with simulated results).
```

#### **Step 2: Load Data into Database (Load)**

Load `affectnet_processed_results.csv` into the `stg_affectnet_raw` table in PostgreSQL.

```bash
python load_affectnet.py
```

**Expected Output:**
```
Reading data from data/affectnet_processed_results.csv...
Read 5000 rows of data.
Connecting to database emotion_dw...
Loading data into table 'stg_affectnet_raw' (Schema: public)...

--- SUCCESS! ---
Data has been successfully loaded into table 'stg_affectnet_raw'.
```

#### **Step 3: Transform Data (Transform)**

Run all DBT models to build the Star Schema (Staging, Dimensions, Fact).

```bash
# Navigate to DBT directory
cd emotion_dw

# Run all models
dbt run

# Return to root directory
cd ..
```

**Expected Output:**
```
Running with dbt=1.x.x
Found 6 models, 0 tests, 0 snapshots, 0 analyses, ...

Completed successfully

Done. PASS=6 WARN=0 ERROR=0 SKIP=0 TOTAL=6
```

---

## 📊 Viewing the Results

You have 2 ways to view the results:

### 1. View Analytics Dashboard (Streamlit)

This shows business intelligence (BI) analysis, model performance charts, and Valence/Arousal analysis.

```bash
# (Ensure you're in the root directory DataWarehouse_EmotionAnalysis)
streamlit run app.py
```

- Open your browser and visit: **http://localhost:8501**

**Dashboard Features:**
- 📊 **Model Performance**: Correct/Incorrect prediction ratio
- 🎯 **Accuracy by Model**: Compare V1_ResNet vs V1_MobileNet
- 🌈 **Emotion Space Analysis**: Valence/Arousal scatter plot colored by emotion

### 2. View Data Lineage Graph (DBT Docs)

This shows the technical structure of the data warehouse and how tables (Fact/Dimension) are connected.

```bash
# 1. Navigate to DBT directory
cd emotion_dw

# 2. Generate documentation
dbt docs generate

# 3. Serve documentation
dbt docs serve
```

- Open your browser and visit: **http://127.0.0.1:8080/**
- Click on `fact_emotion_analysis` in the left sidebar
- Click the blue graph button 🟢 in the bottom right corner to view the lineage graph

---

## 📐 Data Warehouse Schema

### Star Schema Design

```
                    ┌─────────────────┐
                    │   dim_emotion   │
                    │  (emotion_key)  │
                    └────────┬────────┘
                             │
    ┌─────────────────┐      │      ┌─────────────────┐
    │   dim_subject   │      │      │   dim_model     │
    │  (subject_key)  │      │      │   (model_key)   │
    └────────┬────────┘      │      └────────┬────────┘
             │                │               │
             │     ┌──────────▼──────────┐    │
             └─────►  fact_emotion_       ◄────┘
                   │     analysis        │
                   │  (FACT TABLE)       │
                   └──────────▲──────────┘
                              │
                    ┌─────────┴────────┐
                    │    dim_time      │
                    │   (date_key)     │
                    └──────────────────┘
```

### Table Descriptions

**Fact Table:**
- `fact_emotion_analysis`: Contains all emotion analysis measurements and metrics

**Dimension Tables:**
1. `dim_emotion`: Emotion categories (Anger, Happy, Sad, etc.)
2. `dim_model`: AI model versions (V1_ResNet, V1_MobileNet)
3. `dim_subject`: Subject demographics (age groups)
4. `dim_time`: Time dimension (date, day of week, etc.)

---

## 🎯 Key Features

### 1. **Complete ELT Pipeline**
- Extract from raw YOLO format annotations
- Load into PostgreSQL staging area
- Transform into optimized Star Schema using DBT

### 2. **Flexible Configuration**
- Uses relative paths - works on any machine
- Environment variables via `.env` file
- No hardcoded paths or credentials

### 3. **Data Quality**
- Simulates realistic AI model predictions (30% error rate)
- Includes confidence scores, valence, and arousal metrics
- Proper datetime handling and data type validation

### 4. **Interactive Visualization**
- Real-time dashboard with Streamlit
- Model performance comparison
- Emotion space visualization (Valence/Arousal)

### 5. **Technical Documentation**
- Automated lineage graph generation
- Table-level documentation
- Column-level descriptions

---

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check if Docker container is running
docker ps

# Check PostgreSQL logs
docker logs emotion-db

# Restart container if needed
docker restart emotion-db
```

### DBT Issues
```bash
# Test database connection
cd emotion_dw
dbt debug

# Clean and rebuild everything
dbt clean
dbt run
```

### Python Package Issues
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall packages
pip install --upgrade -r requirements.txt
```

---

## 📝 Configuration Files

### `.env` File Structure
```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=emotion_dw
```

### DBT Profile (`~/.dbt/profiles.yml`)
```yaml
emotion_dw:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: admin
      password: admin
      port: 5432
      dbname: emotion_dw
      schema: public
      threads: 4
```

---

## 📚 Dataset Information

This project uses the **AffectNet dataset** in YOLO format:
- **8 emotion categories**: Anger, Contempt, Disgust, Fear, Happy, Neutral, Sad, Surprise
- **Annotation format**: YOLO text files with class indices
- **Processing limit**: 5000 files for quick processing (configurable in `prepare_yolo_data.py`)

---

## 🚀 Future Enhancements

- [ ] Add more sophisticated AI model predictions
- [ ] Implement real-time data streaming
- [ ] Add more dashboard visualizations
- [ ] Include statistical tests and metrics
- [ ] Add data quality tests with dbt tests
- [ ] Implement incremental loading strategies
- [ ] Add API endpoints for data access

---
