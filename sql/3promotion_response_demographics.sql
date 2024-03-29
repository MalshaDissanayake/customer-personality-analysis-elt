CREATE TABLE _promotion_response_demographics AS
SELECT
    p.Marital_Status,
    p.Education,
    AVG(pr.AcceptedCmp1) AS cmp1_acceptance_rate,
    AVG(pr.AcceptedCmp2) AS cmp2_acceptance_rate,
    AVG(pr.AcceptedCmp3) AS cmp3_acceptance_rate,
    AVG(pr.AcceptedCmp4) AS cmp4_acceptance_rate,
    AVG(pr.AcceptedCmp5) AS cmp5_acceptance_rate
FROM
    People p
JOIN
    Promotion pr ON p.ID = pr.ID
GROUP BY
    p.Marital_Status,
    p.Education;
