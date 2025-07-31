import pandas as pd
import ta

# Load data
df = pd.read_csv(r'aapl.csv')
df["Datetime"] = pd.to_datetime(df["Datetime"])
df.set_index("Datetime", inplace=True)

# MACD indicators
macd = ta.trend.MACD(close=df["Close"])
df["macd_hist"] = macd.macd_diff()

# Strategy parameters
take_profit_pct = 0.05
stop_loss_pct = 0.025

# Strategy state
in_position = False
entry_price = 0
trades = []

# Loop through data
for i in range(2, len(df)):
    h_now = df["macd_hist"].iloc[i]
    h_prev = df["macd_hist"].iloc[i - 1]

    # Avoid divide-by-zero
    if h_prev == 0:
        continue

    diff = abs(h_now - h_prev)
    slowdown = diff < 0.1 * abs(h_prev)

    # --- BUY ---
    if not in_position and h_now < 0 and slowdown:
        entry_price = df["Close"].iloc[i]
        in_position = True
        trades.append({
            "type": "BUY",
            "time": df.index[i],
            "price": entry_price
        })
        continue

    # --- SELL ---
    if in_position:
        price = df["Close"].iloc[i]
        pnl = (price - entry_price) / entry_price

        # Exit conditions
        sell_slowdown = h_now > 0 and slowdown
        if pnl >= take_profit_pct or pnl <= -stop_loss_pct or sell_slowdown:
            trades.append({
                "type": "SELL",
                "time": df.index[i],
                "price": price,
                "return_pct": round(pnl * 100, 2),
                "reason": (
                    "TP" if pnl >= take_profit_pct else
                    "SL" if pnl <= -stop_loss_pct else
                    "Momentum fade"
                )
            })
            in_position = False

# Save results
results_df = pd.DataFrame(trades)
results_df.to_csv("macd_momentum_slowdown_strategy.csv", index=False)
print("✅ Strategy complete. Results saved to macd_momentum_slowdown_strategy.csv")

# Summary
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