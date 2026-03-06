import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid

fake = Faker()
Faker.seed(42) # Consistent results

# CONFIGURATION
NUM_USERS = 1000
NUM_TRANSACTIONS = 15000 
FRAUD_RATIO = 0.1 

print("Generating smart financial data...")

# ---------------------------------------------------------
# 1. USERS
# ---------------------------------------------------------
users = []
for _ in range(NUM_USERS):
    uid = str(uuid.uuid4())
    users.append({
        "user_id": uid,
        "name": fake.name(),
        "email": fake.email(),
        "created_at": fake.date_time_between(start_date='-2y', end_date='-1y'),
        "is_active": True
    })
df_users = pd.DataFrame(users)

# ---------------------------------------------------------
# 2. DEVICES
# ---------------------------------------------------------
devices = []
for user in users:
    # Each user has 1-3 devices
    for _ in range(random.randint(1, 3)):
        devices.append({
            "device_id": str(uuid.uuid4()),
            "user_id": user['user_id'],
            "device_type": random.choice(['Mobile', 'Desktop', 'Tablet']),
            "os": random.choice(['iOS', 'Android', 'Windows', 'MacOS']),
            "last_active": fake.date_time_between(start_date='-1m', end_date='now')
        })
df_devices = pd.DataFrame(devices)

# ---------------------------------------------------------
# 3. TRANSACTIONS (The Smart Part)
# ---------------------------------------------------------
transactions = []

# Helper: Get a random device for a user
def get_user_device(u_id):
    user_devs = df_devices[df_devices['user_id'] == u_id]
    if not user_devs.empty:
        return user_devs.sample(1).iloc[0]['device_id']
    return str(uuid.uuid4()) # Unknown device

# A. Generate Standard Traffic (95%)
print("  - Generating normal traffic...")
for _ in range(int(NUM_TRANSACTIONS * (1 - FRAUD_RATIO))):
    user = random.choice(users)
    date_txn = fake.date_time_between(start_date='-1y', end_date='now')
    
    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "user_id": user['user_id'],
        "device_id": get_user_device(user['user_id']),
        "transaction_date": date_txn,
        "amount": round(random.uniform(5.00, 300.00), 2),
        "merchant": fake.company(),
        "category": random.choice(['Retail', 'Food', 'Travel', 'Tech']),
        "city": fake.city(),
        "country": "USA", # Normal traffic is domestic
        "is_fraud": False
    })

# B. Generate "Story" Fraud (5%)
print("  - Injecting specific fraud patterns...")

# Pattern 1: High Velocity (10 txns in 1 minute)
victim_velocity = users[0]
base_time = datetime.now()
for i in range(10):
    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "user_id": victim_velocity['user_id'],
        "device_id": get_user_device(victim_velocity['user_id']),
        "transaction_date": base_time + timedelta(seconds=i*5),
        "amount": 15.99,
        "merchant": "QuickPay Services",
        "category": "Tech",
        "city": "Chicago",
        "country": "USA",
        "is_fraud": True
    })

# Pattern 2: Impossible Travel (NYC -> London in 1 hour)
victim_travel = users[1]
time_travel = datetime.now() - timedelta(days=2)
# Txn 1: NYC
transactions.append({
    "transaction_id": str(uuid.uuid4()),
    "user_id": victim_travel['user_id'],
    "device_id": get_user_device(victim_travel['user_id']),
    "transaction_date": time_travel,
    "amount": 12.50,
    "merchant": "Starbucks NYC",
    "category": "Food",
    "city": "New York",
    "country": "USA",
    "is_fraud": False
})
# Txn 2: London (1 hour later)
transactions.append({
    "transaction_id": str(uuid.uuid4()),
    "user_id": victim_travel['user_id'],
    "device_id": get_user_device(victim_travel['user_id']),
    "transaction_date": time_travel + timedelta(hours=1),
    "amount": 2500.00,
    "merchant": "London Apple Store",
    "category": "Tech",
    "city": "London",
    "country": "UK",
    "is_fraud": True
})

# Pattern 3: High Amount on New Device
victim_whale = users[2]
transactions.append({
    "transaction_id": str(uuid.uuid4()),
    "user_id": victim_whale['user_id'],
    "device_id": str(uuid.uuid4()), # Brand new device ID
    "transaction_date": datetime.now() - timedelta(hours=5),
    "amount": 8500.00, # Huge amount
    "merchant": "Luxury Watches",
    "category": "Retail",
    "city": "Miami",
    "country": "USA",
    "is_fraud": True
})

# Fill remaining random fraud
current_count = len(transactions)
target_count = NUM_TRANSACTIONS
while len(transactions) < target_count:
    user = random.choice(users)
    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "user_id": user['user_id'],
        "device_id": str(uuid.uuid4()), # Often fraud uses new devices
        "transaction_date": fake.date_time_between(start_date='-1y', end_date='now'),
        "amount": round(random.uniform(500.00, 5000.00), 2),
        "merchant": fake.company(),
        "category": "Tech",
        "city": fake.city(),
        "country": random.choice(["Russia", "China", "Nigeria", "Brazil"]),
        "is_fraud": True
    })

# ---------------------------------------------------------
# 4. SAVE
# ---------------------------------------------------------
df_txn = pd.DataFrame(transactions)
df_users.to_csv('users.csv', index=False)
df_devices.to_csv('devices.csv', index=False)
df_txn.to_csv('transactions.csv', index=False)

print(f"Done! Created {len(users)} users, {len(devices)} devices, and {len(transactions)} transactions.")