import oracledb
import os

# Manual setup - Replace with your real passwords
DB_USER = "ADMIN"
DB_PASS = "Madhuri@12#04"
WALLET_PASS = "Madhuri@12#04"
WALLET_DIR = r"F:\PYBlogODB\tech_blog\oracle_wallet"

print(f"Testing connection to maddyblog_low...")

try:
    # This mimics exactly what Django is doing
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn="maddyblog_low",
        config_dir=WALLET_DIR,
        wallet_location=WALLET_DIR,
        wallet_password=WALLET_PASS
    )
    print("✅ SUCCESS! Your connection works.")
    print(f"Database version: {conn.version}")
    conn.close()
except Exception as e:
    print("❌ CONNECTION FAILED")
    print(f"Error details: {e}")