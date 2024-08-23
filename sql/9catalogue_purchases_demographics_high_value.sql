-- Catalogue Purchases, Demographics, and High-value Spending
CREATE TABLE _catalogue_purchases_demographics AS
SELECT
    p.Education,
    AVG(pl.NumCatalogPurchases) AS avg_catalog_purchases,
    AVG(pr.MntGoldProds) AS avg_spending_gold
FROM
    People p
JOIN
    Place pl ON p.ID = pl.ID
JOIN
    Products pr ON p.ID = pr.ID
GROUP BY
    p.Education;
