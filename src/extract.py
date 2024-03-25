#This is the code to extract data into four tables as people,products,promotions, and places.
import psycopg2
import pandas as pd
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to your dataset file
dataset_path = os.path.join(script_dir, "..", "dataset", "dataset.csv")

# Database connection parameters
host = "localhost"
port = "5432"   
database = "postgres"   
user = "postgres"
password = "POSTGRESmalsha@3"

try:
    # Establish a connection to the database
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            ID SERIAL PRIMARY KEY,
            Year_Birth INTEGER,
            Education VARCHAR,
            Marital_Status VARCHAR,
            Income FLOAT,
            Kidhome INTEGER,
            Teenhome INTEGER,
            Dt_Customer DATE,
            Recency INTEGER,
            Complain INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            Product_ID SERIAL PRIMARY KEY,
            ID INTEGER,
            MntWines FLOAT,
            MntFruits FLOAT,
            MntMeatProducts FLOAT,
            MntFishProducts FLOAT,
            MntSweetProducts FLOAT,
            MntGoldProds FLOAT,
            FOREIGN KEY (ID) REFERENCES people(ID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            Promotion_ID SERIAL PRIMARY KEY,
            ID INTEGER,
            NumDealsPurchases INTEGER,
            AcceptedCmp1 INTEGER,
            AcceptedCmp2 INTEGER,
            AcceptedCmp3 INTEGER,
            AcceptedCmp4 INTEGER,
            AcceptedCmp5 INTEGER,
            Response INTEGER,
            FOREIGN KEY (ID) REFERENCES people(ID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            Place_ID SERIAL PRIMARY KEY,
            ID INTEGER,
            NumWebPurchases INTEGER,
            NumCatalogPurchases INTEGER,
            NumStorePurchases INTEGER,
            NumWebVisitsMonth INTEGER,
            FOREIGN KEY (ID) REFERENCES people(ID)
        )
    """)

    # Commit the transaction
    connection.commit()

    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(dataset_path)

    # Insert data into the 'people' table
    people_data = df[["ID", "Year_Birth", "Education", "Marital_Status", 
                      "Income", "Kidhome", "Teenhome", "Dt_Customer", 
                      "Recency", "Complain"]]
    people_data.to_sql('people', connection, if_exists='replace', index=False)

    # Insert data into the 'product' table
    product_data = df[["ID", "MntWines", "MntFruits", "MntMeatProducts", 
                       "MntFishProducts", "MntSweetProducts", "MntGoldProds"]]
    product_data.to_sql('product', connection, if_exists='replace', index=False)

    # Insert data into the 'promotions' table
    promotions_data = df[["ID", "NumDealsPurchases", "AcceptedCmp1", "AcceptedCmp2",
                          "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "Response"]]
    promotions_data.to_sql('promotions', connection, if_exists='replace', index=False)

    # Insert data into the 'places' table
    places_data = df[["ID", "NumWebPurchases", "NumCatalogPurchases", 
                      "NumStorePurchases", "NumWebVisitsMonth"]]
    places_data.to_sql('places', connection, if_exists='replace', index=False)

    print("Data extraction and loading successful!")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
