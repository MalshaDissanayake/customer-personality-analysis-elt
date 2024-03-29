CREATE TABLE _high_spend_customer_segments AS
SELECT
    p.Marital_Status,
    p.Education,
    p.Kidhome,
    p.Teenhome,
    AVG(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS avg_spending
FROM
    People p
JOIN
    Products pr ON p.ID = pr.ID
GROUP BY
    p.Marital_Status,
    p.Education,
    p.Kidhome,
    p.Teenhome;
