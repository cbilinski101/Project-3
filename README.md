# Energy Data Visualization Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![GitHub Pages](https://img.shields.io/badge/Deployed-GitHub%20Pages-brightgreen)


This repository contains three interactive data visualization projects related to global energy consumption trends. Each visualization provides insights into different aspects of energy usage globally.

---

## **1. Global Primary Energy Consumption by Source**

This section provides analysis of the trends in primary energy consumption. Over time, there has been notable growth in renewable energy, with significant increases in solar and wind energy since the early 2000s. Conversely, fossil fuel consumption experienced periods of rapid growth during industrialization and economic booms, followed by stagnation or slight declines in some regions due to policy changes and shifts toward cleaner energy sources.



### Overview
This project visualizes global primary energy consumption from 1800 to 2023 using an interactive area chart. The data is sourced from the **Energy Institute** and **Smil (2017)** and follows the "substitution method" for energy conversion.

The visualization presents trends in primary energy sources such as renewables, nuclear, fossil fuels, and biomass.

### Directory Structure
```
📁 global-energy-substitution
├── global-energy-substitution.csv          # Historical energy consumption data
├── global-energy-substituition.py           # Python script for creating the area chart
├── global-energy-substituition.html         # Exported interactive HTML area chart
├── global-energy-substitution.metadata.json # Metadata file with details about the dataset
└── global-energy-substitution.png           # Static PNG of the visualization
```

### Chart Description
- **Title:** Global Primary Energy Consumption by Source (1800–2023)
- **Energy Sources:** Includes coal, oil, gas, renewables, nuclear, and traditional biomass.
- **Visualization Type:** Stacked area chart illustrating the growth of each energy source over time.

![global-energy-substitution/global-energy-substitution.png](https://github.com/cbilinski101/Project-3/blob/main/global-energy-substitution/global-energy-substitution.png?raw=true)

### How to Run
1. Install the necessary libraries:
   ```bash
   pip install pandas plotly
   ```
2. Update the script with the local file path for the CSV:
   ```python
   file_path_global = "./global-energy-substitution.csv"
   ```
3. Run the Python script:
   ```bash
   python global-energy-substituition.py
   ```
4. Open `global-energy-substituition.html` in your browser to view the interactive chart.

---

## **2. Per Capita Primary Energy Consumption by Source**

This section analyzes the variation in per capita energy use across countries. The data highlights that countries such as the United States and industrialized European nations tend to have higher per capita energy consumption, driven by industrial demand and living standards. In contrast, developing nations often show lower per capita use, though some may exhibit rising trends due to economic growth. Additionally, the sources of energy vary by region: for example, European countries may have a larger share of nuclear and renewables, while other regions rely more heavily on fossil fuels.

### Overview
This project visualizes per capita energy consumption for select countries in 2023 using a stacked bar chart. The data is sourced from the **Energy Institute - Statistical Review of World Energy (2024)** and various population datasets.

The visualization compares energy consumption per person for different countries, highlighting how the consumption of coal, oil, gas, renewables, nuclear, and other sources varies.

### Directory Structure
```
📁 per-capita-energy
├── per-capita-energy-stacked.csv           # Dataset containing energy consumption per capita
├── per-capita-energy.py                    # Python script for creating the bar chart
├── per-capita-energy.html                   # Exported interactive HTML bar chart
├── per-capita-energy-stacked.metadata.json  # Metadata file detailing the dataset
└── per-capita-energy.png                    # Static PNG of the visualization
```

### Chart Description
- **Title:** Per Capita Primary Energy Consumption by Source (2023)
- **Energy Sources:** Coal, oil, gas, nuclear, hydro, wind, solar, and other renewables.
- **Countries Covered:** United States, China, India, France, Germany, and others.
- **Visualization Type:** Stacked bar chart showing the breakdown of energy sources for each country.

![per-capita-energy/per-capita-energy.png](https://github.com/cbilinski101/Project-3/blob/main/per-capita-energy/per-capita-energy.png?raw=true)

### How to Run
1. Install dependencies:
   ```bash
   pip install pandas plotly
   ```
2. Update the script with the local file path for the CSV:
   ```python
   file_path = "./per-capita-energy-stacked.csv"
   ```
3. Execute the script:
   ```bash
   python per-capita-energy.py
   ```
4. Open `per-capita-energy.html` to view the interactive bar chart.

---

## **3. Share of Electricity Production from Renewables**

This section includes insights on regional leaders in renewable electricity production. For example, European countries like Denmark and Germany lead in wind energy adoption due to strong policy support, while nations like Iceland and Norway generate significant electricity from hydropower due to abundant natural resources. The map visualization highlights these trends and shows how renewable shares vary globally, often influenced by policies, geographical advantages, and economic factors.

### Overview
This choropleth map visualizes the share of electricity produced from renewable sources across the world in 2023 using a choropleth map. The data is sourced from **Ember** and the **Energy Institute - Statistical Review of World Energy (2024)**.

The visualization presents how much of each country's electricity is generated by renewables, including hydropower, solar, wind, biomass, waste, geothermal, wave, and tidal sources.

### Directory Structure
```
📁 share-electricity-renewables
├── share-electricity-renewables.csv         # Dataset containing electricity production data by country
├── share-electricity-renewables.py          # Python script for creating the choropleth map
├── share-electricity-renewables.html        # Exported interactive HTML choropleth map
├── share-electricity-renewables.metadata.json # Metadata file with detailed descriptions
└── share-electricity-renewables.png         # Static PNG of the map visualization
```

### Map Description
- **Title:** Share of Electricity Production from Renewables (2023)
- **Coverage:** Global, with data for individual countries.
- **Visualization Type:** Choropleth map showing the percentage of electricity produced from renewable sources.

![share-electricity-renewables/share-electricity-renewables.png](https://github.com/cbilinski101/Project-3/blob/main/share-electricity-renewables/share-electricity-renewables.png?raw=true)

### How to Run
1. Install the required libraries:
   ```bash
   pip install pandas plotly
   ```
2. Update the script with the local file path for the CSV:
   ```python
   file_path_renewables = "./share-electricity-renewables.csv"
   ```
3. Run the script:
   ```bash
   python share-electricity-renewables.py
   ```
4. Open `share-electricity-renewables.html` in your browser to view the interactive map.

---

## **Dependencies**
The following Python packages and modules are required to run the scripts in this repository:

1. **pandas** – for reading and manipulating `.csv` files  
2. **plotly** – for creating interactive visualizations (`.html` exports of area charts, bar charts, and choropleth maps)  
3. **json** (built-in) – for reading and handling `.json` metadata files  
4. **os** (built-in) – for handling file paths if needed  
5. **sys** (built-in) – for command-line interactions (if applicable)  

**Performance Notes**: When working with large datasets, consider using efficient file loading methods and optimizing rendering settings in Plotly (e.g., disabling animations or using lower granularity).

**File Formats and Dependencies**:
- **CSV Files** – Read using `pandas.read_csv()`  
- **HTML Export** – Generated using `plotly` functions such as `plotly.Figure().write_html()`  

### Additional Dependencies (if applicable):
- **geopandas** and **shapely** – for enhanced choropleth map support  
- **numpy** – for numerical operations (if used in preprocessing)

### Python Version:
- Ensure Python `>= 3.8` is installed 

---

## **Deployment Method**
The visualizations can be deployed using **GitHub Pages** for easy access and sharing.

1. Navigate to the repository's deployment settings: [GitHub Pages Deployment](https://github.com/cbilinski101/Project-3/deployments/github-pages).
2. Ensure the `index.html` file in the main directory is set as the entry point for the project.
3. Access the deployed project via the GitHub Pages URL provided in the repository.

**Device Compatibility Notes**: The visualizations have been tested for rendering on desktop and mobile devices. While interactive elements work well on desktops, some mobile devices may experience slower rendering or difficulty with interactive hover features. For best performance, use a modern browser (e.g., Chrome, Firefox) and ensure your browser is up to date.

---

## **Main Directory Structure**
```
.
├── LICENSE                      # Licensing information
├── README.md                    # Documentation for the entire project
└── index.html                    # Entry point linking to all visualizations
```

---

## **Data Sources and Notes**
- **Global Primary Energy Consumption:** Data sourced from *Energy Institute - Statistical Review of World Energy (2024)* and *Vaclav Smil (2017)*.
- **Per Capita Energy Consumption:** The data covers 1965 to 2023 and includes detailed population-adjusted figures.
- **Electricity from Renewables:** Data from *Ember (2024)* and *Energy Institute - Statistical Review of World Energy (2024)*.

### Citation
Please use the following citation when referencing this project:
```
Energy Institute - Statistical Review of World Energy (2024); Population data from various sources (2023).
```

