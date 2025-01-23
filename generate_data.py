import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    dbname="mydatabase",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(100),
    product_cost DECIMAL(10, 2),
    category VARCHAR(50),
    quantity INT,
    price DECIMAL(10, 2),
    discount DECIMAL(10, 2),
    profit DECIMAL(10, 2),
    sale_date DATE,
    sale_time TIMESTAMP,
    customer_id INT,
    customer_name VARCHAR(100),
    customer_region VARCHAR(50),
    payment_method VARCHAR(50)
);
""")
conn.commit()

def generate_data(num_rows):
    categories = ["Electronics", "Accessories", "Home", "Office", "Furniture"]
    products = {
        "Electronics": ["Laptop", "Smartphone", "Tablet", "Monitor", "Printer"],
        "Accessories": ["Keyboard", "Mouse", "Headphones", "Charger", "Adapter"],
        "Home": ["Desk Lamp", "Chair", "Table", "Sofa", "Bed"],
        "Office": ["Printer", "Desk", "Chair", "Projector", "Whiteboard"],
        "Furniture": ["Chair", "Table", "Sofa", "Bed", "Cabinet"]
    }
    payment_methods = ["Credit Card", "Cash", "PayPal", "Bank Transfer"]
    regions = ["North", "South", "East", "West"]

    for _ in range(num_rows):
        category = random.choice(categories)
        product_name = random.choice(products[category])
        product_id = random.randint(1000, 9999)
        product_cost = round(random.uniform(50.0, 1000.0), 2)
        quantity = random.randint(1, 100)
        price = round(random.uniform(100.0, 2000.0), 2)
        discount = round(random.uniform(0.0, 20.0), 2)
        profit = (price - product_cost) * quantity
        sale_date = fake.date_between(start_date="-2y", end_date="today")
        sale_time = fake.date_time_between(start_date="-2y", end_date="now")
        customer_id = random.randint(1, 1000)
        customer_name = fake.name()
        customer_region = random.choice(regions)
        payment_method = random.choice(payment_methods)

        cursor.execute("""
        INSERT INTO sales (
            product_id, product_name, product_cost, category, quantity, price,
            discount, profit, sale_date, sale_time, customer_id, customer_name,
            customer_region, payment_method
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            product_id, product_name, product_cost, category, quantity, price,
            discount, profit, sale_date, sale_time, customer_id, customer_name,
            customer_region, payment_method
        ))

    conn.commit()

generate_data(1_000_000)

cursor.close()
conn.close()