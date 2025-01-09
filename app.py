# app.py

from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Replace with your own database credentials
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'energy',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )
    return conn

@app.route("/api/global_energy_substitution", methods=["GET"])
def get_global_energy_substitution():
    """
    Returns all global energy substitution data or filtered by year if provided.
    Example: /api/global_energy_substitution?year=2020
    """
    year_filter = request.args.get("year", None)
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if year_filter:
                cur.execute("""
                    SELECT * FROM global_energy_substitution WHERE year = %s
                    ORDER BY year ASC
                """, (year_filter,))
            else:
                cur.execute("""
                    SELECT * FROM global_energy_substitution ORDER BY year ASC
                """)
            records = cur.fetchall()
    finally:
        conn.close()

    return jsonify(records), 200

@app.route("/api/share_renewables", methods=["GET"])
def get_share_renewables():
    """
    Returns all share of electricity from renewables data or filtered by year if provided.
    Example: /api/share_renewables?year=2020
    """
    year_filter = request.args.get("year", None)
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if year_filter:
                cur.execute("""
                    SELECT * FROM share_electricity_renewables WHERE year = %s
                    ORDER BY year ASC
                """, (year_filter,))
            else:
                cur.execute("""
                    SELECT * FROM share_electricity_renewables ORDER BY year ASC
                """)
            records = cur.fetchall()
    finally:
        conn.close()

    return jsonify(records), 200

@app.route("/api/per_capita_energy", methods=["GET"])
def get_per_capita_energy():
    """
    Returns all per capita energy data or filtered by year and/or entity if provided.
    Example: /api/per_capita_energy?year=2020&entity=United States
    """
    year_filter = request.args.get("year", None)
    entity_filter = request.args.get("entity", None)
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            base_query = "SELECT * FROM per_capita_energy"
            params = []
            conditions = []

            if year_filter:
                conditions.append("year = %s")
                params.append(year_filter)
            if entity_filter:
                conditions.append("entity = %s")
                params.append(entity_filter)

            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)

            base_query += " ORDER BY year ASC"
            cur.execute(base_query, tuple(params))
            records = cur.fetchall()
    finally:
        conn.close()

    return jsonify(records), 200

if __name__ == "__main__":
    app.run(debug=True)
