SELECT DISTINCT
    MD5(subject_id_anon) AS subject_key,
    subject_id_anon,
    age_group
FROM {{ ref('stg_emotion_features') }}