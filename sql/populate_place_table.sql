-- Populate Place table
INSERT INTO Place (ID, NumWebPurchases, NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth)
SELECT ID, NumWebPurchases, NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth
FROM alldata;
