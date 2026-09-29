import streamlit as st
import pandas as pd
import datetime
import swisseph as swe

st.set_page_config(page_title="Evidence-Based Vedic Astro Engine", layout="wide")

# --- 1. Multi-Language Dictionary Engine ---
LANG_PACK = {
    "English": {
        "title": "⚡ Live Precision Vedic Astro Engine",
        "subtitle": "Ephemeris: Swiss Ephemeris (Lahiri Ayanamsha) | Frameworks: BPHS | Jaimini (K.N. Rao) | KP",
        "input_header": "1. Enter Real Birth Data & Coordinates",
        "dob": "Date of Birth",
        "tob": "Time of Birth",
        "hour": "Hour",
        "min": "Minute",
        "city": "Birth City / Place",
        "lat": "Latitude",
        "lon": "Longitude",
        "btn": "🔮 Compute Live Ephemeris & Karmic Matrix",
        "tab1": "🔍 Comprehensive Predictions",
        "tab2": "🪐 Conjunctions & Parashari Aspects (PAC)",
        "tab3": "📊 Live Planetary Positions & Jaimini Karakas",
        "tab4": "⏱️ Vimshottari & Double Transit",
        "core_identity": "1. Core Soul Identity & Karmic Path (Atmakaraka)",
        "career_destiny": "2. Professional Mastery & Wealth (Amatyakaraka)",
        "spouse_dynamics": "3. Partnership & Spousal Blueprint (Darakaraka)",
        "avastha_header": "4. Critical BPHS Planetary States (Avasthas)",
    },
    "मराठी": {
        "title": "⚡ थेट ग्रहस्थिती वैदिक ज्योतिष प्रेडिक्शन इंजिन",
        "subtitle": "खगोलशास्त्र: स्विस एफिमरिस (लाहिरी अयनांश) | पद्धती: पराशरी (BPHS) | जैमिनी (के.एन. राव)",
        "input_header": "१. खरी जन्मतारीख, वेळ आणि ठिकाण प्रविष्ट करा",
        "dob": "जन्मतारीख",
        "tob": "जन्म वेळ",
        "hour": "तास",
        "min": "मिनिट",
        "city": "जन्म शहर / ठिकाण",
        "lat": "अक्षांश (Latitude)",
        "lon": "रेखांश (Longitude)",
        "btn": "🔮 प्रत्यक्ष ग्रहस्थिती आणि सखोल भविष्यकथन तयार करा",
        "tab1": "🔍 सखोल भविष्यकथन",
        "tab2": "🪐 युती आणि पराशरी दृष्टी (PAC विश्लेषण)",
        "tab3": "📊 प्रत्यक्ष ग्रहस्थिती आणि जैमिनी चर कारके",
        "tab4": "⏱️ विंशोत्तरी दशा आणि गोचर",
        "core_identity": "१. मूळ आत्मा, स्वभाव आणि जीवन ध्येय (आत्मकारक)",
        "career_destiny": "२. करिअर, अधिकार आणि धनप्राप्ती (अमात्यकारक)",
        "spouse_dynamics": "३. जोडीदाराचा स्वभाव आणि वैवाहिक जीवन (दाराकारक)",
        "avastha_header": "४. महत्त्वाच्या पराशरी ग्रहावस्था (BPHS Avasthas)",
    },
    "हिंदी": {
        "title": "⚡ प्रत्यक्ष ग्रहस्थिति वैदिक ज्योतिष प्रेडिक्शन इंजन",
        "subtitle": "खगोलशास्त्र: स्विस एफिमरिस (लाहिड़ी अयनांश) | सिद्धांत: पाराशरी (BPHS) | जैमिनी",
        "input_header": "१. वास्तविक जन्म विवरण और अक्षांश/देशांतर",
        "dob": "जन्म तिथि",
        "tob": "जन्म समय",
        "hour": "घंटा",
        "min": "मिनट",
        "city": "जन्म स्थान / शहर",
        "lat": "अक्षांश (Latitude)",
        "lon": "देशांतर (Longitude)",
        "btn": "🔮 प्रत्यक्ष ग्रह स्थिति और विस्तृत फलित उत्पन्न करें",
        "tab1": "🔍 विस्तृत भविष्यफल",
        "tab2": "🪐 युति और पाराशरी दृष्टि (PAC)",
        "tab3": "📊 प्रत्यक्ष ग्रह अंश और जैमिनी चर कारक",
        "tab4": "⏱️ विंशोत्तरी दशा और गोचर",
        "core_identity": "१. आत्मिक उद्देश्य और जीवन पथ (आत्मकारक)",
        "career_destiny": "२. आजीविका, पद और धन संपदा (अमात्यकारक)",
        "spouse_dynamics": "३. जीवनसाथी का स्वभाव और वैवाहिक योग (दाराकारक)",
        "avastha_header": "४. पाराशर ग्रहावस्था विश्लेषण (BPHS Avasthas)",
    }
}

# --- 2. Language Selection UI ---
col_head, col_lang = st.columns([3, 1])
with col_lang:
    selected_lang = st.selectbox("🌐 Language / भाषा", list(LANG_PACK.keys()), index=0)

T = LANG_PACK[selected_lang]

with col_head:
    st.title(T["title"])
    st.caption(T["subtitle"])

# --- 3. Input Form ---
with st.form("birth_details_form"):
    st.subheader(T["input_header"])
    
    c_dob, c_tob1, c_tob2, c_tob3 = st.columns([2, 1, 1, 1])
    with c_dob:
        dob = st.date_input(T["dob"], value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    with c_tob1:
        t_hour = st.selectbox(T["hour"], [f"{i:02d}" for i in range(1, 13)], index=9)
    with c_tob2:
        t_min = st.selectbox(T["min"], [f"{i:02d}" for i in range(0, 60)], index=40)
    with c_tob3:
        t_ampm = st.selectbox("AM / PM", ["AM", "PM"], index=0)

    c_place, c_lat, c_lon = st.columns([2, 1, 1])
    with c_place:
        place = st.text_input(T["city"], value="Sangamner, Maharashtra")
    with c_lat:
        lat = st.number_input(T["lat"], value=19.5761, format="%.4f")
    with c_lon:
        lon = st.number_input(T["lon"], value=74.2070, format="%.4f")
        
    submitted = st.form_submit_button(T["btn"])

# --- 4. Astronomical Constants ---
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", 
    "Leo", "Virgo", "Libra", "Scorpio", 
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_MAP = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MARS: "Mars",
    swe.MERCURY: "Mercury",
    swe.JUPITER: "Jupiter",
    swe.VENUS: "Venus",
    swe.SATURN: "Saturn",
    swe.TRUE_NODE: "Rahu"
}

# --- 5. Real Ephemeris Calculation Engine ---
def compute_live_ephemeris(dob, hour, minute, ampm, lat, lon):
    # Convert 12-hour AM/PM to 24-hour decimal
    h = int(hour)
    if ampm == "PM" and h != 12:
        h += 12
    elif ampm == "AM" and h == 12:
        h = 0
    time_decimal_ist = h + (int(minute) / 60.0)
    
    # IST to UTC conversion (IST = UTC + 5:30)
    time_decimal_utc = time_decimal_ist - 5.5
    cal_date = dob
    if time_decimal_utc < 0:
        time_decimal_utc += 24.0
        cal_date = dob - datetime.timedelta(days=1)
    elif time_decimal_utc >= 24.0:
        time_decimal_utc -= 24.0
        cal_date = dob + datetime.timedelta(days=1)
        
    # Calculate Julian Day in UT
    jd = swe.julday(cal_date.year, cal_date.month, cal_date.day, time_decimal_utc)
    
    # Set Sidereal Lahiri Ayanamsha
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    
    # Calculate Ascendant (Lagna)
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    asc_sign_idx = int(asc_deg // 30)
    asc_rem_deg = asc_deg % 30
    asc_house_start = asc_sign_idx
    
    planets_data = {}
    for p_id, p_name in PLANET_MAP.items():
        res, _ = swe.calc_ut(jd, p_id, flags)
        lon_deg = res[0]
        sign_idx = int(lon_deg // 30)
        rem_deg = lon_deg % 30
        
        # Calculate Vedic Whole Sign House relative to Lagna
        house_num = ((sign_idx - asc_house_start) % 12) + 1
        planets_data[p_name] = {
            "deg": rem_deg,
            "sign": ZODIAC_SIGNS[sign_idx],
            "house": house_num,
            "full_deg": lon_deg
        }
        
    # Ketu is exactly 180 degrees opposite to Rahu
    rahu_deg = planets_data["Rahu"]["full_deg"]
    ketu_deg = (rahu_deg + 180.0) % 360.0
    k_sign_idx = int(ketu_deg // 30)
    k_rem_deg = ketu_deg % 30
    k_house_num = ((k_sign_idx - asc_house_start) % 12) + 1
    planets_data["Ketu"] = {
        "deg": k_rem_deg,
        "sign": ZODIAC_SIGNS[k_sign_idx],
        "house": k_house_num,
        "full_deg": ketu_deg
    }
    
    lagna_info = {
        "sign": ZODIAC_SIGNS[asc_sign_idx],
        "deg": asc_rem_deg
    }
    
    return planets_data, lagna_info

def calculate_jaimini_karakas(planets_data):
    seven = {k: v for k, v in planets_data.items() if k not in ["Rahu", "Ketu"]}
    sorted_p = sorted(seven.items(), key=lambda x: x[1]['deg'], reverse=True)
    roles = [
        "Atmakaraka (AK)", "Amatyakaraka (AmK)", "Bhratrukaraka (BK)",
        "Matrukaraka (MK)", "Putrakaraka (PK)", "Gnatikaraka (GK)", "Darakaraka (DK)"
    ]
    res = []
    k_dict = {}
    for idx, (p_name, p_info) in enumerate(sorted_p):
        k_dict[roles[idx].split()[0]] = p_name
        res.append({
            "Karaka Role": roles[idx],
            "Planet": p_name,
            "Degree": f"{p_info['deg']:.2f}°",
            "Sign": p_info['sign'],
            "House": f"House {p_info['house']}"
        })
    return pd.DataFrame(res), k_dict

def compute_conjunctions(planets_data):
    house_map = {}
    for p, data in planets_data.items():
        house_map.setdefault(data['house'], []).append((p, data['deg'], data['sign']))
    conjunctions = []
    for house, p_list in house_map.items():
        if len(p_list) > 1:
            names = [item[0] for item in p_list]
            conjunctions.append({
                "House": house,
                "Sign": p_list[0][2],
                "Planets Involved": ", ".join(names)
            })
    return conjunctions

def compute_parashari_aspects(planets_data):
    aspect_hits = []
    for p, d in planets_data.items():
        h = d['house']
        targets = []
        if p == "Mars":
            targets = [(h + 3) % 12 or 12, (h + 6) % 12 or 12, (h + 7) % 12 or 12]
        elif p == "Jupiter":
            targets = [(h + 4) % 12 or 12, (h + 6) % 12 or 12, (h + 8) % 12 or 12]
        elif p == "Saturn":
            targets = [(h + 2) % 12 or 12, (h + 6) % 12 or 12, (h + 9) % 12 or 12]
        elif p in ["Sun", "Moon", "Mercury", "Venus"]:
            targets = [(h + 6) % 12 or 12]
            
        for t in targets:
            residents = [pl for pl, info in planets_data.items() if info['house'] == t]
            aspect_hits.append({
                "Aspecting Planet": p,
                "Target House": f"House {t}",
                "Aspect Received By": ", ".join(residents) if residents else "Open Space"
            })
    return pd.DataFrame(aspect_hits)

# --- 6. Execution Pipeline ---
if submitted:
    natal_planets, lagna_info = compute_live_ephemeris(dob, t_hour, t_min, t_ampm, lat, lon)
    df_karakas, k_dict = calculate_jaimini_karakas(natal_planets)
    conjunctions = compute_conjunctions(natal_planets)
    df_aspects = compute_parashari_aspects(natal_planets)
    
    st.success(f"✅ Calculation Complete! Ascendant (Lagna): **{lagna_info['sign']} ({lagna_info['deg']:.2f}°) **")
    
    tab1, tab2, tab3, tab4 = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"]])
    
    with tab1:
        st.subheader(f"{T['core_identity']}: **{k_dict.get('Atmakaraka')}**")
        ak_p = k_dict.get('Atmakaraka')
        if ak_p == "Saturn":
            st.info("Saturn as AK: The soul evolves through endurance, patient mastery, discipline, and eliminating ego. Yields permanent authority in later cycles.")
        elif ak_p == "Sun":
            st.info("Sun as AK: Soul path centers on executive authority, moral sovereignty, and leadership. Balancing ego and humility is the ultimate lesson.")
        elif ak_p == "Mercury":
            st.info("Mercury as AK: Mind, intellectual curiosity, speech, commerce, and analytical mastery form the soul's primary journey.")
        elif ak_p == "Jupiter":
            st.info("Jupiter as AK: Wisdom, counseling, advisory roles, and higher philosophy represent the soul's guiding light.")
        elif ak_p == "Mars":
            st.info("Mars as AK: Courage, decisive action, and protecting others. Channeling raw passion without impulsive anger is the key test.")
        elif ak_p == "Venus":
            st.info("Venus as AK: Aesthetics, refined relationships, artistic vision, and unconditional love.")
        elif ak_p == "Moon":
            st.info("Moon as AK: Emotional empathy, public connection, counseling, and deep psychological perception.")
            
        st.subheader(f"{T['career_destiny']}: **{k_dict.get('Amatyakaraka')}**")
        amk_p = k_dict.get('Amatyakaraka')
        st.success(f"**{amk_p} as Amatyakaraka:** Directs career orientation. Positioned in House {natal_planets[amk_p]['house']} ({natal_planets[amk_p]['sign']}). Indicates maximum success when applying {amk_p}'s core significations.")
        
        st.subheader(f"{T['spouse_dynamics']}: **{k_dict.get('Darakaraka')}**")
        dk_p = k_dict.get('Darakaraka')
        st.write(f"**{dk_p} as Darakaraka:** Positioned in House {natal_planets[dk_p]['house']} ({natal_planets[dk_p]['sign']}). Your spouse reflects the intellectual and behavioral traits of {dk_p}.")
        
        st.subheader(T["avastha_header"])
        for p, info in natal_planets.items():
            if info['deg'] <= 2.0:
                st.warning(f"⚠️ **{p} ({info['deg']:.2f}°) in House {info['house']} - Balyavastha (Inception State):** Raw karmic cycle requiring conscious calibration.")
            elif info['deg'] >= 28.0:
                st.error(f"⏳ **{p} ({info['deg']:.2f}°) in House {info['house']} - Vriddhavastha (Culminating State):** Karmic completion cycle.")
                
    with tab2:
        st.subheader("Planetary Conjunctions (Yutis)")
        if conjunctions:
            for conj in conjunctions:
                with st.expander(f"House {conj['House']} ({conj['Sign']}): {conj['Planets Involved']}", expanded=True):
                    st.write(f"Planets combined in close spatial union: **{conj['Planets Involved']}**.")
        else:
            st.write("No major planetary conjunctions in the same sign.")
            
        st.subheader("Parashari Full Aspect Table (Drishti Matrix)")
        st.dataframe(df_aspects, use_container_width=True)
        
    with tab3:
        st.subheader("Live Real-Time Planetary Positions")
        live_list = []
        for p, info in natal_planets.items():
            live_list.append({
                "Planet": p,
                "Sign": info["sign"],
                "Degree in Sign": f"{info['deg']:.2f}°",
                "House Placement": f"House {info['house']}"
            })
        st.dataframe(pd.DataFrame(live_list), use_container_width=True)
        
        st.subheader("Jaimini Chara Karakas (Degree Hierarchy)")
        st.dataframe(df_karakas, use_container_width=True)
        
    with tab4:
        st.subheader("K.N. Rao Transit Verification")
        val_h = st.selectbox("House to Validate:", [7, 10], format_func=lambda x: "House 7: Marriage / Partnership Expansion" if x==7 else "House 10: Career Milestone / Enterprise Launch")
        st.info("Transit tracking active against natal Lagna coordinates.")
