SELECT DISTINCT
    -- Tạo khóa chính (Key) kiểu INTEGER để Join nhanh hơn
    CAST(TO_CHAR(capture_timestamp, 'YYYYMMDD') AS INTEGER) AS date_key, 
    DATE(capture_timestamp) AS date_actual,
    EXTRACT(YEAR FROM capture_timestamp) AS year,
    EXTRACT(MONTH FROM capture_timestamp) AS month,
    TO_CHAR(capture_timestamp, 'Month') AS month_name,
    EXTRACT(DAY FROM capture_timestamp) AS day_of_month,
    EXTRACT(DOW FROM capture_timestamp) AS day_of_week_num,
    TO_CHAR(capture_timestamp, 'Day') AS day_of_week_name
    
FROM {{ ref('stg_emotion_features') }}