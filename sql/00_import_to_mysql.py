import mysql.connector

def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="supply_chain_db",
        allow_local_infile=True
    )
    cursor = conn.cursor()
    
    # Execute LOAD DATA LOCAL INFILE
    load_query = """
    LOAD DATA LOCAL INFILE 'supply_chain_ready.csv'
    INTO TABLE supply_chain_orders
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
    """
    
    print("Executing LOAD DATA LOCAL INFILE...")
    cursor.execute(load_query)
    conn.commit()
    print(f"Successfully loaded {cursor.rowcount} rows.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_data()