from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "sales_data.csv"
output_dir = base_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_path)
df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])
df["Month"] = df["Sale_Date"].dt.to_period("M").dt.to_timestamp()
df["Gross_Margin"] = (df["Unit_Price"] - df["Unit_Cost"]) * df["Quantity_Sold"]
df["Net_Revenue"] = df["Sales_Amount"] * (1 - df["Discount"])
df["Net_Profit"] = df["Gross_Margin"] - (df["Sales_Amount"] - df["Net_Revenue"])

monthly = df.groupby("Month")["Net_Revenue"].sum().reset_index()
monthly_region = df.groupby(["Month", "Region"])["Net_Revenue"].sum().reset_index()
rep_perf = df.groupby(["Sales_Rep", "Region"])["Net_Revenue"].sum().reset_index()

fig_trend = px.line(monthly, x="Month", y="Net_Revenue", markers=True, title="Monthly Net Revenue")
fig_trend_region = px.area(monthly_region, x="Month", y="Net_Revenue", color="Region", groupnorm="fraction", title="Monthly Net Revenue Share by Region")
fig_rep = px.bar(rep_perf, x="Net_Revenue", y="Sales_Rep", color="Region", title="Net Revenue by Sales Rep and Region", orientation="h")
fig_hist = px.histogram(df, x="Net_Revenue", nbins=30, marginal="box", title="Net Revenue Distribution with Boxplot")
fig_box = px.box(df, x="Product_Category", y="Net_Revenue", color="Product_Category", title="Net Revenue by Product Category")
fig_scatter = px.scatter(df, x="Discount", y="Net_Profit", color="Sales_Channel", symbol="Customer_Type", title="Net Profit vs Discount by Channel and Customer Type")

corr = df[["Net_Revenue", "Net_Profit", "Quantity_Sold", "Unit_Cost", "Unit_Price", "Discount"]].corr()
fig_corr = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale="Blues", zmin=-1, zmax=1, colorbar=dict(title="Corr")))
fig_corr.update_layout(title="Correlation Matrix")

figs = [fig_trend, fig_trend_region, fig_rep, fig_hist, fig_box, fig_scatter, fig_corr]

html_parts = []
for i, fig in enumerate(figs):
    html_parts.append(
        pio.to_html(
            fig,
            include_plotlyjs="cdn" if i == 0 else False,
            full_html=False,
            default_width="100%",
            default_height="520px",
        )
    )

html = "<html><head><meta charset='utf-8'><title>Sales Dashboard</title></head><body>" + "".join(html_parts) + "</body></html>"
(output_dir / "dashboard.html").write_text(html, encoding="utf-8")

