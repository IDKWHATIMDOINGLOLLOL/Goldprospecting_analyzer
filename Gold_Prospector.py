import streamlit as st
import math

# --- Simulated datasets ---
known_gold_coords = [
    (44.2, -92.65),  # Oronoco - known flakes
    (44.4, -92.75),  # Upper Zumbro
    (44.1, -92.55)   # Rochester
]

glacial_zones = [
    (44.0, -92.7),
    (44.3, -92.6),
    (44.25, -92.65)
]

# --- Functions ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def analyze_location(lat, lon):
    report = {}

    # Distance to known gold
    gold_distances = [haversine(lat, lon, g_lat, g_lon) for g_lat, g_lon in known_gold_coords]
    nearest_gold_km = min(gold_distances)
    report['Nearest known gold site (km)'] = round(nearest_gold_km, 2)

    # Glacial gold zone check
    glacial_hit = any(haversine(lat, lon, g_lat, g_lon) <= 10 for g_lat, g_lon in glacial_zones)
    report['Glacial gold zone'] = "Yes" if glacial_hit else "No"

    # Prospecting potential logic
    if nearest_gold_km < 5 and glacial_hit:
        report['Prospecting Potential'] = "High – Strong chance for flakes or pickers"
    elif nearest_gold_km < 10 or glacial_hit:
        report['Prospecting Potential'] = "Moderate – Check gravel bars and high benches"
    else:
        report['Prospecting Potential'] = "Low – Unlikely to yield gold"

    return report

# --- Streamlit App ---
st.title("Gold Prospecting Potential Analyzer")
st.markdown("Enter a set of GPS coordinates (like from Google Maps) to check prospecting potential.")

lat = st.number_input("Latitude", format="%.6f")
lon = st.number_input("Longitude", format="%.6f")

if st.button("Analyze Location"):
    result = analyze_location(lat, lon)
    st.subheader("Analysis Report")
    for key, value in result.items():
        st.write(f"**{key}:** {value}")

initial commit
