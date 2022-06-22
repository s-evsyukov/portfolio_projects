CREATE MATERIALIZED VIEW yellow_taxi.view 
AS
SELECT /*+ MAPJOIN(p) */ p.name payment_type,
TO_DATE(tp.dt),
ROUND(AVG(tp.tip_amount), 2) tips_average_amount,
COUNT(*) passengers_total
FROM yellow_taxi.type_of_payment p
JOIN yellow_taxi.trip_part tp
ON p.id = tp.payment_type
GROUP BY p.name, to_date(tp.dt);