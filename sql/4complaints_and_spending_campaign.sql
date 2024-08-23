-- Complaints and Spending/Campaign Response
CREATE TABLE _complaints_and_spending_campaign AS
SELECT
    CASE
        WHEN p.Complain = 1 THEN 'Complained'
        ELSE 'Not Complained'
    END AS complaint_status,
    AVG(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS avg_spending,
    AVG(pm.AcceptedCmp1) AS cmp1_acceptance_rate,
    AVG(pm.AcceptedCmp2) AS cmp2_acceptance_rate,
    AVG(pm.AcceptedCmp3) AS cmp3_acceptance_rate,
    AVG(pm.AcceptedCmp4) AS cmp4_acceptance_rate,
    AVG(pm.AcceptedCmp5) AS cmp5_acceptance_rate
FROM
    People p
JOIN
    Products pr ON p.ID = pr.ID
JOIN
    Promotion pm ON p.ID = pm.ID
GROUP BY
    p.Complain;
