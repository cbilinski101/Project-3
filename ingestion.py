# ingestion.py

import requests
import psycopg2
import io
import csv

# -- URLs of the CSV datasets --
URL_GLOBAL_ENERGY_SUBSTITUTION = "https://ourworldindata.org/grapher/global-energy-substitution.csv?v=1&csvType=full&useColumnShortNames=false"
URL_SHARE_OF_RENEWABLES        = "https://ourworldindata.org/grapher/share-electricity-renewables.csv?v=1&csvType=full&useColumnShortNames=false"
URL_PER_CAPITA_ENERGY          = "https://ourworldindata.org/grapher/per-capita-energy-stacked.csv?v=1&csvType=full&useColumnShortNames=false"

def download_csv(url: str) -> io.StringIO:
    """
    Downloads a CSV file from a given URL and returns a StringIO object.
    """
    print(f"Downloading CSV data from {url} ...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if download failed
    csv_data = response.text
    return io.StringIO(csv_data)

def create_tables(conn):
    """
    Creates the tables in PostgreSQL if they don't exist.
    """
    create_global_energy_table = """
    CREATE TABLE IF NOT EXISTS global_energy_substitution (
        id SERIAL PRIMARY KEY,
        entity TEXT,
        code TEXT,
        year INT,
        other_renewables FLOAT,
        biofuels FLOAT,
        solar FLOAT,
        wind FLOAT,
        hydropower FLOAT,
        nuclear FLOAT,
        gas FLOAT,
        oil FLOAT,
        coal FLOAT,
        traditional_biomass FLOAT
    );
    """

    create_share_renewables_table = """
    CREATE TABLE IF NOT EXISTS share_electricity_renewables (
        id SERIAL PRIMARY KEY,
        entity TEXT,
        code TEXT,
        year INT,
        renewables_pct_electricity FLOAT
    );
    """

    create_per_capita_energy_table = """
    CREATE TABLE IF NOT EXISTS per_capita_energy (
        id SERIAL PRIMARY KEY,
        entity TEXT,
        code TEXT,
        year INT,
        coal_per_capita FLOAT,
        oil_per_capita FLOAT,
        gas_per_capita FLOAT,
        nuclear_per_capita FLOAT,
        hydro_per_capita FLOAT,
        wind_per_capita FLOAT,
        solar_per_capita FLOAT,
        other_renewables_per_capita FLOAT
    );
    """

    with conn.cursor() as cur:
        cur.execute(create_global_energy_table)
        cur.execute(create_share_renewables_table)
        cur.execute(create_per_capita_energy_table)
        conn.commit()
    print("Tables created or already exist.")

def insert_global_energy_substitution(conn, csv_file: io.StringIO):
    """
    Inserts data into the global_energy_substitution table.
    """
    reader = csv.DictReader(csv_file)
    rows = []
    for row in reader:
        # Convert empty strings to None
        rows.append((
            row['Entity'] or None,
            row['Code'] or None,
            int(row['Year']) if row['Year'] else None,
            float(row['Other renewables (TWh, substituted energy)']) if row['Other renewables (TWh, substituted energy)'] else None,
            float(row['Biofuels (TWh, substituted energy)']) if row['Biofuels (TWh, substituted energy)'] else None,
            float(row['Solar (TWh, substituted energy)']) if row['Solar (TWh, substituted energy)'] else None,
            float(row['Wind (TWh, substituted energy)']) if row['Wind (TWh, substituted energy)'] else None,
            float(row['Hydropower (TWh, substituted energy)']) if row['Hydropower (TWh, substituted energy)'] else None,
            float(row['Nuclear (TWh, substituted energy)']) if row['Nuclear (TWh, substituted energy)'] else None,
            float(row['Gas (TWh, substituted energy)']) if row['Gas (TWh, substituted energy)'] else None,
            float(row['Oil (TWh, substituted energy)']) if row['Oil (TWh, substituted energy)'] else None,
            float(row['Coal (TWh, substituted energy)']) if row['Coal (TWh, substituted energy)'] else None,
            float(row['Traditional biomass (TWh, substituted energy)']) if row['Traditional biomass (TWh, substituted energy)'] else None,
        ))

    insert_query = """
    INSERT INTO global_energy_substitution (
        entity, code, year, 
        other_renewables, biofuels, solar, wind, hydropower, 
        nuclear, gas, oil, coal, traditional_biomass
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE global_energy_substitution;")  # Clear old data
        cur.executemany(insert_query, rows)
        conn.commit()
    print("Inserted data into global_energy_substitution table.")

def insert_share_renewables(conn, csv_file: io.StringIO):
    """
    Inserts data into the share_electricity_renewables table.
    """
    reader = csv.DictReader(csv_file)
    rows = []
    for row in reader:
        rows.append((
            row['Entity'] or None,
            row['Code'] or None,
            int(row['Year']) if row['Year'] else None,
            float(row['Renewables - % electricity']) if row['Renewables - % electricity'] else None
        ))

    insert_query = """
    INSERT INTO share_electricity_renewables (
        entity, code, year, renewables_pct_electricity
    )
    VALUES (%s, %s, %s, %s)
    """

    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE share_electricity_renewables;")
        cur.executemany(insert_query, rows)
        conn.commit()
    print("Inserted data into share_electricity_renewables table.")

def insert_per_capita_energy(conn, csv_file: io.StringIO):
    """
    Inserts data into the per_capita_energy table.
    """
    reader = csv.DictReader(csv_file)
    rows = []
    for row in reader:
        rows.append((
            row['Entity'] or None,
            row['Code'] or None,
            int(row['Year']) if row['Year'] else None,
            float(row['Coal per capita (kWh)']) if row['Coal per capita (kWh)'] else None,
            float(row['Oil per capita (kWh)']) if row['Oil per capita (kWh)'] else None,
            float(row['Gas per capita (kWh)']) if row['Gas per capita (kWh)'] else None,
            float(row['Nuclear per capita (kWh - equivalent)']) if row['Nuclear per capita (kWh - equivalent)'] else None,
            float(row['Hydro per capita (kWh - equivalent)']) if row['Hydro per capita (kWh - equivalent)'] else None,
            float(row['Wind per capita (kWh - equivalent)']) if row['Wind per capita (kWh - equivalent)'] else None,
            float(row['Solar per capita (kWh - equivalent)']) if row['Solar per capita (kWh - equivalent)'] else None,
            float(row['Other renewables per capita (kWh - equivalent)']) if row['Other renewables per capita (kWh - equivalent)'] else None
        ))

    insert_query = """
    INSERT INTO per_capita_energy (
        entity, code, year,
        coal_per_capita, oil_per_capita, gas_per_capita,
        nuclear_per_capita, hydro_per_capita, wind_per_capita,
        solar_per_capita, other_renewables_per_capita
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE per_capita_energy;")
        cur.executemany(insert_query, rows)
        conn.commit()
    print("Inserted data into per_capita_energy table.")

def main():
    # Database connection parameters
    db_host = "localhost"
    db_name = "energy"
    db_user = "postgres"
    db_password = "postgres"
    db_port = 5432

    # Establish connection
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )

    try:
        # Create tables if not exist
        create_tables(conn)

        # Download CSV data
        csv_global_energy = download_csv(URL_GLOBAL_ENERGY_SUBSTITUTION)
        csv_share_renewables = download_csv(URL_SHARE_OF_RENEWABLES)
        csv_per_capita = download_csv(URL_PER_CAPITA_ENERGY)

        # Insert data
        insert_global_energy_substitution(conn, csv_global_energy)
        insert_share_renewables(conn, csv_share_renewables)
        insert_per_capita_energy(conn, csv_per_capita)

    finally:
        conn.close()

if __name__ == "__main__":
    main()