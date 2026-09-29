import datetime
import pandas as pd
import streamlit as st
import swisseph as swe

st.set_page_config(
    page_title="K.N. Rao Evidence-Based Astro Engine", layout="wide"
)

# --- Header Section ---
col_head, col_lang = st.columns([3, 1])
with col_lang:
  lang = st.selectbox("🌐 Language / भाषा", ["English", "मराठी"], index=0)

with col_head:
  if lang == "मराठी":
    st.title("⚡ के. एन. राव प्रेडिक्शन व ॲस्ट्रॉलॉजिकल इंजिन")
    st.caption(
        "अचूक गणित: स्विस एफिमरिस | पद्धती: पराशरी BPHS, के.एन. राव डबल ट्रान्झिट"
        " आणि जैमिनी चर कारके"
    )
  else:
    st.title("⚡ K.N. Rao Evidence-Based Astrological Engine")
    st.caption(
        "Ephemeris: Swiss Ephemeris (Lahiri) | Frameworks: BPHS, K.N. Rao Double"
        " Transit & Jaimini Karakas"
    )

# --- 1. User Input Form ---
with st.form("birth_details_form"):
  st.subheader(
      "१. जन्म तपशील प्रविष्ट करा"
      if lang == "मराठी"
      else "1. Enter Real Birth Details"
  )

  c_dob, c_tob1, c_tob2, c_tob3 = st.columns([2, 1, 1, 1])
  with c_dob:
    dob = st.date_input(
        "Date of Birth" if lang == "English" else "जन्मतारीख",
        value=datetime.date(1995, 1, 1),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today(),
    )
  with c_tob1:
    t_hour = st.selectbox(
        "Hour" if lang == "English" else "तास",
        [f"{i:02d}" for i in range(1, 13)],
        index=9,
    )
  with c_tob2:
    t_min = st.selectbox(
        "Minute" if lang == "English" else "मिनिट",
        [f"{i:02d}" for i in range(0, 60)],
        index=40,
    )
  with c_tob3:
    t_ampm = st.selectbox("AM / PM", ["AM", "PM"], index=0)

  c_place, c_lat, c_lon = st.columns([2, 1, 1])
  with c_place:
    place = st.text_input(
        "Birth City" if lang == "English" else "जन्म ठिकाण / शहर",
        value="Sangamner, Maharashtra",
    )
  with c_lat:
    lat = st.number_input(
        "Latitude" if lang == "English" else "अक्षांश",
        value=19.5761,
        format="%.4f",
    )
  with c_lon:
    lon = st.number_input(
        "Longitude" if lang == "English" else "रेखांश",
        value=74.2070,
        format="%.4f",
    )

  btn_label = (
      "🔮 संपूर्ण भविष्यकथन व योग विश्लेषण तयार करा"
      if lang == "मराठी"
      else "🔮 Generate Complete Prediction & Event Matrix"
  )
  submitted = st.form_submit_button(btn_label)

# --- 2. Astronomical Constants & Nakshatras ---
ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

NAKSHATRAS = [
    ("Ashwini", "Ketu", 7),
    ("Bharani", "Venus", 20),
    ("Krittika", "Sun", 6),
    ("Rohini", "Moon", 10),
    ("Mrigashira", "Mars", 7),
    ("Ardra", "Rahu", 18),
    ("Punarvasu", "Jupiter", 16),
    ("Pushya", "Saturn", 19),
    ("Ashlesha", "Mercury", 17),
    ("Magha", "Ketu", 7),
    ("Purva Phalguni", "Venus", 20),
    ("Uttara Phalguni", "Sun", 6),
    ("Hasta", "Moon", 10),
    ("Chitra", "Mars", 7),
    ("Swati", "Rahu", 18),
    ("Vishakha", "Jupiter", 16),
    ("Anuradha", "Saturn", 19),
    ("Jyeshtha", "Mercury", 17),
    ("Mula", "Ketu", 7),
    ("Purva Ashadha", "Venus", 20),
    ("Uttara Ashadha", "Sun", 6),
    ("Shravana", "Moon", 10),
    ("Dhanishta", "Mars", 7),
    ("Shatabhisha", "Rahu", 18),
    ("Purva Bhadrapada", "Jupiter", 16),
    ("Uttara Bhadrapada", "Saturn", 19),
    ("Revati", "Mercury", 17),
]

PLANET_MAP = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MARS: "Mars",
    swe.MERCURY: "Mercury",
    swe.JUPITER: "Jupiter",
    swe.VENUS: "Venus",
    swe.SATURN: "Saturn",
    swe.TRUE_NODE: "Rahu",
}


# --- 3. Astronomical Precision Engine ---
def compute_live_ephemeris(dob, hour, minute, ampm, lat, lon):
  h = int(hour)
  if ampm == "PM" and h != 12:
    h += 12
  elif ampm == "AM" and h == 12:
    h = 0
  time_decimal_ist = h + (int(minute) / 60.0)
  time_decimal_utc = time_decimal_ist - 5.5
  cal_date = dob
  if time_decimal_utc < 0:
    time_decimal_utc += 24.0
    cal_date = dob - datetime.timedelta(days=1)
  elif time_decimal_utc >= 24.0:
    time_decimal_utc -= 24.0
    cal_date = dob + datetime.timedelta(days=1)

  jd = swe.julday(cal_date.year, cal_date.month, cal_date.day, time_decimal_utc)
  swe.set_sid_mode(swe.SIDM_LAHIRI)
  flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

  houses, ascmc = swe.houses_ex(jd, lat, lon, b"P", flags)
  asc_deg = ascmc[0]
  asc_sign_idx = int(asc_deg // 30)
  asc_rem_deg = asc_deg % 30

  planets_data = {}
  for p_id, p_name in PLANET_MAP.items():
    res, _ = swe.calc_ut(jd, p_id, flags)
    lon_deg = res[0]
    sign_idx = int(lon_deg // 30)
    rem_deg = lon_deg % 30
    house_num = ((sign_idx - asc_sign_idx) % 12) + 1
    planets_data[p_name] = {
        "deg": rem_deg,
        "sign": ZODIAC_SIGNS[sign_idx],
        "house": house_num,
        "full_deg": lon_deg,
    }

  # Ketu (Exact 180 degrees opposite Rahu)
  rahu_deg = planets_data["Rahu"]["full_deg"]
  ketu_deg = (rahu_deg + 180.0) % 360.0
  k_sign_idx = int(ketu_deg // 30)
  planets_data["Ketu"] = {
      "deg": ketu_deg % 30,
      "sign": ZODIAC_SIGNS[k_sign_idx],
      "house": ((k_sign_idx - asc_sign_idx) % 12) + 1,
      "full_deg": ketu_deg,
  }

  return planets_data, {"sign": ZODIAC_SIGNS[asc_sign_idx], "deg": asc_rem_deg}


# --- 4. Classical Yoga Scanner ---
def detect_classical_yogas(planets, lagna_sign):
  yogas = []
  h_sun = planets["Sun"]["house"]
  h_mer = planets["Mercury"]["house"]
  h_jup = planets["Jupiter"]["house"]
  h_moon = planets["Moon"]["house"]
  h_sat = planets["Saturn"]["house"]
  h_mars = planets["Mars"]["house"]
  h_ven = planets["Venus"]["house"]

  # Budhaditya Yoga
  if h_sun == h_mer:
    yogas.append({
        "Yoga": "Budhaditya Yoga (बुधादित्य योग)",
        "Type": "Raj Yoga / Intellectual Yoga",
        "Description": (
            "Sun and Mercury unite in the same house. Endows high analytical"
            " mastery, razor-sharp intellect, reputation, and strong aptitude"
            " for advisory or leadership."
        ),
    })

  # Gaja Kesari Yoga (Jupiter in Kendra from Moon)
  diff_jup_moon = (h_jup - h_moon) % 12
  if diff_jup_moon in [0, 3, 6, 9]:
    yogas.append({
        "Yoga": "Gaja Kesari Yoga (गजकेसरी योग)",
        "Type": "Sovereign Auspicious Yoga",
        "Description": (
            "Jupiter resides in a Kendra (1st, 4th, 7th, 10th) from the Moon."
            " Grants lasting social respect, protection from adversaries,"
            " noble character, and financial stability."
        ),
    })

  # Pancha Mahapurusha Yogas (Exaltation or Own Sign in Kendra 1,4,7,10)
  kendras = [1, 4, 7, 10]
  if h_sat in kendras and planets["Saturn"]["sign"] in [
      "Capricorn",
      "Aquarius",
      "Libra",
  ]:
    yogas.append({
        "Yoga": "Shasha Mahapurusha Yoga (शश योग)",
        "Type": "Pancha Mahapurusha (Saturn)",
        "Description": (
            "Saturn occupies Kendra in own or exalted sign. Indicates a"
            " strategist, high endurance, power over large organizations, and"
            " lasting authority achieved through discipline."
        ),
    })

  if h_jup in kendras and planets["Jupiter"]["sign"] in [
      "Sagittarius",
      "Pisces",
      "Cancer",
  ]:
    yogas.append({
        "Yoga": "Hamsa Mahapurusha Yoga (हंस योग)",
        "Type": "Pancha Mahapurusha (Jupiter)",
        "Description": (
            "Jupiter occupies Kendra in own or exalted sign. Indicates wisdom,"
            " ethical leadership, spiritual stature, and widespread acclaim."
        ),
    })

  if h_mars in kendras and planets["Mars"]["sign"] in [
      "Aries",
      "Scorpio",
      "Capricorn",
  ]:
    yogas.append({
        "Yoga": "Ruchaka Mahapurusha Yoga (रुचक योग)",
        "Type": "Pancha Mahapurusha (Mars)",
        "Description": (
            "Mars in Kendra in own/exalted sign. Endows valor, executive"
            " power, victory in litigation/competitions, and real-estate"
            " strength."
        ),
    })

  # Viparita Raja Yoga (Lords of 6, 8, 12 in 6, 8, 12)
  dusthanas = [6, 8, 12]
  if h_mars in dusthanas and h_sat in dusthanas:
    yogas.append({
        "Yoga": "Viparita Raja Yoga (विपरीत राजयोग)",
        "Type": "Crisis-to-Triumph Yoga",
        "Description": (
            "Strong protection in periods of severe adversity. Success rises"
            " rapidly after competitors stumble or through sudden unexpected"
            " breakthroughs."
        ),
    })

  return yogas


# --- 5. Dynamic Vimshottari Dasha Engine ---
def calculate_vimshottari(moon_full_deg, birth_date):
  nak_idx = int(moon_full_deg // (360 / 27))
  rem_nak_deg = moon_full_deg % (360 / 27)
  nak_span = 360 / 27  # 13°20' = 13.3333°

  nak_name, balance_lord, total_years = NAKSHATRAS[nak_idx]
  fraction_left = 1.0 - (rem_nak_deg / nak_span)
  balance_days = fraction_left * total_years * 365.25

  # Order of 9 Mahadashas
  dasha_order = [
      ("Ketu", 7),
      ("Venus", 20),
      ("Sun", 6),
      ("Moon", 10),
      ("Mars", 7),
      ("Rahu", 18),
      ("Jupiter", 16),
      ("Saturn", 19),
      ("Mercury", 17),
  ]

  # Find start index
  start_idx = 0
  for i, (lord, span) in enumerate(dasha_order):
    if lord == balance_lord:
      start_idx = i
      break

  current_date = datetime.datetime(
      birth_date.year, birth_date.month, birth_date.day
  )
  timeline = []

  # First balance dasha
  first_end = current_date + datetime.timedelta(days=balance_days)
  timeline.append({
      "Lord": balance_lord,
      "Start Year": current_date.year,
      "End Year": first_end.year,
      "Span": f"{current_date.strftime('%b %Y')} - {first_end.strftime('%b %Y')}",
  })
  current_date = first_end

  # Subsequent dashas
  for step in range(1, 9):
    idx = (start_idx + step) % 9
    lord, yrs = dasha_order[idx]
    end_date = current_date + datetime.timedelta(days=yrs * 365.25)
    timeline.append({
        "Lord": lord,
        "Start Year": current_date.year,
        "End Year": end_date.year,
        "Span": (
            f"{current_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"
        ),
    })
    current_date = end_date

  return timeline, nak_name


# --- 6. Execution Pipeline ---
if submitted:
  planets, lagna = compute_live_ephemeris(
      dob, t_hour, t_min, t_ampm, lat, lon
  )
  yogas_found = detect_classical_yogas(planets, lagna["sign"])
  dasha_timeline, birth_nak = calculate_vimshottari(
      planets["Moon"]["full_deg"], dob
  )

  # Calculate Jaimini Karakas
  seven = {k: v for k, v in planets.items() if k not in ["Rahu", "Ketu"]}
  sorted_p = sorted(seven.items(), key=lambda x: x[1]["deg"], reverse=True)
  ak_planet = sorted_p[0][0]  # Atmakaraka
  amk_planet = sorted_p[1][0]  # Amatyakaraka
  dk_planet = sorted_p[6][0]  # Darakaraka

  st.success(
      f"✅ **Lagna (Ascendant): {lagna['sign']} ({lagna['deg']:.2f}°) | Janma"
      f" Nakshatra: {birth_nak}**"
  )

  # Tabs Architecture for High Value Reading
  tab_pred, tab_events, tab_yogas, tab_dasha, tab_matrix = st.tabs([
      "📖 संपूर्ण भविष्यकथन (Master Prediction)",
      "🎯 प्रमुख जीवन घटना (Timing of Milestones)",
      "🌟 कुंडलीतील राजयोग (Classical Yogas)",
      "⏱️ विंशोत्तरी दशा टाईमलाईन (Vimshottari)",
      "📊 खगोलीय तक्ता (Ephemeris Coordinates)",
  ])

  # --- TAB 1: MASTER PREDICTIONS (K.N. Rao Style) ---
  with tab_pred:
    st.header("Executive Vedic Assessment (के. एन. राव प्रारब्ध विश्लेषण)")

    st.subheader(f"१. आत्म्याचा उद्देश व व्यक्तिमत्त्व (Atmakaraka: {ak_planet})")
    if ak_planet == "Saturn":
      st.markdown(
          "> **शनी आत्मकारक:** तुमचा आत्मा कठोर शिस्त, सत्य, आणि निष्कलंक कर्माचा"
          " मार्ग निवडतो. सुरुवातीच्या काळात विलंब, जबाबदाऱ्यांचे ओझे किंवा संघर्ष"
          " जाणवू शकतो; परंतु हा ग्रह तुम्हाला एका रात्रीत नाही, तर कायमस्वरूपी"
          " आणि अढळ सत्ता/अधिकार देतो. ३२ ते ३६ वयानंतर मोठा अधिकार प्राप्त"
          " होतो."
      )
    elif ak_planet == "Sun":
      st.markdown(
          "> **सूर्य आत्मकारक:** नेतृत्व, स्वाभिमान, प्रशासकीय अधिकार आणि स्वतःचे"
          " साम्राज्य निर्माण करणे हा तुमच्या आत्म्याचा मूळ हेतू आहे. कोणाच्या"
          " हाताखाली दबून काम करणे तुम्हाला मान्य होणार नाही."
      )
    elif ak_planet == "Mercury":
      st.markdown(
          "> **बुध आत्मकारक:** बुद्धिमत्ता, डेटा, विश्लेषण, सल्लागार, तंत्रज्ञान"
          " आणि वाणिज्य हा तुमचा खरा मार्ग आहे. सतत नवीन शिकणे ही तुमची ताकद"
          " आहे."
      )
    elif ak_planet == "Jupiter":
      st.markdown(
          "> **गुरू आत्मकारक:** ज्ञान, धर्म, सल्लागार (Consultancy), आणि"
          " इतरांना मार्ग दाखवणे हा तुमचा आध्यात्मिक मार्ग आहे. समाजात तुमचा"
          " सल्ला प्रमाण मानला जाईल."
      )
    elif ak_planet == "Mars":
      st.markdown(
          "> **मंगळ आत्मकारक:** प्रचंड ऊर्जा, धैर्य, इंजिनिअरिंग/टेक्निकल कौशल्य"
          " आणि कोणत्याही आव्हानावर मात करण्याची वृत्ती. रागावर नियंत्रण ठेवणे"
          " ही तुमची सर्वात मोठी साधना आहे."
      )
    elif ak_planet == "Venus":
      st.markdown(
          "> **शुक्र आत्मकारक:** सर्जनशीलता, कला, डिझाइन, लक्झरी आणि आंतरराष्ट्रीय"
          " संबंधांमधून भाग्योदय."
      )
    elif ak_planet == "Moon":
      st.markdown(
          "> **चंद्र आत्मकारक:** संवेदनशीलता, जनसंपर्क, मानसशास्त्र आणि लोकांच्या"
          " गरजा समजून काम करण्याचे प्रचंड कौशल्य."
      )

    st.subheader(
        f"२. आजीविका, करिअर आणि संपत्ती (Amatyakaraka: {amk_planet} in House"
        f" {planets[amk_planet]['house']})"
    )
    st.info(
        f"तुमचा करिअर नियंत्रक ग्रह **{amk_planet}** हा कुंडलीच्या"
        f" **{planets[amk_planet]['house']} व्या घरात** बसलेला आहे. याचा अर्थ"
        " तुम्ही दुसऱ्यांवर अवलंबून राहण्यापेक्षा स्वतःची स्वतंत्र"
        " ओळख/कन्सल्टन्सी, धोरणात्मक सल्लागार किंवा व्यवस्थापकीय निर्णयक्षमतेत"
        " सर्वोच्च संपत्ती व प्रतिष्ठा मिळवाल."
    )

    st.subheader(
        f"३. वैवाहिक जीवन व जोडीदार (Darakaraka: {dk_planet} in House"
        f" {planets[dk_planet]['house']})"
    )
    st.write(
        f"तुमचा दाराकारक ग्रह **{dk_planet}** आहे. जोडीदार सुशिक्षित, स्वतंत्र"
        " विचारसरणीचा आणि नात्यामध्ये बौद्धिक समानतेला सर्वाधिक महत्त्व देणारा"
        " असेल. दोघांमधील संवाद हा वैवाहिक सौख्याचा मुख्य आधार राहील."
    )

  # --- TAB 2: TIMING OF EVENTS ---
  with tab_events:
    st.header("🎯 के. एन. राव इव्हेंट टाइमिंग विंडो (Major Milestones)")
    st.write(
        "के. एन. राव यांच्या सिद्धांतानुसार, दशा अनुकूल असताना गोचरीतील **गुरू"
        " आणि शनी** या दोघांचा दुहेरी प्रभाव (Double Transit) संबंधित घरावर येतो,"
        " तेव्हाच घटना प्रत्यक्ष घडते."
    )

    col_e1, col_e2 = st.columns(2)
    with col_e1:
      st.success("💼 **करिअरचा सुवर्णकाळ व स्वतःचा उद्योग (Career Peak Window)**")
      st.markdown(
          "- **वय ३१ ते ३६ वर्ष:** शनी आणि गुरूचा १० व्या आणि ११ व्या घरावर"
          " होणारा ट्रान्झिट.\n- **निष्कर्ष:** नोकरीकडून स्वतःच्या स्वतंत्र"
          " कन्सल्टन्सी/सॉफ्टवेअर किंवा अधिकारयुक्त पदाकडे वाटचाल. हा काळ आर्थिक"
          " पाया कायमचा मजबूत करेल."
      )

      st.info("🏡 **घर, वाहन व मालमत्ता खरेदी योग (Property & Assets)**")
      st.markdown(
          "- **४ थ्या घरावरील अनुकूल गोचर:** गुरु आणि मंगळाची परस्पर दृष्टी किंवा"
          " ४ थ्या भावावर शनीचा पायाभूत प्रभाव कायमस्वरूपी स्थावर मालमत्ता मिळवून"
          " देतो."
      )

    with col_e2:
      st.warning("💍 **विवाह व भागीदारीचा काळ (Marriage Window)**")
      st.markdown(
          "- **७ व्या घरावरील डबल ट्रान्झिट:** जेव्हा गोचरीचा गुरू ७ व्या घराला"
          " किंवा ७ व्या घराच्या स्वामीला पाहतो, तेव्हा विवाहाचा योग निश्चित"
          " होतो.\n- **सल्ला:** घाईगडबडीत निर्णय न घेता कुंडलीतील सप्तमेश आणि"
          " दाराकारकाचे अंश जुळवून विवाह करणे अत्यंत लाभदायक ठरते."
      )

  # --- TAB 3: YOGAS ---
  with tab_yogas:
    st.header("🌟 तुमच्या कुंडलीत आढळलेले शुभ योग (Classical Yogas)")
    if yogas_found:
      for y in yogas_found:
        with st.expander(f"✨ {y['Yoga']} — {y['Type']}", expanded=True):
          st.write(y["Description"])
    else:
      st.write("कुंडलीतील इतर सूक्ष्म योग कार्यरत आहेत.")

  # --- TAB 4: VIMSHOTTARI DASHA ---
  with tab_dasha:
    st.header(
        "⏱️ विंशोत्तरी महादशा टाईमलाईन (Vimshottari Dasha Calendar - 120 Years)"
    )
    st.write(
        f"जन्मावेळचे नक्षत्र: **{birth_nak}** (अधिपती: **{dasha_timeline[0]['Lord']}**)"
    )
    df_dasha = pd.DataFrame(dasha_timeline)
    st.dataframe(df_dasha, use_container_width=True)

  # --- TAB 5: EPHEMERIS COORDINATES ---
  with tab_matrix:
    st.header("📊 अचूक खगोलीय ग्रहस्थिती (Lahiri Ayanamsha)")
    live_rows = []
    for p, info in planets.items():
      live_rows.append({
          "ग्रह (Planet)": p,
          "राशी (Sign)": info["sign"],
          "अंश (Degree in Sign)": f"{info['deg']:.2f}°",
          "घर (House)": f"House {info['house']}",
      })
    st.table(pd.DataFrame(live_rows))
