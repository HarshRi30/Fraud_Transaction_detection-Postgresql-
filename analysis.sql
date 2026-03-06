--Analysis Code For Fraud Detection System.


-- USERS WITH HIGHEST RISK SCORE AND MOST RISK HISTORY
SELECT DISTINCT(user_id), COUNT(*) OVER(PARTITION BY user_id), risk_score
FROM fraud_risk_report
ORDER BY risk_score DESC, 2 DESC;

-- USERS WHO LOST MOST OF THE MONEY WITH COUNT
SELECT DISTINCT(user_id), COUNT(*) OVER(PARTITION BY user_id), amount
FROM fraud_risk_report
ORDER BY amount DESC, 2 DESC;

--DEVICES WITH MOST FRAUD TRANSACTIONS
SELECT DISTINCT(device_id), COUNT(*) OVER(PARTITION BY device_id)
FROM fraud_risk_report
ORDER BY 2 DESC;

--LOCATION WITH MOST FRAUDS
SELECT DISTINCT(city), country , COUNT(*) OVER(PARTITION BY city)
FROM fraud_risk_report
ORDER BY 3 DESC;

--DATE WITH MOST FRAUDS
SELECT DISTINCT(DATE(transaction_date)), COUNT(*) OVER(PARTITION BY DATE(transaction_date))
FROM fraud_risk_report
ORDER BY 2 DESC;

--Time of Day
SELECT
    EXTRACT(HOUR FROM transaction_date) AS hour_of_day,
    COUNT(*) AS total_fraud_attempts,
    SUM(amount) AS amount_at_risk
FROM Fraud_Risk_Report
GROUP BY EXTRACT(HOUR FROM transaction_date)
ORDER BY total_fraud_attempts DESC;

--Targeted Categories
SELECT
    category,
    COUNT(*) as alert_count,
    ROUND(AVG(amount), 2) as average_fraud_transaction_value
FROM Fraud_Risk_Report
GROUP BY category
ORDER BY alert_count DESC;

--The Executive Summary
SELECT
    priority_level,
    COUNT(*) as total_cases,
    SUM(amount) as total_dollars_at_risk
FROM Fraud_Risk_Report
GROUP BY priority_level
ORDER BY
    CASE WHEN priority_level = 'CRITICAL' THEN 1
         WHEN priority_level = 'HIGH' THEN 2
         ELSE 3 END;

--Most Risky Users(Highest Total Risk & Total Money at Risk)
SELECT
    user_id,
    COUNT(transaction_id) as total_alerts,
    SUM(amount) as total_money_at_risk,
    MAX(risk_score) as highest_single_risk_score
FROM Fraud_Risk_Report
GROUP BY user_id
ORDER BY total_money_at_risk DESC, total_alerts DESC
LIMIT 10;


--Locations with the Most Fraud (Fraud Hotspots)
SELECT
    city,
    country,
    COUNT(transaction_id) as fraud_cases,
    SUM(amount) as total_amount_lost
FROM Fraud_Risk_Report
GROUP BY city, country
ORDER BY fraud_cases DESC
LIMIT 10;