import pandas as pd
import mysql.connector

# 1. Load CSV
print("1. Loading CSV file...")
df = pd.read_csv('SupplyChainCleaned.csv', encoding='latin1')

# 2. Fix date format
print("2. Formatting dates to YYYY-MM-DD...")
df['Formatted_order date'] = pd.to_datetime(
    df['Formatted_order date'], errors='coerce'
).dt.strftime('%Y-%m-%d')

# 3. Rename columns
column_mapping = {
    'Type': 'TransactionType',
    'Days for shipping (real)': 'DaysForShippingReal',
    'Days for shipment (scheduled)': 'DaysForShippingScheduled',
    'Benefit per order': 'BenefitPerOrder',
    'Sales per customer': 'SalesPerCustomer',
    'Delivery Status': 'DeliveryStatus',
    'Late_delivery_risk': 'LateDeliveryRisk',
    'Category Id': 'CategoryId',
    'Category Name': 'CategoryName',
    'Customer City': 'CustomerCity',
    'Customer Country': 'CustomerCountry',
    'Customer Email': 'CustomerEmail',
    'Customer Fname': 'CustomerFName',
    'Customer Id': 'CustomerId',
    'Customer Lname': 'CustomerLName',
    'Customer Password': 'CustomerPassword',
    'Customer Segment': 'CustomerSegment',
    'Customer State': 'CustomerState',
    'Customer Street': 'CustomerStreet',
    'Customer Zipcode': 'CustomerZipcode',
    'Department Id': 'DepartmentId',
    'Department Name': 'DepartmentName',
    'Latitude': 'Latitude',
    'Longitude': 'Longitude',
    'Market': 'Market',
    'Order City': 'OrderCity',
    'Order Country': 'OrderCountry',
    'Order Customer Id': 'OrderCustomerId',
    'Formatted_order date': 'FormattedOrderDate',
    'order date (DateOrders)': 'OrderDateRaw',
    'Order Id': 'OrderID',
    'Order Item Cardprod Id': 'OrderItemCardprodId',
    'Order Item Discount': 'OrderItemDiscount',
    'Order Item Discount Rate': 'OrderItemDiscountRate',
    'Order Item Id': 'OrderItemId',
    'Order Item Product Price': 'OrderItemProductPrice',
    'Order Item Profit Ratio': 'OrderItemProfitRatio',
    'Order Item Quantity': 'OrderItemQuantity',
    'Sales': 'Sales',
    'Order Item Total': 'OrderItemTotal',
    'Order Profit Per Order': 'OrderProfitPerOrder',
    'Order Region': 'OrderRegion',
    'Order State': 'OrderState',
    'Order Status': 'OrderStatus',
    'Order Zipcode': 'OrderZipcode',
    'Product Card Id': 'ProductCardId',
    'Product Category Id': 'ProductCategoryId',
    'Product Description': 'ProductDescription',
    'Product Image': 'ProductImage',
    'Product Name': 'ProductName',
    'Product Price': 'ProductPrice',
    'Product Status': 'ProductStatus',
    'shipping date (DateOrders)': 'ShippingDateRaw',
    'Shipping Mode': 'ShippingMode',
    'Delay_Days': 'DelayDays',
    'Delay_Category': 'DelayCategory',
    'Loss_Percentage': 'LossPercentage',
    'CostImpactof_Delay': 'CostImpactOfDelay',
    'SupplierRiskScore': 'SupplierRiskScore'
}
df = df.rename(columns=column_mapping)

# 4. Replace all NaN with None (SQL NULL)
print("3. Converting NaN to NULL...")
df = df.astype(object).where(pd.notnull(df), None)

# 5. Convert dataframe to list of tuples
rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
columns = list(df.columns)
placeholders = ', '.join(['%s'] * len(columns))
col_names = ', '.join([f'`{c}`' for c in columns])
insert_query = f"INSERT INTO supply_chain_orders ({col_names}) VALUES ({placeholders})"

# 6. Connect to MySQL directly (no SQLAlchemy)
print("4. Connecting to MySQL on port 3308...")
conn = mysql.connector.connect(
    host="localhost",
    port=3308,
    user="root",
    password="",
    database="supply_chain_db"
)
cursor = conn.cursor()

# 7. Clear existing data
print("5. Clearing existing table data...")
cursor.execute("TRUNCATE TABLE supply_chain_orders")
conn.commit()

# 8. Insert in chunks of 5000 rows using executemany
chunk_size = 5000
total_rows = len(rows)
print(f"6. Inserting {total_rows} rows in chunks of {chunk_size}...")

for i in range(0, total_rows, chunk_size):
    chunk = rows[i:i + chunk_size]
    cursor.executemany(insert_query, chunk)
    conn.commit()
    print(f"   Inserted rows {i} to {min(i + chunk_size, total_rows)}...")

print(f"\nSuccess! All {total_rows} rows inserted into MySQL!")
cursor.close()
conn.close()