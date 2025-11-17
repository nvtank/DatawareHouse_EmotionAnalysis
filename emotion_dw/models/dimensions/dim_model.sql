SELECT DISTINCT
    MD5(model_version_name) AS model_key,
    model_version_name,
    -- Giả định kiến trúc mô hình dựa trên tên
    CASE 
        WHEN model_version_name LIKE '%ResNet%' THEN 'ResNet'
        WHEN model_version_name LIKE '%MobileNet%' THEN 'MobileNet'
        ELSE 'Unknown'
    END AS architecture
FROM {{ ref('stg_emotion_features') }}