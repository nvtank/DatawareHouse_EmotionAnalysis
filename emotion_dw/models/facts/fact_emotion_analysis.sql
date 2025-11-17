SELECT
    MD5(t1.subject_id_anon) AS subject_key,
    MD5(t1.true_emotion) AS emotion_key,
    MD5(t1.model_version_name) AS model_key,
    CAST(TO_CHAR(t1.capture_timestamp, 'YYYYMMDD') AS INTEGER) AS date_key,

    t1.confidence_score,
    t1.is_correct_prediction,
    t1.predicted_valence_score AS predicted_valence, 
    t1.predicted_arousal_score AS predicted_arousal,
    1 AS analysis_count 

FROM {{ ref('stg_emotion_features') }} t1