Select 
symbol,
current_price,
ROUND(day_high,2) AS day_high,
ROUND(day_low,2) AS day_low,
ROUND(day_open,2) AS day_open,
change_amount,
ROUND(change_percent,4) AS change_percent,
makret_timestamp,
fetched_at 
FROM {{ ref('bronze_stg_stock_quotes') }}
where current_price IS NOT NULL