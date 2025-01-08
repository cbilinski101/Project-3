import pandas as pd
import plotly.express as px

# Load the dataset
file_path_renewables = "D:/Promi/Map_Visualization/share-electricity-renewables.csv"
renewables_data = pd.read_csv(file_path_renewables)

# Filter the data for the year 2023
renewables_2023 = renewables_data[renewables_data["Year"] == 2023]

# Rename columns for better readability
renewables_2023 = renewables_2023.rename(columns={
    "Entity": "Country",
    "Renewables - % electricity": "Renewables Share (%)"
})

# Create the interactive map with hover and click functionality
fig_map = px.choropleth(
    renewables_2023,
    locations="Country",
    locationmode="country names",
    color="Renewables Share (%)",
    hover_name="Country",
    hover_data=["Renewables Share (%)"],
    color_continuous_scale="Greens",
    title="Share of Electricity Production from Renewables (2023)"
)

# Update the layout to enable zoom and clicks
fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="equirectangular"
    ),
    clickmode="event+select"
)

# Save the map to an HTML file
output_file_path = "interactive_map.html"
fig_map.write_html(output_file_path)

print(f"Interactive map saved as {output_file_path}")
