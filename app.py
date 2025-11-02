import pandas as pd
import pgeocode
from geopy.distance import geodesic
from flask import Flask, render_template, request

app = Flask(__name__)

def find_nearest_zip(zip_code, df):
    nomi = pgeocode.Nominatim('us')
    target = nomi.query_postal_code(zip_code)
    target_coords = (target.latitude, target.longitude)

    df['zip_code'] = df['zip_code'].astype(str).str.replace(r'\D', '', regex=True).str.strip()
    unique_zips = df['zip_code'].drop_duplicates()

    distances = []
    for z in unique_zips:
        loc = nomi.query_postal_code(z)
        if pd.notnull(loc.latitude) and pd.notnull(loc.longitude):
            dist = geodesic(target_coords, (loc.latitude, loc.longitude)).miles
            distances.append((z, loc.latitude, loc.longitude, dist))

    nearest = sorted(distances, key=lambda x: x[3])[0]
    return nearest[0], nearest[1], nearest[2]  # zip, lat, lon

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    zip_code = request.form['zip'].strip()

    nomi = pgeocode.Nominatim('us')
    location = nomi.query_postal_code(zip_code)
    lat = location.latitude
    lon = location.longitude

    df = pd.read_csv('helpers.csv')
    df.columns = df.columns.str.strip()
    df['zip_code'] = df['zip_code'].astype(str).str.replace(r'\D', '', regex=True).str.strip()

    filtered_df = df[df['zip_code'] == zip_code]

    if filtered_df.empty:
        nearest_zip, lat, lon = find_nearest_zip(zip_code, df)
        filtered_df = df[df['zip_code'] == nearest_zip]
        zip_code = nearest_zip  # Update for display

    print("FILTERED ROW COUNT:", len(filtered_df))

    results = []
    for _, row in filtered_df.iterrows():
        print("ROW DEBUG:", row.to_dict())

        name = str(row.get("organization_name", "")).strip()
        display_address = str(row.get("display_address", "")).strip().lower()
        address = "" if display_address == "false" else display_address
        if not address:
            address = str(row.get("street_address", "")).strip()

        phone = str(row.get("main_phone_number", "")).strip()
        email = str(row.get("email_address", "")).strip()
        hours = str(row.get("office_hours", "")).strip()

        results.append({
            "name": name or "Unnamed Organization",
            "address": address or "No address listed",
            "phone": phone or "No phone listed",
            "email": email,
            "hours": hours
        })

    if not results:
        results = [{"name": "No resources found for this ZIP", "address": "", "phone": ""}]

    return render_template('results.html', zip_code=zip_code, lat=lat, lon=lon, results=results)

if __name__ == '__main__':
    app.run(debug=True)