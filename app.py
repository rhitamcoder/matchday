from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://api.football-data.org/v4"
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
# export FOOTBALL_DATA_API_KEY="YOUR_API_KEY_HERE"

COMPETITIONS = {
    "BSA": "Campeonato Brasileiro Série A",
    "ELC": "Championship",
    "PL": "Premier League",
    "CL": "UEFA Champions League",
    "EC": "European Championship",
    "FL1": "Ligue 1",
    "BL1": "Bundesliga",
    "SA": "Serie A",
    "DED": "Eredivisie",
    "PPL": "Primeira Liga",
    "CLI": "Copa Libertadores",
    "PD": "Primera Division",
    "WC": "FIFA World Cup"
}

def get_standings(competition_code):
    """Fetch league standings from football-data.org"""

    if not API_KEY:
        print("ERROR: FOOTBALL_DATA_API_KEY is not set.")
        return []

    url = f"{API_URL}/competitions/{competition_code}/standings"

    headers = {
        "X-Auth-Token": API_KEY
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        #football-data.org returns standings
        #inside the "standings" list.
        if not data.get("standings"):
            return []

        #We want the TOTAL league table.
        for standing in data["standings"]:
            if standing.get("type") == "TOTAL":
                return standing.get("table", [])

        return []

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        return []

    except ValueError:
        print("API returned invalid JSON.")
        return []

def get_fixtures(competition_code):
    if not API_KEY:
        print("ERROR: FOOTBALL_DATA_API_KEY is not set.")
        return []

    url = f"{API_URL}/competitions/{competition_code}/matches"
    headers = {"X-Auth-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data.get("matches", [])

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        return []

    except ValueError:
        print("API returned invalid JSON.")
        return []

@app.route("/")
def home():
    selected_competition = request.args.get(
        "competition",
        "PL"
    )

    #Prevent invalid competition codes
    if selected_competition not in COMPETITIONS:
        selected_competition = "PL"

    standings = get_standings(
        selected_competition
    )

    fixtures = get_fixtures(
        selected_competition
    )

    return render_template(
        "index.html",
        competitions=COMPETITIONS,
        selected_competition=selected_competition,
        standings=standings,
        fixtures=fixtures
    )

if __name__ == "__main__":
    app.run(debug=True)




# For Testing -->
# import requests

# headers = {
#     "X-Auth-Token": "API-KEY"
# }

# response = requests.get("https://api.football-data.org/v4/competitions", headers=headers)
# data = response.json()

# for comp in data["competitions"]:
#     print(comp["code"], "-", comp["name"])
