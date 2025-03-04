import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
import json

# Conversion functions
def km_to_miles(km): return km / 1.609
def miles_to_km(miles): return miles * 1.609
def kg_to_lb(kg): return kg * 2.205
def lb_to_kg(lb): return lb / 2.205
def inches_to_cm(inches): return inches * 2.54
def cm_to_inches(cm): return cm / 2.54
def celsius_to_fahrenheit(celsius): return (celsius * 9/5) + 32
def fahrenheit_to_celsius(fahrenheit): return (fahrenheit - 32) * 5/9
def liters_to_gallons(liters): return liters * 0.264172
def gallons_to_liters(gallons): return gallons / 0.264172
def sqft_to_sqm(sqft): return sqft * 0.092903
def sqm_to_sqft(sqm): return sqm / 0.092903
def kmh_to_mph(kmh): return kmh / 1.609
def mph_to_kmh(mph): return mph * 1.609
def bar_to_psi(bar): return bar * 14.5038
def psi_to_bar(psi): return psi / 14.5038
def minutes_to_seconds(minutes): return minutes * 60
def seconds_to_minutes(seconds): return seconds / 60

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Load history & favorites from file
def load_data():
    try:
        with open("history.json", "r") as f:
            data = json.load(f)
            st.session_state.conversion_history = data.get("history", [])
            st.session_state.favorites = data.get("favorites", [])
    except FileNotFoundError:
        st.session_state.conversion_history = []
        st.session_state.favorites = []

def save_data():
    with open("history.json", "w") as f:
        json.dump({"history": st.session_state.conversion_history, "favorites": st.session_state.favorites}, f)

load_data()

# Custom CSS for better UI
st.markdown("""
<style>
    body { font-family: Arial, sans-serif; }
    .header { background-color: #3498db; color: white; padding: 2rem; border-radius: 12px; text-align: center; }
    .result { font-size: 1.5rem; font-weight: bold; padding: 1rem; background-color: #f0f0f0; border-radius: 8px; text-align: center; }
    .stButton > button { background-color: #2980b9; color: white; padding: 10px; border-radius: 8px; width: 100%; }
    .stButton > button:hover { opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="header"><h1>🌐 Advanced Unit Converter</h1></div>', unsafe_allow_html=True)

# Theme toggle button
theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
if st.button(f"{theme_icon} Toggle Theme"):
    toggle_theme()
    st.rerun()

# Conversion categories
categories = {
    "📏 Length": ["Kilometers to Miles", "Miles to Kilometers", "Inches to Centimeters", "Centimeters to Inches"],
    "⚖️ Weight": ["Kilograms to Pounds", "Pounds to Kilograms"],
    "🌡️ Temperature": ["Celsius to Fahrenheit", "Fahrenheit to Celsius"],
    "🧊 Volume": ["Liters to Gallons", "Gallons to Liters"],
    "📐 Area": ["Square Feet to Square Meters", "Square Meters to Square Feet"],
    "🚗 Speed": ["Kilometers per hour to Miles per hour", "Miles per hour to Kilometers per hour"],
    "⚙️ Pressure": ["Bar to PSI", "PSI to Bar"],
    "⏳ Time": ["Minutes to Seconds", "Seconds to Minutes"]
}

# Category selection
category = st.radio("Select a category:", list(categories.keys()))
options = categories[category]

# Conversion UI
col1, col2 = st.columns([2, 1])
with col1:
    choice = st.selectbox("Choose a conversion:", options)
with col2:
    value = st.number_input("Enter value:", format="%.6f")

# Perform conversion
if st.button("Convert"):
    conversions = {
        "Kilometers to Miles": (km_to_miles, "miles"),
        "Miles to Kilometers": (miles_to_km, "kilometers"),
        "Kilograms to Pounds": (kg_to_lb, "pounds"),
        "Pounds to Kilograms": (lb_to_kg, "kilograms"),
        "Inches to Centimeters": (inches_to_cm, "centimeters"),
        "Centimeters to Inches": (cm_to_inches, "inches"),
        "Celsius to Fahrenheit": (celsius_to_fahrenheit, "°F"),
        "Fahrenheit to Celsius": (fahrenheit_to_celsius, "°C"),
        "Liters to Gallons": (liters_to_gallons, "gallons"),
        "Gallons to Liters": (gallons_to_liters, "liters"),
        "Square Feet to Square Meters": (sqft_to_sqm, "square meters"),
        "Square Meters to Square Feet": (sqm_to_sqft, "square feet"),
        "Kilometers per hour to Miles per hour": (kmh_to_mph, "mph"),
        "Miles per hour to Kilometers per hour": (mph_to_kmh, "km/h"),
        "Bar to PSI": (bar_to_psi, "psi"),
        "PSI to Bar": (psi_to_bar, "bar"),
        "Minutes to Seconds": (minutes_to_seconds, "seconds"),
        "Seconds to Minutes": (seconds_to_minutes, "minutes"),
    }

    result, unit = conversions[choice][0](value), conversions[choice][1]
    st.markdown(f'<div class="result">{value:.4f} {choice.split(" to ")[0]} = {result:.4f} {unit}</div>', unsafe_allow_html=True)

    # Save to history
    st.session_state.conversion_history.append(f"{value:.4f} {choice.split(' to ')[0]} = {result:.4f} {unit}")
    save_data()

# Fun Fact Section
fun_facts = [
    "The metric system is used by 95% of the world.",
    "The Fahrenheit scale was created in 1724.",
    "A marathon is exactly 42.195 kilometers or 26.2 miles.",
    "One gallon of water weighs 8.34 pounds."
]
st.subheader("💡 Fun Fact")
st.write(random.choice(fun_facts))

# History
if st.session_state.conversion_history:
    st.subheader("🕒 Conversion History")
    for conv in st.session_state.conversion_history[-5:]:
        st.write(conv)

# Favorites
if st.button("Add to Favorites") and 'result' in locals():
    fav_entry = f"{value:.4f} {choice.split(' to ')[0]} = {result:.4f} {unit}"
    if fav_entry not in st.session_state.favorites:
        st.session_state.favorites.append(fav_entry)
        save_data()

if st.session_state.favorites:
    st.subheader("⭐ Favorites")
    for fav in st.session_state.favorites:
        st.write(fav)

st.markdown("---")
st.markdown("Created with ❤️ by ARMEEN NADEEM | [GitHub](https://github.com/armeennadeem197)")
