import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
peak_hours = pd.read_csv("s3://your-bucket/nyc_taxi_data/output/peak_hours.csv")

# Plot peak hours
plt.figure(figsize=(12, 6))
sns.barplot(data=peak_hours, x='pickup_hour', y='trip_count', palette='viridis')
plt.title('Peak Hours for NYC Taxi Pickups')
plt.xlabel('Pickup Hour')
plt.ylabel('Trip Count')
plt.show()
