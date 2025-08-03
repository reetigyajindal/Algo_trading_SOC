
import pandas as pd
import ta

# Load data
df = pd.read_csv(r"C:\Users\Rohit Desale\OneDrive\Desktop\VWAP_RSI_Strategy\inf.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"])
df.set_index("Datetime", inplace=True)

# MACD Histogram
macd = ta.trend.MACD(close=df["Close"])
df["macd_hist"] = macd.macd_diff()

# Strategy variables
in_position = False
entry_price = 0
trades = []

# Strategy loop
for i in range(3, len(df)):
    h = df["macd_hist"].iloc[i]

    # Candle colors
    c0 = df["Close"].iloc[i] > df["Open"].iloc[i]
    c1 = df["Close"].iloc[i - 1] > df["Open"].iloc[i - 1]
    c2 = df["Close"].iloc[i - 2] > df["Open"].iloc[i - 2]

    # BUY: 2 red → 1 green + histogram < 0
    if not in_position and h < 0 and not c2 and not c1 and c0:
        entry_price = df["Close"].iloc[i]
        trades.append({
            "type": "BUY",
            "time": df.index[i],
            "price": entry_price
        })
        in_position = True
        continue

    # SELL: 2 green → 1 red + histogram > 0
    if in_position and h > 0 and c2 and c1 and not c0:
        exit_price = df["Close"].iloc[i]
        pnl = (exit_price - entry_price) / entry_price
        trades.append({
            "type": "SELL",
            "time": df.index[i],
            "price": exit_price,
            "return_pct": round(pnl * 100, 2)
        })
        in_position = False

# Save and summarize
results_df = pd.DataFrame(trades)
results_df.to_csv("histogram_candle_strategy_nothreshold.csv", index=False)
print("✅ Strategy complete. Results saved to histogram_candle_strategy_nothreshold.csv")

if not results_df.empty:
    profits = results_df[results_df["type"] == "SELL"]["return_pct"]
    num_trades = len(profits)
    win_rate = (profits > 0).mean() * 100
    avg_return = profits.mean()
    total_return = profits.sum()

    print(f"📊 Total trades: {num_trades}")
    print(f"✅ Win rate: {win_rate:.2f}%")
    print(f"📈 Avg return per trade: {avg_return:.2f}%")
    print(f"💰 Total return: {total_return:.2f}%")
else:
    print("No trades were executed.")
