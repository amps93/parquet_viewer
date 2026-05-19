import os
import random
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq

def generate_mock_sales_data(num_rows: int = 10000) -> pa.Table:
    """
    Generates a rich mock sales dataset entirely using pure Python and PyArrow (No Pandas/NumPy).
    """
    random.seed(42)
    
    # Generate Transaction ID
    transaction_ids = list(range(100001, 100001 + num_rows))
    
    # Generate Timestamp
    start_date = datetime.now() - timedelta(days=365)
    timestamps = [start_date + timedelta(seconds=random.randint(0, 365 * 24 * 3600)) for _ in range(num_rows)]
    
    # Generate Customer ID
    customer_ids = [f"CUST-{random.randint(1000, 1999)}" for _ in range(num_rows)]
    
    # Categories & Payments
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports & Outdoors', 'Beauty']
    category_weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
    category_choices = random.choices(categories, weights=category_weights, k=num_rows)
    
    payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Crypto', 'Debit Card']
    payment_weights = [0.45, 0.25, 0.15, 0.05, 0.10]
    payments = random.choices(payment_methods, weights=payment_weights, k=num_rows)
    
    prices = []
    quantities = []
    for cat in category_choices:
        if cat == 'Electronics':
            price = round(random.uniform(50.0, 1200.0), 2)
            qty = random.randint(1, 2)
        elif cat == 'Clothing':
            price = round(random.uniform(15.0, 150.0), 2)
            qty = random.randint(1, 4)
        elif cat == 'Home & Kitchen':
            price = round(random.uniform(10.0, 500.0), 2)
            qty = random.randint(1, 2)
        elif cat == 'Books':
            price = round(random.uniform(5.0, 45.0), 2)
            qty = random.randint(1, 3)
        elif cat == 'Sports & Outdoors':
            price = round(random.uniform(20.0, 300.0), 2)
            qty = random.randint(1, 2)
        else: # Beauty
            price = round(random.uniform(8.0, 120.0), 2)
            qty = random.randint(1, 3)
        prices.append(price)
        quantities.append(qty)
        
    total_amounts = [round(p * q, 2) for p, q in zip(prices, quantities)]
    
    # Ratings (float 1.0 to 5.0 with ~8% missing/None values)
    ratings = []
    for _ in range(num_rows):
        if random.random() < 0.08:
            ratings.append(None)
        else:
            ratings.append(round(random.uniform(1.0, 5.0), 1))
            
    # Is Returned (boolean)
    is_returned = random.choices([True, False], weights=[0.07, 0.93], k=num_rows)
    
    # States
    states = ['CA', 'NY', 'TX', 'FL', 'IL', 'WA', 'MA', 'CO', 'GA', 'AZ']
    store_states = [random.choice(states) for _ in range(num_rows)]
    
    # Construct dictionary
    data = {
        'transaction_id': transaction_ids,
        'timestamp': timestamps,
        'customer_id': customer_ids,
        'category': category_choices,
        'unit_price': prices,
        'quantity': quantities,
        'total_amount': total_amounts,
        'payment_method': payments,
        'rating': ratings,
        'is_returned': is_returned,
        'store_state': store_states
    }
    
    return pa.Table.from_pydict(data)

def save_mock_parquet(directory_path: str, num_rows: int = 10000) -> str:
    """
    Saves the generated mock sales table as a parquet file.
    """
    os.makedirs(directory_path, exist_ok=True)
    table = generate_mock_sales_data(num_rows)
    file_path = os.path.join(directory_path, "mock_sales_data.parquet")
    pq.write_table(table, file_path)
    return os.path.abspath(file_path)
