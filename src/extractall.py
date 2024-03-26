import os
import csv
import psycopg2
from datetime import datetime

# Function to establish a connection to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="POSTGRESmalsha@3",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to database:", e)

# Function to create a table in the PostgreSQL database
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_personality (
                ID SERIAL PRIMARY KEY,
                Year_Birth INTEGER,
                Education TEXT,
                Marital_Status TEXT,
                Income NUMERIC,
                Kidhome INTEGER,
                Teenhome INTEGER,
                Dt_Customer DATE,
                Recency INTEGER,
                MntWines NUMERIC,
                MntFruits NUMERIC,
                MntMeatProducts NUMERIC,
                MntFishProducts NUMERIC,
                MntSweetProducts NUMERIC,
                MntGoldProds NUMERIC,
                NumDealsPurchases INTEGER,
                NumWebPurchases INTEGER,
                NumCatalogPurchases INTEGER,
                NumStorePurchases INTEGER,
                NumWebVisitsMonth INTEGER,
                AcceptedCmp3 INTEGER,
                AcceptedCmp4 INTEGER,
                AcceptedCmp5 INTEGER,
                AcceptedCmp1 INTEGER,
                AcceptedCmp2 INTEGER,
                Complain INTEGER,
                Z_CostContact INTEGER,
                Z_Revenue INTEGER,
                Response INTEGER
            )
        """)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error creating table:", e)

# Function to parse date from string
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').date()
    except ValueError:
        return None  # Return None if date format is not recognized

# Function to extract data from the CSV file and load it into the PostgreSQL table
def extract_and_load_data(conn):
    try:
        cursor = conn.cursor()
        with open(os.path.join(os.path.dirname(__file__), '..', 'dataset', 'dataset1.csv'), 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                # Convert date string to datetime object
                dt_customer = parse_date(row[7])
                if dt_customer is None:
                    print("Error parsing date:", row[7])
                    continue

                # Convert empty strings to None for numeric columns
                row = [None if value == '' else value for value in row]

                cursor.execute("""
                    INSERT INTO customer_personality (
                        ID,Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, Dt_Customer,
                        Recency, MntWines, MntFruits, MntMeatProducts, MntFishProducts,
                        MntSweetProducts, MntGoldProds, NumDealsPurchases,NumWebPurchases,
                        NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth, AcceptedCmp3, AcceptedCmp4,
                        AcceptedCmp5, AcceptedCmp1, AcceptedCmp2, Complain, Z_CostContact, Z_Revenue, Response
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, row)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error loading data:", e)

def main():
    conn = connect_to_database()
    if conn is not None:
        create_table(conn)
        extract_and_load_data(conn)
        conn.close()

if __name__ == "__main__":
    main()
