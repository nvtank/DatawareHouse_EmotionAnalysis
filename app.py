import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys


load_dotenv()

@st.cache_data
def get_db_url():
    """Create database connection URL from .env file"""
 
    user = os.getenv('POSTGRES_USER') 
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    db = os.getenv('POSTGRES_DB')
    
    if not all([user, password, host, port, db]):
        print(f"DEBUG: USER={user}, PASS={bool(password)}, HOST={host}, PORT={port}, DB={db}")
        st.error("Error: Some environment variables (.env) are missing. Please check the .env file and restart the app.")
        sys.exit(1)
        
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

#  Connect to DB -
try:
    DB_URL = get_db_url()
    engine = create_engine(DB_URL)
except Exception as e:
    st.error(f"Database connection error: {e}")
    sys.exit()

st.set_page_config(page_title="Emotion Analysis Dashboard", layout="wide")
st.title("📊 Emotion Analysis Dashboard")

@st.cache_data
def load_data():
    """Query data from DW by joining Fact and Dimensions"""
    query = """
    SELECT
        f.confidence_score,
        f.is_correct_prediction,
        f.predicted_valence,
        f.predicted_arousal,
        
        d_emo.emotion_name,
        d_emo.valence_benchmark,
        d_emo.arousal_benchmark,
        d_sub.age_group,
        d_mod.model_version_name AS model_name,
        d_time.date_actual,
        d_time.day_of_week_name
        
    FROM fact_emotion_analysis AS f
    
    LEFT JOIN dim_emotion AS d_emo ON f.emotion_key = d_emo.emotion_key
    LEFT JOIN dim_subject AS d_sub ON f.subject_key = d_sub.subject_key
    LEFT JOIN dim_model AS d_mod ON f.model_key = d_mod.model_key
    LEFT JOIN dim_time AS d_time ON f.date_key = d_time.date_key
    
    LIMIT 1000;
    """
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error querying Data Warehouse: {e}")
        return pd.DataFrame() # Return empty DataFrame

df = load_data()

if not df.empty:
    st.header("Model Performance")

    #  Bar chart: Correct/Incorrect ratio
    correct_counts = df['is_correct_prediction'].value_counts().rename({1: 'Correct', 0: 'Incorrect'})
    st.bar_chart(correct_counts)

    #  Analysis by Model
    st.subheader("Accuracy by Model")
    accuracy_by_model = df.groupby('model_name')['is_correct_prediction'].mean()
    st.dataframe(accuracy_by_model.map(lambda x: f"{x:.2%}"))

    st.header("Emotion Space Analysis (Valence/Arousal)")
    # Scatter plot
    st.scatter_chart(
        df,
        x='predicted_valence',
        y='predicted_arousal',
        color='emotion_name'
    )
else:
    st.warning("Could not load data from Data Warehouse. Dashboard cannot be displayed.")
