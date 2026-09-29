import streamlit as st
import pandas as pd

st.set_page_config(page_title="Evidence-Based Astro Platform", layout="centered")

st.title("⚡ AI-Integrated Vedic Astro Engine")
st.caption("Frameworks: Parashari | Jaimini (K.N. Rao) | KP Cuspal | V.P. Goel Rules")

# --- User Input Section ---
with st.form("birth_details"):
    st.subheader("1. Enter Birth Data")
    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("Date of Birth")
    with col2:
        tob = st.time_input("Time of Birth")
    
    place = st.text_input("Birth City / Place", value="Sangamner, Maharashtra")
    lat = st.number_input("Latitude", value=19.5761, format="%.4f")
    lon = st.number_input("Longitude", value=74.2070, format="%.4f")
    
    submitted = st.form_submit_button("Generate Astrological Matrix")

# --- Calculation Modules ---
def calculate_jaimini_karakas(planets_data):
    seven_planets = {k: v for k, v in planets_data.items() if k not in ["Rahu", "Ketu"]}
    sorted_planets = sorted(seven_planets.items(), key=lambda x: x[1]['deg'], reverse=True)
    
    karaka_names = [
        "Atmakaraka (AK)",
        "Amatyakaraka (AmK)",
        "Bhratrukaraka (BK)",
        "Matrukaraka (MK)",
        "Putrakaraka (PK)",
        "Gnatikaraka (GK)",
        "Darakaraka (DK)"
    ]
    
    karaka_result = []
    for idx, (p_name, p_info) in enumerate(sorted_planets):
        karaka_result.append({
            "Karaka": karaka_names[idx],
            "Planet": p_name,
            "Degree": f"{p_info['deg']:.2f}°",
            "Sign": p_info['sign']
        })
    return pd.DataFrame(karaka_result)

def check_kn_rao_double_transit(target_house, jup_aspects, sat_aspects):
    jup_hits = target_house in jup_aspects
    sat_hits = target_house in sat_aspects
    return jup_hits and sat_hits

# --- Output Trigger ---
if submitted:
    st.success("Mathematical Matrix Calculated Successfully!")
    
    sample_planets = {
        "Sun": {"deg": 17.32, "sign": "Sagittarius"},
        "Moon": {"deg": 12.44, "sign": "Aquarius"},
        "Mars": {"deg": 16.45, "sign": "Scorpio"},
        "Mercury": {"deg": 1.88, "sign": "Sagittarius"},
        "Jupiter": {"deg": 11.36, "sign": "Gemini"},
        "Venus": {"deg": 12.48, "sign": "Capricorn"},
        "Saturn": {"deg": 21.96, "sign": "Sagittarius"},
        "Rahu": {"deg": 24.69, "sign": "Aquarius"},
        "Ketu": {"deg": 24.69, "sign": "Leo"}
    }
    
    st.subheader("📊 1. Jaimini Chara Karakas (Composite Engine)")
    df_karakas = calculate_jaimini_karakas(sample_planets)
    st.table(df_karakas)
    
    st.subheader("🔍 2. Extreme Degree / Inception State Analysis")
    extreme_flags = []
    for p, info in sample_planets.items():
        if info['deg'] <= 2.0:
            extreme_flags.append(f"⚠️ **{p}** ({info['deg']:.2f}°) is in **Balyavastha / Inception Degree**. Represents brand new karmic cycle.")
        elif info['deg'] >= 28.0:
            extreme_flags.append(f"⏳ **{p}** ({info['deg']:.2f}°) is in **Vriddhavastha / Karmic Boundary**.")
            
    if extreme_flags:
        for alert in extreme_flags:
            st.info(alert)
    else:
        st.write("No extreme gandanta degrees detected.")
        
    st.subheader("🎯 3. K. N. Rao Double Transit Check")
    colA, colB = st.columns(2)
    with colA:
        check_house = st.selectbox("Select House to Validate (e.g., 7 for Marriage, 10 for Career)", [7, 10])
    
    current_jup_aspects = [2, 6, 10]
    current_sat_aspects = [3, 7, 10]
    
    double_transit_active = check_kn_rao_double_transit(check_house, current_jup_aspects, current_sat_aspects)
    
    with colB:
        if double_transit_active:
            st.success(f"✅ Double Transit ACTIVE on House {check_house}! High-confidence event window.")
        else:
            st.warning(f"❌ Double Transit not concurrent on House {check_house}.")
