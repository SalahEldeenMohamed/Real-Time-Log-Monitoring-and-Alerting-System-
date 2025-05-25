import os
import json
from datetime import datetime, timedelta

log_dir = 'logs_output'
threshold = 10
time_window = timedelta(minutes=5)
error_count = 0

now = datetime.now()

# Loop through log files
for filename in os.listdir(log_dir):
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(log_dir, filename)
    with open(filepath, 'r') as f:
        for line in f:
            try:
                log = json.loads(line)
                log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
                if log['level'] == 'ERROR' and now - log_time <= time_window:
                    error_count += 1
            except:
                continue

# Trigger alert
if error_count >= threshold:
    print(f"🚨 ALERT: {error_count} ERROR logs in last 5 minutes!")
else:
    print(f"✅ No alert. ERROR count: {error_count}")
