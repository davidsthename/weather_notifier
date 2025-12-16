# Automated Weather Notifier

**Real-time severe weather alerts with voice notification**  
A beautiful, modular, professional-grade Streamlit app.

## Features

- Monitors any cities you choose
- Custom alert thresholds (heat, cold, wind, rain, storms)
- Speaks alerts out loud (text-to-speech)
- Auto-refreshes every 5 minutes
- No alert spam (max once per hour)
- Clean modular code (5 files – easy to understand)

## What's Included in This ZIP

weather_notifier/
├── .streamlit/
│ └── secrets.toml ← put your API key here
├── main.py ← run this file
├── config.py
├── weather.py
├── alerts.py
├── ui.py
└── README.md ← you are reading this!

## How to Run (Step-by-Step – Works for Everyone!)

### 1. Install Python (if you don't have it)

Download from: https://www.python.org/downloads/  
During installation → **CHECK "Add Python to PATH"**

### 2. Get a FREE OpenWeatherMap API Key

1. Go to: https://openweathermap.org/api
2. Sign up (free) → click "API keys" tab
3. Copy your key (example: `df501581c4b860c65bb33d3dd6af8b71`)

### 3. Put Your API Key in the Secrets File

1. Open the `.streamlit` folder (enable "show hidden files" if needed)
2. Edit `secrets.toml` with Notepad/TextEdit
3. Replace the line with your real key:

```toml
OPENWEATHER_API_KEY = "your_actual_key_here"
```

### 4. Install Required Packages (One Command!)

Open Command Prompt (Windows) or Terminal (Mac/Linux)
Navigate to the unzipped folder and run:

pip install streamlit requests gtts

### 5. Run the App!

In the same terminal, run:
streamlit run main.py

### Breakdown of what each of the 5 files does:

1. main.py → The actual app launcher

This is the file you run.

Streamlit reads it and opens the app in the browser.

2. ui.py → The UI

Contains the Streamlit layout.

Controls what the page looks like.

3. alerts.py → Checks conditions + plays voice alerts
4. weather.py → Fetches data from OpenWeatherMap API
5. config.py → Stores API key and default sliders
