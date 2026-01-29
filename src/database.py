import sqlite3
from pathlib import Path
from datetime import date, timedelta
import random

DB_PATH = Path(__file__).parent.parent / "data.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            date DATE NOT NULL,
            impressions INTEGER NOT NULL,
            clicks INTEGER NOT NULL,
            spend REAL NOT NULL,
            conversions INTEGER NOT NULL,
            revenue REAL NOT NULL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM campaigns")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    campaigns = [
        ("Summer Sale 2026", "active", "2026-01-01"),
        ("Brand Awareness Q1", "active", "2026-01-15"),
        ("Product Launch", "active", "2026-02-01"),
        ("Retargeting Campaign", "paused", "2026-01-10"),
        ("Holiday Promo", "ended", "2025-12-01"),
    ]

    cursor.executemany(
        "INSERT INTO campaigns (name, status, created_at) VALUES (?, ?, ?)",
        campaigns
    )

    random.seed(42)
    start_date = date(2026, 1, 1)

    for campaign_id in range(1, 6):
        base_impressions = random.randint(5000, 20000)
        base_ctr = random.uniform(0.02, 0.05)
        base_cpc = random.uniform(0.5, 2.0)
        base_conv_rate = random.uniform(0.02, 0.08)
        base_order_value = random.uniform(50, 150)

        for day_offset in range(90):
            current_date = start_date + timedelta(days=day_offset)
            weekday = current_date.weekday()
            weekend_factor = 0.7 if weekday >= 5 else 1.0

            impressions = int(base_impressions * weekend_factor * random.uniform(0.8, 1.2))
            clicks = int(impressions * base_ctr * random.uniform(0.8, 1.2))
            spend = round(clicks * base_cpc * random.uniform(0.9, 1.1), 2)
            conversions = int(clicks * base_conv_rate * random.uniform(0.7, 1.3))
            revenue = round(conversions * base_order_value * random.uniform(0.8, 1.2), 2)

            cursor.execute(
                """INSERT INTO daily_metrics
                   (campaign_id, date, impressions, clicks, spend, conversions, revenue)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (campaign_id, current_date.isoformat(), impressions, clicks, spend, conversions, revenue)
            )

    conn.commit()
    conn.close()
