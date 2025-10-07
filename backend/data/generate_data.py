import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(0)
random.seed(0)

# Set fixed names
names = ["Trump", "Harris", "Obama", "Romney"]

# Generate time series data
def generate_sentiment_data(start_date, num_days):
    data = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    for i in range(num_days):
        for name in names:
            score = round(random.uniform(-1, 1), 3)
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "score": score,
                "name": name
            })
        current_date += timedelta(days=1)
    return data

# Generate 5 days of data, starting from 2025-01-1)
generated_data = generate_sentiment_data("2025-01-1", 5)
# print("Generated_data", generated_data)
