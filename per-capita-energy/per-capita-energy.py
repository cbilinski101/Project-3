import pandas as pd
import plotly.express as px

# Load the dataset
file_path = "D:/Promi/Per_Capita_Visualization/per-capita-energy-stacked.csv"
data = pd.read_csv(file_path)

# Filter the dataset for the year 2023 and relevant countries
countries = [
    "United States", "United Kingdom", "World", "China", 
    "India", "France", "Germany", "Sweden", 
    "South Africa", "Japan", "Brazil"
]
filtered_data = data[(data["Year"] == 2023) & (data["Entity"].isin(countries))]

# Melt the dataframe for easier visualization
melted_data = filtered_data.melt(
    id_vars=["Entity"],
    value_vars=[
        "Coal per capita (kWh)", "Oil per capita (kWh)", 
        "Gas per capita (kWh)", "Nuclear per capita (kWh - equivalent)", 
        "Hydro per capita (kWh - equivalent)", "Wind per capita (kWh - equivalent)", 
        "Solar per capita (kWh - equivalent)", "Other renewables per capita (kWh - equivalent)"
    ],
    var_name="Energy Source",
    value_name="Consumption (kWh)"
)

# Rename columns for better readability
melted_data["Energy Source"] = melted_data["Energy Source"].str.replace(" per capita \\(kWh.*\\)", "", regex=True)

# Create the interactive stacked bar chart
fig = px.bar(
    melted_data,
    x="Entity",
    y="Consumption (kWh)",
    color="Energy Source",
    title="Per Capita Primary Energy Consumption by Source (2023)",
    labels={"Entity": "Country", "Consumption (kWh)": "Consumption (kWh)"},
    hover_data={"Energy Source": True, "Consumption (kWh)": True}
)

# Save the interactive bar chart to an HTML file
output_file_path = "interactive_bar_chart.html"
fig.write_html(output_file_path)

print(f"Interactive bar chart saved as {output_file_path}")
