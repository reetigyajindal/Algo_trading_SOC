import pandas as pd

# Replace with your actual filename
file_path = "file.csv" # add the file

# Load the CSV
df = pd.read_csv(file_path)

# Drop first two rows if they are metadata
df = df.iloc[2:].copy()

# Rename columns correctly
df.columns = ["Datetime", "Close", "High", "Low", "Open", "Volume"]

# Convert datatypes
df["Datetime"] = pd.to_datetime(df["Datetime"])
for col in ["Open", "High", "Low", "Close", "Volume"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop any remaining NaNs
df.dropna(inplace=True)

# Set datetime as index
df.set_index("Datetime", inplace=True)

# Save cleaned version
df.to_csv("eicher.csv")
print("✅ Cleaned CSV saved as cleaned_data.csv")
