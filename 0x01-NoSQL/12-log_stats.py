#!/usr/bin/env python3
"""log stats from collection
"""
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.logs
collection = db.nginx

# Count total logs
total_logs = collection.count_documents({})

print(f"{total_logs} logs")

# Count methods
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = {method: collection.count_documents({"method": method}) for method in methods}

print("Methods:")
for method, count in method_counts.items():
    print(f"\tmethod {method}: {count}")

# Count status check
status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

print(f"{status_check_count} status check")
