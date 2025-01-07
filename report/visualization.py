import databento as db
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# First, create a historical client
client = db.Historical(key="n/a")

# Next, we will request mbp-10 for the front-month ES contract
data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    schema="mbp-10",
    start="2023-12-06T14:30:00",
    end="2023-12-06T20:33:00",
    symbols=["ES.n.0"],
    stype_in="continuous",
)

# And, convert to a pandas DataFrame
df = data.to_df()

# Filter out trades only
df = df[df.action == "T"]
# Now, get midprice returns with a forward markout of 500 trades
df["mid"] = (df["bid_px_00"] + df["ask_px_00"]) / 2
df["ret_500t"] = df["mid"].shift(-500) - df["mid"]
df = df.dropna()

# Calculate depth imbalance on top level ('skew')
df["skew"] = np.log(df.bid_sz_00) - np.log(df.ask_sz_00)

# Calculate order imbalance on top ten levels ('imbalance')
bid_count = df[list(df.filter(regex="bid_ct_0[0-9]"))].sum(axis=1)
ask_count = df[list(df.filter(regex="ask_ct_0[0-9]"))].sum(axis=1)
df["imbalance"] = np.log(bid_count) - np.log(ask_count)

# Split in-sample and out-of-sample
split = int(0.66 * len(df))
split -= split % 100
df_in = df.iloc[:split]
df_out = df.iloc[split:]

# Now, evaluate signal correlation
corr = df_in[["skew", "imbalance", "ret_500t"]].corr()
print(corr.where(np.triu(np.ones(corr.shape)).astype(bool)))

reg = LinearRegression(fit_intercept=False, positive=True)

# Create a model using skew only
reg.fit(df_in[["skew"]], df_in["ret_500t"])
pred_skew = reg.predict(df_out[["skew"]])

# Create a model using imbalance only
reg.fit(df_in[["imbalance"]], df_in["ret_500t"])
pred_imbalance = reg.predict(df_out[["imbalance"]])

# Create a model using both skew and imbalance
reg.fit(df_in[["skew", "imbalance"]], df_in["ret_500t"])
pred_combined = reg.predict(df_out[["skew", "imbalance"]])


# Define a function to calculate profit and loss
def get_cumulative_markout_pnl(pred):
    df_pnl = pd.DataFrame({"pred": pred, "ret_500t": df_out["ret_500t"].values})
    df_pnl.loc[df_pnl["pred"] < 0, "ret_500t"] *= -1
    df_pnl = df_pnl.sort_values(by="pred")
    return df_pnl["ret_500t"].cumsum().values


# Then, collect results into a DataFrame
results = pd.DataFrame(
    {
        "skew": get_cumulative_markout_pnl(pred_skew),
        "imbalance": get_cumulative_markout_pnl(pred_imbalance),
        "combined": get_cumulative_markout_pnl(pred_combined),
    },
    index=np.linspace(0, 100, num=len(df_out)),
)

# Plot the results
results.plot(
    title="Forecasting with book skew vs. imbalance",
    xlabel="Predictor value (percentile)",
    ylabel="Cumulative return",
).legend(loc="lower center", ncols=3)
plt.show()

