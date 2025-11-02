# Healthcare Resource Navigator 

A Flask-based web app that helps users find treatment resources by ZIP code and insurance type. Built to support real-time access to care in underserved communities.

## Features

- Search by ZIP code and insurance type
- Interactive map view using Leaflet.js
- Smart filtering with mock data (CSV-ready)
- Clean, responsive layout with custom CSS

## Demo

![screenshot](static/demo.png)  
*Search results with map view*

## Setup

```bash
git clone https://github.com/yourusername/healthcare-navigator.git
cd healthcare-navigator
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install flask
python app.py