-- Customer Loyalty vs. Spending
CREATE TABLE _customer_loyalty AS
SELECT
    EXTRACT(DAY FROM AGE(CURRENT_DATE, p.Dt_Customer)) AS days_since_enrollment,
    SUM(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS total_spending
FROM
    People p
JOIN
    Products pr ON p.ID = pr.ID
GROUP BY
    p.Dt_Customer;
