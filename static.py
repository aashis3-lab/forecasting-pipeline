import pandas as pd # Reads/manages data tables.
import matplotlib.pyplot as plt # Makes graphs
from statsmodels.tsa.holtwinters import ExponentialSmoothing # Basic forecasting

df = pd.read_csv("sales_data.csv")

# print(df.head()) # (prints first few lines)
# df.info()
# print(df.isna().sum())

# print(df["Customer"].unique()) # prints all our customers

# filter data
df_one = df[
    (df["Customer"] == "AMAZON.COM") &
    (df["Item"] == "PAC00-14231") &
    (df["Organization"] == "PRD:IND:IND-GEODIS WHSE IND US")
].copy()

# converting dates
df_one["Month"] = pd.to_datetime(
    df_one["Month"],
    format="%d-%b-%y"
)

# remove missing rows
df_one = df_one.dropna(subset=["History"])

# aggregate monthly demand
df_one = df_one.groupby("Month", as_index=False)["History"].sum()

# add monthly frequency
df_one = df_one.set_index("Month")
df_one = df_one.asfreq("MS")

# plot the demand
plt.plot(df_one.index, df_one.values) # draw line graph
plt.title("Demand Over Time (PAC00-14231) at AMAZON.COM in Indiana")
plt.show() # display our graph

# forecast model
model = ExponentialSmoothing(
    df_one["History"],
    trend="add"
)
fit = model.fit() # learn past demand pattern

forecast = fit.forecast(18)  # predict next 18 months
print("forecast for next 18 months:")
print(forecast)