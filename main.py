import os
import random
from datetime import datetime

import faker
import psycopg2


fake = faker.Faker()


def generate_transaction():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "userId": user["username"],
        "timestamp": datetime.utcnow().timestamp(),
        "amount": round(random.uniform(10, 1000), 2),
        "currency": random.choice(["USD", "GBP"]),
        "city": fake.city(),
        "country": fake.country(),
        "merchantName": fake.company(),
        "paymentMethod": random.choice(
            ["credit_card", "debit_card", "online_transfer"]
        ),
        "ipAddress": fake.ipv4(),
        "voucherCode": random.choice(["", "DISCOUNT10", ""]),
        "affiliateId": fake.uuid4(),
    }


def create_table(conn):
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            timestamp TIMESTAMP,
            amount DECIMAL,
            currency VARCHAR(255),
            city VARCHAR(255),
            country VARCHAR(255),
            merchant_name VARCHAR(255),
            payment_method VARCHAR(255),
            ip_address VARCHAR(255),
            voucher_code VARCHAR(255),
            affiliateId VARCHAR(255)
        )
        """
    )

    cursor.close()
    conn.commit()


def main():
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        raise ValueError(
            "DB_PASSWORD is required. Set it via environment variables (recommended: use .env.example)."
        )

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "financial_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=db_password,
        port=int(os.getenv("DB_PORT", "5432")),
    )

    create_table(conn)

    transaction = generate_transaction()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO transactions(transaction_id, user_id, timestamp, amount, currency, city, country, merchant_name, payment_method, 
        ip_address, affiliateId, voucher_code)
        VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            transaction["transactionId"],
            transaction["userId"],
            datetime.fromtimestamp(transaction["timestamp"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            transaction["amount"],
            transaction["currency"],
            transaction["city"],
            transaction["country"],
            transaction["merchantName"],
            transaction["paymentMethod"],
            transaction["ipAddress"],
            transaction["affiliateId"],
            transaction["voucherCode"],
        ),
    )

    cur.close()
    conn.commit()


if __name__ == "__main__":
    main()
