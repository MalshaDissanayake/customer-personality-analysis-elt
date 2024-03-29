-- Discount Purchases vs. Overall Spending
CREATE TABLE _discount_purchases_vs_spending AS
SELECT
    p.ID,
    SUM(pm.NumDealsPurchases) AS total_discount_purchases,
    SUM(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS total_spending
FROM
    People p
JOIN
    Products pr ON p.ID = pr.ID
JOIN
    Promotion pm ON p.ID = pm.ID
GROUP BY
    p.ID;
