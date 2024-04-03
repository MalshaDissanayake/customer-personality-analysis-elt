CREATE TABLE _website_engagement_promotion_response AS
SELECT
    p.NumWebVisitsMonth,
    AVG(pr.AcceptedCmp1) AS cmp1_acceptance_rate,
    AVG(pr.AcceptedCmp2) AS cmp2_acceptance_rate,
    AVG(pr.AcceptedCmp3) AS cmp3_acceptance_rate,
    AVG(pr.AcceptedCmp4) AS cmp4_acceptance_rate,
    AVG(pr.AcceptedCmp5) AS cmp5_acceptance_rate
FROM
    Place p
JOIN
    Promotion pr ON p.ID = pr.ID
GROUP BY
    p.NumWebVisitsMonth;
