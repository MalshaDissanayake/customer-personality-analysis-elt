CREATE TABLE _online_vs_offline_preferences AS
SELECT
    SUM(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS total_spending,
    SUM(pl.NumWebPurchases) AS total_web_purchases,
    SUM(pl.NumStorePurchases) AS total_store_purchases
FROM
    Products pr
JOIN
    Place pl ON pr.ID = pl.ID;
