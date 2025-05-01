# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "764cb912-89c8-449a-b476-915bc4628bfb",
# META       "default_lakehouse_name": "bics_demo_lakehouse1",
# META       "default_lakehouse_workspace_id": "bb476c60-a3e3-4fd8-9168-81aa255ae0d3",
# META       "known_lakehouses": [
# META         {
# META           "id": "764cb912-89c8-449a-b476-915bc4628bfb"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import requests
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Step 1: Call Open-Meteo API for basic weather data
url = "https://api.open-meteo.com/v1/forecast?latitude=35.7796&longitude=-78.6382&hourly=temperature_2m"
response = requests.get(url)
data = response.json()

# Step 2: Extract the hourly forecast data
time_list = data['hourly']['time']
temp_list = data['hourly']['temperature_2m']
records = list(zip(time_list, temp_list))

# Step 3: Create DataFrame schema
schema = StructType([
    StructField("time", StringType(), True),
    StructField("temperature", DoubleType(), True)
])

# Step 4: Create DataFrame
df = spark.createDataFrame(records, schema=schema)

# Step 5: Save DataFrame to Lakehouse in Delta format
# NOTE: Your notebook MUST be attached to bics_demo_lakehouse1 in the top right UI
df.write.mode("overwrite").format("delta").save("Tables/WeatherForecast")

print("✅ WeatherForecast table created in Lakehouse: bics_demo_lakehouse1")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
