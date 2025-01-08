import pandas as pd
import plotly.express as px

# Load the dataset
file_path_global = "D:/Promi/Time_Series_Line_Visualization/global-energy-substitution.csv"
global_data = pd.read_csv(file_path_global)

# Melt the dataframe for easier visualization
global_melted_data = global_data.melt(
    id_vars=["Year"],
    value_vars=[
        "Other renewables (TWh, substituted energy)", "Biofuels (TWh, substituted energy)",
        "Solar (TWh, substituted energy)", "Wind (TWh, substituted energy)",
        "Hydropower (TWh, substituted energy)", "Nuclear (TWh, substituted energy)",
        "Gas (TWh, substituted energy)", "Oil (TWh, substituted energy)",
        "Coal (TWh, substituted energy)", "Traditional biomass (TWh, substituted energy)"
    ],
    var_name="Energy Source",
    value_name="Consumption (TWh)"
)

# Simplify the energy source names for better readability
global_melted_data["Energy Source"] = global_melted_data["Energy Source"].str.replace(
    " \\(TWh, substituted energy\\)", "", regex=True
)

# Create the interactive area chart
fig = px.area(
    global_melted_data,
    x="Year",
    y="Consumption (TWh)",
    color="Energy Source",
    title="Global Primary Energy Consumption by Source (1800-2023)",
    labels={"Consumption (TWh)": "Consumption (TWh)", "Year": "Year"},
    hover_data={"Energy Source": True, "Consumption (TWh)": True}
)

# Save the interactive area chart to an HTML file
output_file_path = "interactive_area_chart.html"
fig.write_html(output_file_path)

print(f"Interactive area chart saved as {output_file_path}")
