SELECT
    image_id,
    capture_timestamp,
    subject_id_anon,
    model_version_name,
    true_emotion,
    predicted_emotion,
    confidence_score,
    predicted_valence_score,
    predicted_arousal_score,
    
    -- Tạo một cột mới (chỉ số): 1 nếu dự đoán đúng, 0 nếu sai
    CASE
        WHEN true_emotion = predicted_emotion THEN 1
        ELSE 0
    END AS is_correct_prediction

FROM {{ source('public', 'stg_affectnet_raw') }}
WHERE 
    true_emotion IS NOT NULL 
    AND predicted_emotion IS NOT NULL