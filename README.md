# ⚽ Matchday

**Live standings and upcoming fixtures, straight from the source.**

Matchday is a Flask web app powered by the [football-data.org](https://www.football-data.org/) API. Pick a league from the dropdown, from the Premier League to the FIFA World Cup, and instantly see the current standings table alongside upcoming fixtures, team crests included.

---

## ✨ Features

- 🏆 **13 supported competitions**, including the Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Champions League, Copa Libertadores, and the FIFA World Cup
- 📊 **Full standings table** — position, played, won, drawn, lost, goal difference, and points, with team crests
- 📅 **Upcoming fixtures list**, showing match date and both competing teams with their crests
- 🔄 **League switcher** — change competitions instantly via a dropdown, no page reload logic needed beyond a simple GET request
- 🛡️ **Graceful fallbacks** — invalid competition codes default safely to the Premier League, and missing data shows a clean empty state instead of breaking the page
- 🔐 **API key kept out of the code**, loaded from an environment variable

---

## 🛠️ Tech Stack

- **Python 3** + **Flask** — routing and server-side logic
- **requests** — calling the football-data.org API
- **Jinja2** — server-side templating
- **HTML5 / CSS3** — custom-styled dark-mode frontend, no CSS framework
- **Google Fonts** — JetBrains Mono (headings/data) & Inter (body)
- **[football-data.org](https://www.football-data.org/)** — live football data API

---

## 📁 Project Structure

```
matchday/
├── app.py                  # Flask application (API calls + routing)
├── templates/
│   └── index.html          # Main page template (Jinja2)
├── static/
│   └── style.css           # Stylesheet
└── README.md
```

---

## ▶️ Getting Started

### Prerequisites

```
pip install flask requests
```

### Get a football-data.org API Key

1. Sign up for a free account at [football-data.org](https://www.football-data.org/client/register)
2. Copy your API key (token) from your account dashboard

### Set Up Your Environment

Set the `FOOTBALL_DATA_API_KEY` environment variable before running the app:

```
export FOOTBALL_DATA_API_KEY="your_api_key_here"
```

(On Windows: `set FOOTBALL_DATA_API_KEY=your_api_key_here`)

### Running the App

```
git clone https://github.com/rhitamcoder/matchday.git
```
```
cd matchday
```
```
python app.py
```

The app will start in debug mode at `http://127.0.0.1:5000/`. Pick a league from the dropdown to see its standings and fixtures.

---

## 🧠 How It Works

- **`get_standings()`** calls the `/competitions/{code}/standings` endpoint and extracts the `"TOTAL"` type table (as opposed to home-only or away-only splits)
- **`get_fixtures()`** calls the `/competitions/{code}/matches` endpoint and returns the full matches list
- Both functions **fail safely**: a missing API key, a failed request, or malformed JSON all return an empty list and print an error, rather than crashing the app
- The **`home()`** route reads the selected competition from the query string, validates it against the known `COMPETITIONS` dictionary (defaulting to the Premier League if invalid), fetches standings and fixtures, and renders them into the page

---

## 🔐 Security Note

The API key is read entirely from the `FOOTBALL_DATA_API_KEY` environment variable via `os.getenv()`. No key is hardcoded anywhere in the source, so nothing sensitive is included in this repo.

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
