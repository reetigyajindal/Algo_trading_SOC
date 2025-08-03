import os
import yfinance as yf

def fetch_csv(filename="file.csv", period="60d"):
    df = yf.download("EICHERMOT.NS", period=period, interval="15m")
    df.reset_index(inplace=True)  # Ensure 'Datetime' is a column
    df.to_csv(filename, index=False)
    full_path = os.path.abspath(filename)
    print(f"✅ Saved CSV to: {full_path}")
    return full_path

if __name__ == "__main__":
    fetch_csv()
