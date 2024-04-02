import os
import csv
import psycopg
from datetime import datetime

# Function to establish a connection to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT")
        )
        return conn
    except psycopg.Error as e:
        print("Error connecting to database:", e)

# Function to create a table in the PostgreSQL database
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alldata (
                ID INTEGER,
                Year_Birth INTEGER,
                Education TEXT,
                Marital_Status TEXT,
                Income NUMERIC,
                Kidhome INTEGER,
                Teenhome INTEGER,
                Dt_Customer DATE,
                Recency INTEGER,
                Complain INTEGER,
                MntWines NUMERIC,
                MntFruits NUMERIC,
                MntMeatProducts NUMERIC,
                MntFishProducts NUMERIC,
                MntSweetProducts NUMERIC,
                MntGoldProds NUMERIC,
                NumWebPurchases INTEGER,
                NumCatalogPurchases INTEGER,
                NumStorePurchases INTEGER,
                NumWebVisitsMonth INTEGER,
                NumDealsPurchases INTEGER,
                AcceptedCmp3 INTEGER,
                AcceptedCmp4 INTEGER,
                AcceptedCmp5 INTEGER,
                AcceptedCmp1 INTEGER,
                AcceptedCmp2 INTEGER,
                Response INTEGER
            )
        """)
        conn.commit()
        cursor.close()
    except psycopg.Error as e:
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
                    INSERT INTO alldata (
                        ID, Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, Dt_Customer,
                        Recency, Complain, MntWines, MntFruits, MntMeatProducts, MntFishProducts,
                        MntSweetProducts, MntGoldProds, NumWebPurchases,
                        NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth, NumDealsPurchases, AcceptedCmp3, AcceptedCmp4,
                        AcceptedCmp5, AcceptedCmp1, AcceptedCmp2, Response
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, row)
        conn.commit()
        cursor.close()
    except psycopg.Error as e:
        print("Error loading data:", e)

def main():
    conn = connect_to_database()
    if conn is not None:
        create_table(conn)
        extract_and_load_data(conn)
        conn.close()

if __name__ == "__main__":
    main()
