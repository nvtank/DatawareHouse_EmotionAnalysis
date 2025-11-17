SELECT DISTINCT
    -- Dùng MD5 để tạo khóa chính (Primary Key) duy nhất
    MD5(true_emotion) AS emotion_key, 
    true_emotion AS emotion_name,
    'Discrete' AS emotion_type,
    

    CASE true_emotion 
        WHEN 'Happy' THEN 0.8 
        WHEN 'Sad' THEN -0.6 
        WHEN 'Angry' THEN -0.5 
        WHEN 'Fear' THEN -0.7
        WHEN 'Surprise' THEN 0.6
        WHEN 'Disgust' THEN -0.6
        WHEN 'Contempt' THEN -0.4
        ELSE 0 
    END AS valence_benchmark,
    
    CASE true_emotion 
        WHEN 'Happy' THEN 0.7 
        WHEN 'Sad' THEN -0.5 
        WHEN 'Angry' THEN 0.8 
        WHEN 'Fear' THEN 0.7
        WHEN 'Surprise' THEN 0.8
        WHEN 'Disgust' THEN -0.3
        WHEN 'Contempt' THEN -0.1
        ELSE 0 
    END AS arousal_benchmark
    
FROM {{ ref('stg_emotion_features') }} 