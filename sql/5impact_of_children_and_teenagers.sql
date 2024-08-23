CREATE TABLE _impact_of_children_and_teenagers AS
SELECT
    p.Kidhome,
    p.Teenhome,
    AVG(pr.MntWines) AS avg_spending_wines,
    AVG(pr.MntFruits) AS avg_spending_fruits,
    AVG(pr.MntMeatProducts) AS avg_spending_meat,
    AVG(pr.MntFishProducts) AS avg_spending_fish,
    AVG(pr.MntSweetProducts) AS avg_spending_sweets,
    AVG(pr.MntGoldProds) AS avg_spending_gold
FROM
    People p
JOIN
    Products pr ON p.ID = pr.ID
GROUP BY
    p.Kidhome,
    p.Teenhome;
