-- Populate People table
INSERT INTO People (ID, Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, Dt_Customer, Recency, Complain)
SELECT ID, Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, CAST(Dt_Customer AS DATE), Recency, Complain
FROM alldata;
