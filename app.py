import streamlit as st
import pandas as pd
import datetime
import swisseph as swe

st.set_page_config(
    page_title="Universal Multi-Framework Vedic Astro Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. Multi-Language Full Dictionary (₹51 Shagun Offer) ---
L_DATA = {
    "English": {
        "title": "⚡ Universal Multi-Framework Vedic Astro Engine",
        "subtitle": "Synthesized Ephemeris Engine: BPHS (Parashari) | Jaimini Sutras | KP Cuspal System | K.N. Rao Timing",
        "input_header": "1. Enter Birth Data & Planetary Coordinates",
        "dob": "Date of Birth",
        "tob": "Time of Birth",
        "hour": "Hour",
        "min": "Minute",
        "city": "Birth City / Place",
        "lat": "Latitude",
        "lon": "Longitude",
        "btn_free": "🔮 Generate Natal Chart & Free Assessment",
        "prem_banner": "👑 UNLOCK COMPLETE MULTI-FRAMEWORK PREDICTION REPORT",
        "prem_desc": "Get deep evidence-based synthesis covering BPHS Planetary States, KP Star & Sub-Lord Analysis, Jaimini Soul Blueprint, and Exact Event Timing Windows.",
        "pay_btn": "💳 Pay ₹51 (Shubh Shagun Offer)",
        "pass_prompt": "Already paid? Enter UPI Transaction Ref No / Code:",
        "unlock_btn": "Unlock Complete Report",
        "tab_free1": "📊 Planetary Coordinates & Lagna",
        "tab_free2": "🌟 Classical Yogas (BPHS)",
        "tab_prem1": "🪐 BPHS Deep Synthesis & Avasthas",
        "tab_prem2": "💎 Jaimini Karaka Blueprint",
        "tab_prem3": "⚡ KP (Krishnamurti) Cuspal Signifiers",
        "tab_prem4": "⏱️ K.N. Rao Event Timing & Vimshottari",
        "unlocked_msg": "🎉 Premium Multi-Framework Report Unlocked!"
    },
    "मराठी": {
        "title": "⚡ सर्वसमावेशक बहुआयामी वैदिक ज्योतिष प्लॅटफॉर्म",
        "subtitle": "अचूक गणितीय पद्धती: पराशरी BPHS | जैमिनी सूत्रे | केपी (KP) कस्पल पद्धत | के.एन. राव टाइमिंग",
        "input_header": "१. जन्म तपशील आणि अक्षांश/रेखांश",
        "dob": "जन्मतारीख",
        "tob": "जन्म वेळ",
        "hour": "तास",
        "min": "मिनिट",
        "city": "जन्म शहर / ठिकाण",
        "lat": "अक्षांश (Latitude)",
        "lon": "रेखांश (Longitude)",
        "btn_free": "🔮 मोफत कुंडली व प्राथमिक विश्लेषण पाहा",
        "prem_banner": "👑 संपूर्ण सखोल भविष्यकथन रिपोर्ट अनलॉक करा (शुभ शगुन ऑफर)",
        "prem_desc": "पराशरी ग्रहावस्था, केपी नक्षत्र व सब-लॉर्ड विश्लेषण, जैमिनी आत्मकारक व करिअर-विवाह अचूक टाईमलाईन एकाच ठिकाणी मिळवा.",
        "pay_btn": "💳 फक्त ₹५१ भरा आणि संपूर्ण रिपोर्ट अनलॉक करा",
        "pass_prompt": "पेमेंट केले असल्यास UPI Ref नंबर / Transaction ID टाका:",
        "unlock_btn": "प्रीमियम रिपोर्ट अनलॉक करा",
        "tab_free1": "📊 ग्रहस्थिती आणि लग्न",
        "tab_free2": "🌟 कुंडलीतील राजयोग (BPHS)",
        "tab_prem1": "🪐 पराशरी BPHS सखोल फलित व अवस्था",
        "tab_prem2": "💎 जैमिनी चर कारके आणि आत्मिक हेतू",
        "tab_prem3": "⚡ केपी (KP) कस्पल व नक्षत्र विश्लेषण",
        "tab_prem4": "⏱️ के.एन. राव इव्हेंट टाइमिंग व दशा",
        "unlocked_msg": "🎉 अभिनंदन! तुमचा संपूर्ण सखोल रिपोर्ट यशस्वीरीत्या अनलॉक झाला आहे!"
    },
    "हिंदी": {
        "title": "⚡ सार्वभौमिक वैदिक ज्योतिष प्रेडिक्शन इंजन",
        "subtitle": "समेकित सिद्धांत: पाराशरी (BPHS) | जैमिनी सूत्र | केपी (KP) पद्धति | के.एन. राव टाइमिंग",
        "input_header": "१. जन्म विवरण और अक्षांश/देशांतर",
        "dob": "जन्म तिथि",
        "tob": "जन्म समय",
        "hour": "घंटा",
        "min": "मिनट",
        "city": "जन्म स्थान / शहर",
        "lat": "अक्षांश (Latitude)",
        "lon": "देशांतर (Longitude)",
        "btn_free": "🔮 जन्म कुंडली और निःशुल्क विश्लेषण देखें",
        "prem_banner": "👑 संपूर्ण विस्तृत भविष्यफल रिपोर्ट अनलॉक करें (शुभ शगुन ऑफर)",
        "prem_desc": "पाराशरी ग्रह अवस्थाएं, केपी उप-स्वामी विश्लेषण, जैमिनी आत्मकारक और जीवन की प्रमुख घटनाओं की सटीक समय-सारणी प्राप्त करें।",
        "pay_btn": "💳 मात्र ₹51 का भुगतान करके पूरी रिपोर्ट अनलॉक करें",
        "pass_prompt": "भुगतान किया है? UPI Ref संख्या / Transaction ID दर्ज करें:",
        "unlock_btn": "प्रीमियम रिपोर्ट अनलॉक करें",
        "tab_free1": "📊 ग्रह स्थिति और लग्न",
        "tab_free2": "🌟 शास्त्रीय राजयोग (BPHS)",
        "tab_prem1": "🪐 पाराशरी BPHS फलित व अवस्थाएं",
        "tab_prem2": "💎 जैमिनी चर कारक और आत्मिक उद्देश्य",
        "tab_prem3": "⚡ केपी (KP) नक्षत्र व कस्पल विश्लेषण",
        "tab_prem4": "⏱️ के.एन. राव घटना समय व दशा",
        "unlocked_msg": "🎉 बधाई! आपकी संपूर्ण रिपोर्ट अनलॉक हो चुकी है!"
    },
    "ગુજરાતી": {
        "title": "⚡ યુનિવર્સલ વૈદિક જ્યોતિષ એન્જિન",
        "subtitle": "સિદ્ધાંતો: પરાશરી (BPHS) | જૈમિની સૂત્રો | કેપી સિસ્ટમ | કે.એન. રાવ ટાઈમિંગ",
        "input_header": "૧. જન્મ વિગતો દાખલ કરો",
        "dob": "જન્મ તારીખ",
        "tob": "જન્મ સમય",
        "hour": "કલાક",
        "min": "મિનિટ",
        "city": "જન્મ સ્થળ",
        "lat": "અક્ષાંશ (Latitude)",
        "lon": "રેખાંશ (Longitude)",
        "btn_free": "🔮 મફત કુંડળી અને વિશ્લેષણ જુઓ",
        "prem_banner": "👑 સંપૂર્ણ પ્રીમિયમ રિપોર્ટ અનલોક કરો (શુભ શગુન ઓફર)",
        "prem_desc": "પરાશરી અવસ્થાઓ, કેપી નક્ષત્ર સબ-લોર્ડ, જૈમિની આત્મકારક અને મહત્વપૂર્ણ જીવન ઘટનાઓનો સમય મેળવો.",
        "pay_btn": "💳 માત્ર ₹51 ચૂકવીને સંપૂર્ણ રિપોર્ટ મેળવો",
        "pass_prompt": "પેમેન્ટ કર્યું હોય તો UPI Ref નંબર દાખલ કરો:",
        "unlock_btn": "પ્રીમિયમ રિપોર્ટ અનલોક કરો",
        "tab_free1": "📊 ગ્રહ સ્થિતિ અને લગ્ન",
        "tab_free2": "🌟 ક્લાસિકલ રાજયોગ",
        "tab_prem1": "🪐 પરાશરી BPHS વિશ્લેષણ",
        "tab_prem2": "💎 જૈમિની ચર કારક",
        "tab_prem3": "⚡ કેપી (KP) કસ્પલ સિગ્નિફાયર",
        "tab_prem4": "⏱️ કે.એન. રાવ ટાઈમિંગ અને દશા",
        "unlocked_msg": "🎉 પ્રીમિયમ રિપોર્ટ અનલોક થઈ ગયો છે!"
    }
}

# --- 2. Language Selection Bar ---
c_head, c_lang = st.columns([3, 1])
with c_lang:
    selected_lang = st.selectbox("🌐 Select Language / भाषा:", list(L_DATA.keys()), index=0)

T = L_DATA[selected_lang]

with c_head:
    st.title(T["title"])
    st.caption(T["subtitle"])

# --- 3. Input Form ---
with st.form("main_form"):
    st.subheader(T["input_header"])
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        dob = st.date_input(T["dob"], value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    with c2:
        t_hour = st.selectbox(T["hour"], [f"{i:02d}" for i in range(1, 13)], index=9)
    with c3:
        t_min = st.selectbox(T["min"], [f"{i:02d}" for i in range(0, 60)], index=40)
    with c4:
        t_ampm = st.selectbox("AM/PM", ["AM", "PM"], index=0)
        
    p1, p2, p3 = st.columns([2, 1, 1])
    with p1:
        place = st.text_input(T["city"], value="Sangamner, Maharashtra")
    with p2:
        lat = st.number_input(T["lat"], value=19.5761, format="%.4f")
    with p3:
        lon = st.number_input(T["lon"], value=74.2070, format="%.4f")
        
    submitted = st.form_submit_button(T["btn_free"])

# --- 4. Ephemeris Constants & Setup ---
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", 
    "Leo", "Virgo", "Libra", "Scorpio", 
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    ("Ashwini", "Ketu", 7), ("Bharani", "Venus", 20), ("Krittika", "Sun", 6),
    ("Rohini", "Moon", 10), ("Mrigashira", "Mars", 7), ("Ardra", "Rahu", 18),
    ("Punarvasu", "Jupiter", 16), ("Pushya", "Saturn", 19), ("Ashlesha", "Mercury", 17),
    ("Magha", "Ketu", 7), ("Purva Phalguni", "Venus", 20), ("Uttara Phalguni", "Sun", 6),
    ("Hasta", "Moon", 10), ("Chitra", "Mars", 7), ("Swati", "Rahu", 18),
    ("Vishakha", "Jupiter", 16), ("Anuradha", "Saturn", 19), ("Jyeshtha", "Mercury", 17),
    ("Mula", "Ketu", 7), ("Purva Ashadha", "Venus", 20), ("Uttara Ashadha", "Sun", 6),
    ("Shravana", "Moon", 10), ("Dhanishta", "Mars", 7), ("Shatabhisha", "Rahu", 18),
    ("Purva Bhadrapada", "Jupiter", 16), ("Uttara Bhadrapada", "Saturn", 19), ("Revati", "Mercury", 17)
]

PLANET_MAP = {
    swe.SUN: "Sun", swe.MOON: "Moon", swe.MARS: "Mars",
    swe.MERCURY: "Mercury", swe.JUPITER: "Jupiter", swe.VENUS: "Venus",
    swe.SATURN: "Saturn", swe.TRUE_NODE: "Rahu"
}

def compute_ephemeris(dob, hour, minute, ampm, lat, lon):
    h = int(hour)
    if ampm == "PM" and h != 12:
        h += 12
    elif ampm == "AM" and h == 12:
        h = 0
    t_dec_ist = h + (int(minute) / 60.0)
    t_dec_utc = t_dec_ist - 5.5
    cal_date = dob
    if t_dec_utc < 0:
        t_dec_utc += 24.0
        cal_date = dob - datetime.timedelta(days=1)
    elif t_dec_utc >= 24.0:
        t_dec_utc -= 24.0
        cal_date = dob + datetime.timedelta(days=1)
        
    jd = swe.julday(cal_date.year, cal_date.month, cal_date.day, t_dec_utc)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    asc_sign_idx = int(asc_deg // 30)
    
    planets = {}
    for p_id, p_name in PLANET_MAP.items():
        res, _ = swe.calc_ut(jd, p_id, flags)
        lon_deg = res[0]
        s_idx = int(lon_deg // 30)
        nak_num = int(lon_deg // (360/27))
        star_lord = NAKSHATRAS[nak_num][1]
        deg_in_sign = lon_deg % 30
        
        if deg_in_sign <= 6.0:
            avastha = "Balyavastha (Inception)"
        elif deg_in_sign <= 12.0:
            avastha = "Kumaravastha (Youth)"
        elif deg_in_sign <= 18.0:
            avastha = "Yuvavastha (Peak Power)"
        elif deg_in_sign <= 24.0:
            avastha = "Vriddhavastha (Mature)"
        else:
            avastha = "Mritavastha (Transcendence)"
            
        planets[p_name] = {
            "deg": deg_in_sign,
            "sign": ZODIAC_SIGNS[s_idx],
            "house": ((s_idx - asc_sign_idx) % 12) + 1,
            "full_deg": lon_deg,
            "star_lord": star_lord,
            "avastha": avastha
        }
        
    rahu_deg = planets["Rahu"]["full_deg"]
    ketu_deg = (rahu_deg + 180.0) % 360.0
    k_s_idx = int(ketu_deg // 30)
    k_nak = int(ketu_deg // (360/27))
    planets["Ketu"] = {
        "deg": ketu_deg % 30,
        "sign": ZODIAC_SIGNS[k_s_idx],
        "house": ((k_s_idx - asc_sign_idx) % 12) + 1,
        "full_deg": ketu_deg,
        "star_lord": NAKSHATRAS[k_nak][1],
        "avastha": "Karmic Axis Node"
    }
    return planets, {"sign": ZODIAC_SIGNS[asc_sign_idx], "deg": asc_deg % 30}

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if submitted:
    st.session_state.computed = True
    st.session_state.dob = dob
    st.session_state.t_hour = t_hour
    st.session_state.t_min = t_min
    st.session_state.t_ampm = t_ampm
    st.session_state.lat = lat
    st.session_state.lon = lon

if st.session_state.get("computed", False):
    planets, lagna = compute_ephemeris(
        st.session_state.dob, st.session_state.t_hour, st.session_state.t_min, 
        st.session_state.t_ampm, st.session_state.lat, st.session_state.lon
    )
    
    st.success(f"✅ Lagna: **{lagna['sign']} ({lagna['deg']:.2f}°)** | Location: **{place}**")
    
    # Free Tabs
    f_tab1, f_tab2 = st.tabs([T["tab_free1"], T["tab_free2"]])
    with f_tab1:
        st.subheader("Natal Coordinates & House Placements")
        p_list = []
        for p, d in planets.items():
            p_list.append({
                "Planet": p, "Sign": d["sign"], "Degree": f"{d['deg']:.2f}°",
                "House": f"House {d['house']}", "KP Star Lord": d["star_lord"]
            })
        st.dataframe(pd.DataFrame(p_list), use_container_width=True)
        
    with f_tab2:
        st.subheader("Fundamental Classical Yogas")
        h_sun, h_mer = planets["Sun"]["house"], planets["Mercury"]["house"]
        h_jup, h_moon = planets["Jupiter"]["house"], planets["Moon"]["house"]
        if h_sun == h_mer:
            st.success("✨ **Budhaditya Yoga (Sun + Mercury):** Active in House " + str(h_sun) + ". Sharp intellect & analytical mastery.")
        if ((h_jup - h_moon) % 12) in [0, 3, 6, 9]:
            st.success("✨ **Gaja Kesari Yoga (Jupiter Kendra from Moon):** Social standing, protection & enduring honor.")

    # --- MONETIZATION SECTION WITH LIVE UPI ---
    st.markdown("---")
    if not st.session_state.unlocked:
        st.warning(f"### {T['prem_banner']}")
        st.write(T["prem_desc"])
        
        my_upi_id = "gordeyogesh0003@okhdfcbank"
        upi_pay_link = f"upi://pay?pa={my_upi_id}&pn=Yogesh%20Gorde&am=51&cu=INR&tn=Complete%20Vedic%20Astrology%20Report"
        
        pay_col1, pay_col2 = st.columns([1, 1])
        with pay_col1:
            st.markdown("#### Step 1: Pay ₹51 via UPI App")
            st.write("Click below on your mobile or scan to pay **₹51 (Shubh Shagun)** via GPay / PhonePe / Paytm:")
            st.code(f"UPI ID: {my_upi_id}\nName: Yogesh Gorde\nAmount: ₹51", language="text")
            st.markdown(f"[👉 **Click here to Open UPI App & Pay ₹51**]({upi_pay_link})")
            
        with pay_col2:
            st.markdown("#### Step 2: Instant Report Unlock")
            access_code = st.text_input(T["pass_prompt"], placeholder="Enter UPI Ref No. or Passcode")
            if st.button(T["unlock_btn"]):
                if access_code.strip() != "":
                    st.session_state.unlocked = True
                    st.rerun()
                else:
                    st.error("Please enter a valid reference / code.")
                    
    # Premium Content
    if st.session_state.unlocked:
        st.balloons()
        st.info(T["unlocked_msg"])
        
        p_tab1, p_tab2, p_tab3, p_tab4 = st.tabs([
            T["tab_prem1"], T["tab_prem2"], T["tab_prem3"], T["tab_prem4"]
        ])
        
        with p_tab1:
            st.header("1. Parashari BPHS Planetary States (Avasthas)")
            av_data = [{"Planet": p, "Sign": d["sign"], "Degree": f"{d['deg']:.2f}°", "Avastha": d["avastha"]} for p, d in planets.items()]
            st.table(pd.DataFrame(av_data))
            
        with p_tab2:
            st.header("2. Jaimini Sutras & Chara Karakas")
            seven = {k: v for k, v in planets.items() if k not in ["Rahu", "Ketu"]}
            sorted_p = sorted(seven.items(), key=lambda x: x[1]['deg'], reverse=True)
            k_names = ["Atmakaraka (AK)", "Amatyakaraka (AmK)", "Bhratrukaraka (BK)", "Matrukaraka (MK)", "Putrakaraka (PK)", "Gnatikaraka (GK)", "Darakaraka (DK)"]
            j_list = [{"Karaka Role": k_names[i], "Planet": p_name, "Degree": f"{p_info['deg']:.2f}°", "House": f"House {p_info['house']}"} for i, (p_name, p_info) in enumerate(sorted_p)]
            st.dataframe(pd.DataFrame(j_list), use_container_width=True)
            st.success(f"**Atmakaraka (Soul Purpose):** `{sorted_p[0][0]}` | **Amatyakaraka (Career Power):** `{sorted_p[1][0]}` | **Darakaraka (Spouse Indicator):** `{sorted_p[6][0]}`")

        with p_tab3:
            st.header("3. KP (Krishnamurti) Cuspal System")
            kp_matrix = [{"Planet": p, "House": d["house"], "Star Lord": d["star_lord"], "Signification Trigger": f"Houses {d['house']}, {((d['house']+4)%12 or 12)}, {((d['house']+8)%12 or 12)}"} for p, d in planets.items()]
            st.dataframe(pd.DataFrame(kp_matrix), use_container_width=True)
            
        with p_tab4:
            st.header("4. K.N. Rao Timing & Double Transit")
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                st.success("💼 **Career Peak & Independent Enterprise Window**")
                st.write("Double transit of Saturn and Jupiter triggering 10th and 11th houses activates independent authority and commercial expansion.")
            with c_t2:
                st.warning("💍 **Marriage & Alliance Window**")
                st.write("Transit Jupiter aspecting 7th house lord or Darakaraka confirms marital alliance timing.")
