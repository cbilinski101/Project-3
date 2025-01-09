import os
import requests
import pandas as pd
import plotly.express as px

# -------------------------------------------------------------------------
# 1. Define Metadata for Our Visualizations
# -------------------------------------------------------------------------
visualizations_info = {
    "global_energy_substitution": {
        "title": "Global Energy Substitution",
        "filename": "global_energy_substitution.html",
        "description": (
            "Explore the evolution of primary energy consumption "
            "by source from 1800–2023."
        )
    },
    "per_capita_energy": {
        "title": "Per Capita Energy",
        "filename": "per_capita_energy.html",
        "description": (
            "Compare per capita energy consumption by country, "
            "focusing on top consumers."
        )
    },
    "share_of_renewables": {
        "title": "Share of Renewables",
        "filename": "share_of_renewables.html",
        "description": (
            "See how renewable energy adoption varies across the globe "
            "with an interactive map."
        )
    },
}

# -------------------------------------------------------------------------
# 2. Shared HTML Templates
# -------------------------------------------------------------------------
HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Energy Visualizations</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0; 
            padding: 0;
            background-color: #f9f9f9;
            color: #333;
        }
        header {
            background-color: #222;
            color: #fff;
            padding: 20px 30px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
        header h1 {
            margin: 0;
            font-weight: 500;
        }
        main {
            padding: 30px;
        }
        footer {
            background-color: #222;
            color: #fff;
            padding: 20px 30px;
            margin-top: 30px;
            text-align: center;
        }
        footer p {
            margin: 0;
            font-size: 0.9rem;
        }
        .chart-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        /* Grid for recommended visualizations + Home */
        .visualizations-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-top: 40px;
        }
        .card {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            flex: 1 1 300px; /* each card will be at least 300px wide */
            max-width: 350px;
            padding: 20px;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .card h3 {
            margin-top: 0;
            margin-bottom: 10px;
            font-weight: 500;
        }
        .card p {
            margin-bottom: 20px;
            line-height: 1.4;
        }
        .card .btn {
            background-color: #222;
            color: #fff;
            text-decoration: none;
            padding: 10px 16px;
            border-radius: 4px;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        .card .btn:hover {
            background-color: #444;
        }
    </style>
</head>
<body>
<header>
    <h1>Energy Visualizations</h1>
</header>
<main>
<div class="chart-container">
"""

FOOTER = """
</div>
<footer>
    <p>&copy; 2023 Energy Insights. All rights reserved.</p>
</footer>
</main>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 3. Utility: Generate "Suggested Visualizations" & "Home" HTML
# -------------------------------------------------------------------------
def generate_suggested_visualizations_html(current_key):
    """
    Given the key for the current visualization, return HTML cards
    for the other two, plus a card that leads 'Home'.
    """
    other_keys = [k for k in visualizations_info.keys() if k != current_key]
    
    html_cards = ['<section class="visualizations-grid">']
    
    # 1) Cards for the other two visualizations
    for key in other_keys:
        info = visualizations_info[key]
        card_html = f"""
        <div class="card">
            <h3>{info['title']}</h3>
            <p>{info['description']}</p>
            <a class="btn" href="{info['filename']}">View</a>
        </div>
        """
        html_cards.append(card_html)
    
    # 2) Card to go back to the Home page (index.html is one level above 'visualizations')
    home_card = """
    <div class="card">
        <h3>Home</h3>
        <p>Return to the homepage to explore more content or learn more.</p>
        <a class="btn" href="../index.html">Go Home</a>
    </div>
    """
    html_cards.append(home_card)

    html_cards.append("</section>")
    
    return "\n".join(html_cards)


# -------------------------------------------------------------------------
# 4. Visualization Functions
# -------------------------------------------------------------------------
def global_energy_substitution_plot(api_url, output_html):
    resp = requests.get(api_url)
    data = resp.json()
    df = pd.DataFrame(data)

    # Convert numeric columns
    numeric_cols = [
        'other_renewables', 'biofuels', 'solar', 'wind',
        'hydropower', 'nuclear', 'gas', 'oil', 'coal', 'traditional_biomass'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    fig = px.area(
        df.sort_values(by="year"),
        x="year",
        y=numeric_cols,
        title="Global Primary Energy Consumption by Source (1800–2023)",
        labels={'value': 'TWh (Substituted Energy)', 'year': 'Year'},
    )
    fig_html = fig.to_html(full_html=False)
    
    suggested_html = generate_suggested_visualizations_html("global_energy_substitution")

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write(fig_html)
        f.write(suggested_html)
        f.write(FOOTER)

    print(f"Global energy substitution chart saved to {output_html}")


def per_capita_energy_plot(api_url, output_html, filter_year=2023):
    params = {'year': filter_year}
    resp = requests.get(api_url, params=params)
    data = resp.json()
    df = pd.DataFrame(data)

    df = df[df['entity'].notna()]

    numeric_cols = [
        'coal_per_capita', 'oil_per_capita', 'gas_per_capita',
        'nuclear_per_capita', 'hydro_per_capita', 'wind_per_capita',
        'solar_per_capita', 'other_renewables_per_capita'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['total_per_capita'] = df[numeric_cols].sum(axis=1)
    df = df.sort_values(by='total_per_capita', ascending=False).head(15)

    df_melted = df.melt(
        id_vars=['entity'],
        value_vars=numeric_cols,
        var_name='energy_source',
        value_name='kWh_per_capita'
    )

    fig = px.bar(
        df_melted,
        x="entity",
        y="kWh_per_capita",
        color="energy_source",
        title=f"Per Capita Primary Energy Consumption by Source ({filter_year})",
        labels={'kWh_per_capita': 'kWh per Capita', 'entity': 'Country/Region'}
    )
    fig.update_layout(barmode='stack')

    fig_html = fig.to_html(full_html=False)
    suggested_html = generate_suggested_visualizations_html("per_capita_energy")

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write(fig_html)
        f.write(suggested_html)
        f.write(FOOTER)

    print(f"Per capita energy consumption chart saved to {output_html}")


def share_of_renewables_plot(api_url, output_html, filter_year=2023):
    params = {'year': filter_year}
    resp = requests.get(api_url, params=params)
    data = resp.json()
    df = pd.DataFrame(data)

    df['renewables_pct_electricity'] = pd.to_numeric(
        df['renewables_pct_electricity'], errors='coerce'
    ).fillna(0)
    df['code'] = df['code'].fillna('')

    fig = px.choropleth(
        df,
        locations="code",
        color="renewables_pct_electricity",
        hover_name="entity",
        color_continuous_scale="Greens",
        range_color=(0, 100),
        title=f"Share of Electricity Production from Renewables ({filter_year})",
        labels={'renewables_pct_electricity': '% Renewables'}
    )
    
    fig_html = fig.to_html(full_html=False)
    suggested_html = generate_suggested_visualizations_html("share_of_renewables")

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write(fig_html)
        f.write(suggested_html)
        f.write(FOOTER)

    print(f"Share of renewables map saved to {output_html}")


# -------------------------------------------------------------------------
# 5. Main Script
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Adjust these if your local API is on a different host/port
    GLOBAL_ENERGY_API = "http://127.0.0.1:5000/api/global_energy_substitution"
    PER_CAPITA_API     = "http://127.0.0.1:5000/api/per_capita_energy"
    RENEWABLES_API     = "http://127.0.0.1:5000/api/share_renewables"

    # Create output directory if needed
    os.makedirs("visualizations", exist_ok=True)

    global_energy_html    = os.path.join(
        "visualizations", visualizations_info["global_energy_substitution"]["filename"]
    )
    per_capita_html       = os.path.join(
        "visualizations", visualizations_info["per_capita_energy"]["filename"]
    )
    share_renewables_html = os.path.join(
        "visualizations", visualizations_info["share_of_renewables"]["filename"]
    )

    global_energy_substitution_plot(GLOBAL_ENERGY_API, global_energy_html)
    per_capita_energy_plot(PER_CAPITA_API, per_capita_html, filter_year=2023)
    share_of_renewables_plot(RENEWABLES_API, share_renewables_html, filter_year=2023)
