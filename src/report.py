import os
import psycopg2
import csv

# Function to securely retrieve database credentials from environment variables
def get_database_credentials():
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("localhost")
    db_port = os.environ.get("5432")
    return db_name, db_user, db_password, db_host, db_port

# Function to connect to the PostgreSQL database
def connect_to_database():
    try:
        db_name, db_user, db_password, db_host, db_port = get_database_credentials()
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Function to execute SQL queries
def execute_query(conn, sql_query):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        return None

# Function to generate reports
def generate_report(conn, sql_query, report_name):
    rows = execute_query(conn, sql_query)

    if rows:
        # Generate report file
        cursor = conn.cursor()
        cursor.execute(sql_query)
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()

        # Replace problematic characters in report name
        report_name = report_name.replace('/', '_')

        with open(f'{report_name}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(column_names)  # Write column headers
            for row in rows:
                writer.writerow(row)
        print(f"{report_name} generated successfully.")
    else:
        print(f"No data retrieved from the database for {report_name}. Report generation failed.")

# Main function
def main():
    # Connect to the database
    conn = connect_to_database()
    if conn:
        # SQL queries and report names
        queries_and_reports = [
            ("SELECT p.Marital_Status, p.Education, AVG(p.Income) AS avg_income, AVG(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS avg_spending FROM People p JOIN Products pr ON p.ID = pr.ID GROUP BY p.Marital_Status, p.Education;", "demographic_influence"),
            ("SELECT EXTRACT(DAY FROM AGE(CURRENT_DATE, p.Dt_Customer)) AS days_since_enrollment, SUM(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS total_spending FROM People p JOIN Products pr ON p.ID = pr.ID GROUP BY p.Dt_Customer;", "Customer Loyalty vs. Spending"),
            ("SELECT p.Marital_Status, p.Education, AVG(pr.AcceptedCmp1) AS cmp1_acceptance_rate, AVG(pr.AcceptedCmp2) AS cmp2_acceptance_rate, AVG(pr.AcceptedCmp3) AS cmp3_acceptance_rate, AVG(pr.AcceptedCmp4) AS cmp4_acceptance_rate, AVG(pr.AcceptedCmp5) AS cmp5_acceptance_rate FROM People p JOIN Promotion pr ON p.ID = pr.ID GROUP BY p.Marital_Status, p.Education;", "promotion_response_demographics"),
            ("SELECT CASE WHEN p.Complain = 1 THEN 'Complained' ELSE 'Not Complained' END AS complaint_status, AVG(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS avg_spending, AVG(pm.AcceptedCmp1) AS cmp1_acceptance_rate, AVG(pm.AcceptedCmp2) AS cmp2_acceptance_rate, AVG(pm.AcceptedCmp3) AS cmp3_acceptance_rate, AVG(pm.AcceptedCmp4) AS cmp4_acceptance_rate, AVG(pm.AcceptedCmp5) AS cmp5_acceptance_rate FROM People p JOIN Products pr ON p.ID = pr.ID JOIN Promotion pm ON p.ID = pm.ID GROUP BY p.Complain;", "Complaints and Spending/Campaign Response"),
            ("SELECT p.Kidhome, p.Teenhome, AVG(pr.MntWines) AS avg_spending_wines, AVG(pr.MntFruits) AS avg_spending_fruits, AVG(pr.MntMeatProducts) AS avg_spending_meat, AVG(pr.MntFishProducts) AS avg_spending_fish, AVG(pr.MntSweetProducts) AS avg_spending_sweets, AVG(pr.MntGoldProds) AS avg_spending_gold FROM People p JOIN Products pr ON p.ID = pr.ID GROUP BY p.Kidhome, p.Teenhome;", "impact_of_children_and_teenagers"),
            ("SELECT p.ID, SUM(pm.NumDealsPurchases) AS total_discount_purchases, SUM(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS total_spending FROM People p JOIN Products pr ON p.ID = pr.ID JOIN Promotion pm ON p.ID = pm.ID GROUP BY p.ID;", "Discount Purchases vs. Overall Spending"),
            ("SELECT SUM(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS total_spending, SUM(pl.NumWebPurchases) AS total_web_purchases, SUM(pl.NumStorePurchases) AS total_store_purchases FROM Products pr JOIN Place pl ON pr.ID = pl.ID;", "online_vs_offline_preferences"),
            ("SELECT p.NumWebVisitsMonth, AVG(pr.AcceptedCmp1) AS cmp1_acceptance_rate, AVG(pr.AcceptedCmp2) AS cmp2_acceptance_rate, AVG(pr.AcceptedCmp3) AS cmp3_acceptance_rate, AVG(pr.AcceptedCmp4) AS cmp4_acceptance_rate, AVG(pr.AcceptedCmp5) AS cmp5_acceptance_rate FROM Place p JOIN Promotion pr ON p.ID = pr.ID GROUP BY p.NumWebVisitsMonth;", "website_engagement_promotion_response"),
            ("SELECT p.Education, AVG(pl.NumCatalogPurchases) AS avg_catalog_purchases, AVG(pr.MntGoldProds) AS avg_spending_gold FROM People p JOIN Place pl ON p.ID = pl.ID JOIN Products pr ON p.ID = pr.ID GROUP BY p.Education;", "catalogue_purchases_demographics"),
            ("SELECT p.Marital_Status, p.Education, p.Kidhome, p.Teenhome, AVG(pr.MntWines + pr.MntFruits + pr.MntMeatProducts + pr.MntFishProducts + pr.MntSweetProducts + pr.MntGoldProds) AS avg_spending FROM People p JOIN Products pr ON p.ID = pr.ID GROUP BY p.Marital_Status, p.Education, p.Kidhome, p.Teenhome;", "high_spend_customer_segments")
        ]

        # Generate reports for all queries
        for query, report_name in queries_and_reports:
            generate_report(conn, query, report_name)

        # Close database connection
        conn.close()

if __name__ == "__main__":
    main()