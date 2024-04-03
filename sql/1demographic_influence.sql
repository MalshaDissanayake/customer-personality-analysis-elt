CREATE TABLE _demographic_influence AS
SELECT
    p.Marital_Status,
    p.Education,
    AVG(p.Income) AS avg_income,
    AVG(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS avg_spending
FROM
    People p
JOIN
    Products pr ON p.ID = pr.ID
GROUP BY
    p.Marital_Status,
    p.Education;
