import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Universal Evidence-Based Astro Engine", layout="wide"
)

# --- 1. Multi-Language Dictionary Engine ---
LANG_PACK = {
    "English": {
        "title": "⚡ Evidence-Based Vedic Astro Engine",
        "subtitle": (
            "Integrated Frameworks: Parashari (BPHS) | Jaimini (K.N. Rao) | KP"
            " Cuspal | V.P. Goel Rules"
        ),
        "input_header": "1. Enter Birth Data & Coordinates",
        "dob": "Date of Birth",
        "tob": "Time of Birth",
        "hour": "Hour",
        "min": "Minute",
        "city": "Birth City / Place",
        "lat": "Latitude",
        "lon": "Longitude",
        "btn": "🔮 Generate Complete Astrological & Karmic Matrix",
        "tab1": "🔍 Comprehensive Predictions",
        "tab2": "🪐 Conjunctions & Parashari Aspects (PAC)",
        "tab3": "📊 Jaimini & BPHS Degrees",
        "tab4": "⏱️ Vimshottari & Double Transit",
        "core_identity": "1. Core Soul Identity & Karmic Path (Atmakaraka)",
        "career_destiny": "2. Professional Mastery & Wealth (Amatyakaraka)",
        "spouse_dynamics": "3. Partnership & Spousal Blueprint (Darakaraka)",
        "avastha_header": "4. Critical BPHS Planetary States (Avasthas)",
        "ak_saturn": (
            "**Saturn as Atmakaraka:** Your soul's evolutionary task is"
            " grounded in endurance, discipline, and building permanent,"
            " unshakeable foundations. Saturn demands patience and dismantling"
            " ego. Early career trials yield unmatched authority and public"
            " respect in mature cycles."
        ),
        "amk_sun": (
            "**Sun as Amatyakaraka (Career Indicator):** High inclination"
            " toward executive leadership, advisory roles, strategic management,"
            " and sovereign entrepreneurial ventures. Routine subordinate work"
            " drains vitality; you excel where intellectual autonomy is"
            " supreme."
        ),
        "dk_mercury": (
            "**Mercury as Darakaraka (Partner Indicator):** Your life partner"
            " possesses a sharp, analytical, and inquisitive mind. The"
            " relationship thrives on open intellectual dialogue, shared"
            " commercial/creative ideas, and mutual mental stimulation."
        ),
        "budhaditya": (
            "**Budhaditya Yoga (Sun + Mercury):** Enhances razor-sharp"
            " analytical capabilities, intellectual independence, and strategic"
            " architectural reasoning."
        ),
        "sunsat": (
            "**Sun + Saturn Union:** Produces intense resilience. Fosters the"
            " ability to execute massive multi-year projects without requiring"
            " short-term external validation."
        ),
    },
    "मराठी": {
        "title": "⚡ वैदिक ज्योतिष प्रेडिक्शन इंजिन",
        "subtitle": (
            "एकत्रित पद्धती: पराशरी (BPHS) | जैमिनी (के.एन. राव) | केपी कस्पल |"
            " व्ही.पी. गोयल नियम"
        ),
        "input_header": "१. जन्म तपशील आणि रेखांश-अक्षांश",
        "dob": "जन्मतारीख",
        "tob": "जन्म वेळ",
        "hour": "तास",
        "min": "मिनिट",
        "city": "जन्म शहर / ठिकाण",
        "lat": "अक्षांश (Latitude)",
        "lon": "रेखांश (Longitude)",
        "btn": "🔮 संपूर्ण सखोल भविष्यकथन आणि कुंडली विश्लेषण करा",
        "tab1": "🔍 सखोल भविष्यकथन",
        "tab2": "🪐 युती आणि पराशरी दृष्टी (PAC विश्लेषण)",
        "tab3": "📊 जैमिनी चर कारके आणि अंश",
        "tab4": "⏱️ विंशोत्तरी दशा आणि गोचर",
        "core_identity": "१. मूळ आत्मा, स्वभाव आणि जीवन ध्येय (आत्मकारक)",
        "career_destiny": "२. करिअर, अधिकार आणि धनप्राप्ती (अमात्यकारक)",
        "spouse_dynamics": "३. जोडीदाराचा स्वभाव आणि वैवाहिक जीवन (दाराकारक)",
        "avastha_header": "४. महत्त्वाच्या पराशरी ग्रहावस्था (BPHS Avasthas)",
        "ak_saturn": (
            "**शनी आत्मकारक:** तुमच्या आत्म्याचा मूळ मार्ग कठोर परिश्रम, शिस्त,"
            " संयम आणि सत्यनिष्ठेवर आधारित आहे. सुरुवातीला विलंब किंवा संघर्ष"
            " सहन करावा लागला तरी उत्तरार्धात शाश्वत आणि मोठे यश प्राप्त होते."
        ),
        "amk_sun": (
            "**सूर्य अमात्यकारक (करिअर):** प्रशासकीय नेतृत्व, सल्लागार पद,"
            " संस्थात्मक धोरण आणि स्वतःचे स्वतंत्र कार्यक्षेत्र यात मोठी"
            " प्रगती. स्वतःचे बौद्धिक स्वातंत्र्य असणाऱ्या ठिकाणी तुम्ही सर्वोत्तम"
            " कामगिरी कराल."
        ),
        "dk_mercury": (
            "**बुध दाराकारक (जोडीदार):** जोडीदार अतिशय बुद्धिमान, संवादप्रिय,"
            " हजरजबाबी आणि व्यावहारिक असेल. बौद्धिक देवाणघेवाण नात्याचा मजबूत पाया"
            " ठरेल."
        ),
        "budhaditya": (
            "**बुधादित्य योग (सूर्य + बुध):** तीव्र बुद्धिमत्ता, विश्लेषणात्मक"
            " क्षमता आणि धोरणात्मक निर्णयक्षमता वाढवणारा अत्यंत शुभ योग."
        ),
        "sunsat": (
            "**सूर्य + शनी युती:** प्रचंड सहनशीलता आणि दीर्घकालीन उद्दिष्टे"
            " पूर्ण करण्याची आंतरिक ताकद प्रदान करते."
        ),
    },
    "हिंदी": {
        "title": "⚡ वैदिक ज्योतिष प्रेडिक्शन इंजन",
        "subtitle": (
            "समेकित सिद्धांत: पाराशरी (BPHS) | जैमिनी (के.एन. राव) | केपी |"
            " वी.पी. गोयल"
        ),
        "input_header": "१. जन्म विवरण और अक्षांश/देशांतर",
        "dob": "जन्म तिथि",
        "tob": "जन्म समय",
        "hour": "घंटा",
        "min": "मिनट",
        "city": "जन्म स्थान / शहर",
        "lat": "अक्षांश (Latitude)",
        "lon": "देशांतर (Longitude)",
        "btn": "🔮 संपूर्ण कुंडली और भविष्यफल विश्लेषण उत्पन्न करें",
        "tab1": "🔍 विस्तृत भविष्यफल",
        "tab2": "🪐 युति और पाराशरी दृष्टि (PAC)",
        "tab3": "📊 जैमिनी चर कारक और ग्रह अंश",
        "tab4": "⏱️ विंशोत्तरी दशा और गोचर",
        "core_identity": "१. आत्मिक उद्देश्य और जीवन पथ (आत्मकारक)",
        "career_destiny": "२. आजीविका, पद और धन संपदा (अमात्यकारक)",
        "spouse_dynamics": "३. जीवनसाथी का स्वभाव और वैवाहिक योग (दाराकारक)",
        "avastha_header": "४. पाराशर ग्रहावस्था विश्लेषण (BPHS Avasthas)",
        "ak_saturn": (
            "**शनि आत्मकारक:** जीवन का प्रमुख उद्देश्य अनुशासन, सत्य, धैर्य और"
            " दीर्घकालिक निर्माण है। शुरुआती दौर में संघर्ष हो सकता है, परंतु"
            " अंततः स्थायी अधिकार प्राप्त होता है।"
        ),
        "amk_sun": (
            "**सूर्य अमात्यकारक:** नेतृत्व, प्रशासनिक कार्य, उच्च स्तरीय"
            " परामर्श और स्वतंत्र व्यावसायिक उद्यम में श्रेष्ठ सफलता का योग।"
        ),
        "dk_mercury": (
            "**बुध दाराकारक:** जीवनसाथी तीक्ष्ण बुद्धि वाला, संवाद-प्रिय और"
            " व्यावहारिक स्वभाव का होगा। वैचारिक तालमेल श्रेष्ठ रहेगा।"
        ),
        "budhaditya": (
            "**बुधादित्य योग (सूर्य + बुध):** उत्कृष्ट तार्किक क्षमता,"
            " रणनीतिक दृष्टि और बौद्धिक प्रतिष्ठा प्रदान करता है।"
        ),
        "sunsat": (
            "**सूर्य + शनि युति:** गहन धैर्य और बिना किसी बाहरी सहारे के बड़े"
            " लक्ष्यों को प्राप्त करने की क्षमता।"
        ),
    },
    "ગુજરાતી": {
        "title": "⚡ વૈદિક જ્યોતિષ પ્રિડિક્શન એન્જિન",
        "subtitle": (
            "સિદ્ધાંતો: પરાશરી (BPHS) | જૈમિની (કે.એન. રાવ) | કેપી પદ્ધતિ"
        ),
        "input_header": "૧. જન્મ વિગતો",
        "dob": "જન્મ તારીખ",
        "tob": "જન્મ સમય",
        "hour": "કલાક",
        "min": "મિનિટ",
        "city": "જન્મ સ્થળ",
        "lat": "અક્ષાંશ (Latitude)",
        "lon": "રેખાંશ (Longitude)",
        "btn": "🔮 સંપૂર્ણ જ્યોતિષીય વિશ્લેષણ મેળવો",
        "tab1": "🔍 ઊંડાણપૂર્વક આગાહી",
        "tab2": "🪐 યુતિ અને પરાશરી દ્રષ્ટિ",
        "tab3": "📊 જૈમિની કારક અને અંશ",
        "tab4": "⏱️ વિંશોત્તરી દશા અને ગોચર",
        "core_identity": "૧. આત્મા અને જીવનનું ધ્યેય (આત્મકારક)",
        "career_destiny": "૨. કારકિર્દી અને સંપત્તિ (અમાત્યકારક)",
        "spouse_dynamics": "૩. જીવનસાથીનો સ્વભાવ (દારકારક)",
        "avastha_header": "૪. ગ્રહ અવસ્થા વિશ્લેષણ",
        "ak_saturn": (
            "**શનિ આત્મકારક:** શિસ્ત, ધૈર્ય અને પરિશ્રમ દ્વારા કાયમી સફળતા."
        ),
        "amk_sun": (
            "**સૂર્ય અમાત્યકારક:** નેતૃત્વ, કન્સલ્ટિંગ અને સ્વતંત્ર ઉદ્યોગમાં"
            " શ્રેષ્ઠ સફળતા."
        ),
        "dk_mercury": (
            "**બુધ દારકારક:** જીવનસાથી બુદ્ધિશાળી અને ઉત્તમ સંવાદ કુશળતા"
            " ધરાવનાર હશે."
        ),
        "budhaditya": "**બુધાદિત્ય યોગ:** ઉત્તમ તાર્કિક ક્ષમતા અને માન-સન્માન.",
        "sunsat": "**સૂર્ય + શનિ યુતિ:** અડગ ધૈર્ય અને સહનશક્તિ.",
    },
    "தமிழ்": {
        "title": "⚡ வேத ஜோதிட கணிப்பு இயந்திரம்",
        "subtitle": "பராசர (BPHS) | ஜெய்மினி (K.N. ராவ்) | KP அமைப்பு",
        "input_header": "1. பிறப்பு விவரங்கள்",
        "dob": "பிறந்த தேதி",
        "tob": "பிறந்த நேரம்",
        "hour": "மணி",
        "min": "நிமிடம்",
        "city": "பிறந்த ஊர்",
        "lat": "அட்சரேகை (Latitude)",
        "lon": "தீர்க்கரேகை (Longitude)",
        "btn": "🔮 முழுமையான ஜாதக பலன்களைக் காண்க",
        "tab1": "🔍 விரிவான பலன்கள்",
        "tab2": "🪐 சேர்க்கை & பார்வைகள்",
        "tab3": "📊 காரகங்கள் & பாகைகள்",
        "tab4": "⏱️ தசா & கோச்சாரம்",
        "core_identity": "1. ஆத்ம காரகன் & வாழ்க்கை நோக்கம்",
        "career_destiny": "2. தொழில் மற்றும் செல்வம் (அமத்தியகாரகன்)",
        "spouse_dynamics": "3. வாழ்க்கைத் துணைவர் குணம் (தாரகாரகன்)",
        "avastha_header": "4. கிரக அவஸ்தைகள்",
        "ak_saturn": "**சனி ஆத்மகாரகன்:** பொறுமை, ஒழுக்கம் மற்றும் நீண்ட கால உழைப்பின் மூலம் நிலையான வெற்றி.",
        "amk_sun": "**சூரியன் அமத்தியகாரகன்:** தலைமைப் பண்பு, நிர்வாகம் மற்றும் சுயதொழிலில் மேன்மை.",
        "dk_mercury": "**புதன் தாரகாரகன்:** கூர்மையான அறிவாற்றல் மற்றும் சிறந்த உரையாடல் திறன் கொண்ட துணைவர்.",
        "budhaditya": "**புதாதித்ய யோகம்:** சிறந்த அறிவாற்றல் மற்றும் நிர்வாகத் திறன்.",
        "sunsat": "**சூரியன் + சனி சேர்க்கை:** அசைக்க முடியாத சகிப்புத்தன்மை மற்றும் மன உறுதி.",
    },
}

# --- 2. Language Selection UI ---
col_head, col_lang = st.columns([3, 1])
with col_lang:
  selected_lang = st.selectbox(
      "🌐 Select Language / भाषा चुनें", list(LANG_PACK.keys()), index=0
  )

T = LANG_PACK[selected_lang]

with col_head:
  st.title(T["title"])
  st.caption(T["subtitle"])

# --- 3. Input Form ---
with st.form("birth_details_form"):
  st.subheader(T["input_header"])

  c_dob, c_tob1, c_tob2, c_tob3 = st.columns([2, 1, 1, 1])
  with c_dob:
    dob = st.date_input(
        T["dob"],
        value=datetime.date(1995, 1, 1),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today(),
    )
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

# --- 4. Astrological Calculation Helper Functions ---
def calculate_jaimini_karakas(planets_data):
  seven = {k: v for k, v in planets_data.items() if k not in ["Rahu", "Ketu"]}
  sorted_p = sorted(seven.items(), key=lambda x: x[1]["deg"], reverse=True)
  roles = [
      "Atmakaraka (AK)",
      "Amatyakaraka (AmK)",
      "Bhratrukaraka (BK)",
      "Matrukaraka (MK)",
      "Putrakaraka (PK)",
      "Gnatikaraka (GK)",
      "Darakaraka (DK)",
  ]
  res = []
  k_dict = {}
  for idx, (p_name, p_info) in enumerate(sorted_p):
    k_dict[roles[idx].split()[0]] = p_name
    res.append({
        "Karaka Role": roles[idx],
        "Planet": p_name,
        "Degree": f"{p_info['deg']:.2f}°",
        "Sign": p_info["sign"],
        "House": p_info["house"],
    })
  return pd.DataFrame(res), k_dict


def compute_conjunctions(planets_data):
  house_map = {}
  for p, data in planets_data.items():
    house_map.setdefault(data["house"], []).append(
        (p, data["deg"], data["sign"])
    )
  conjunctions = []
  for house, p_list in house_map.items():
    if len(p_list) > 1:
      names = [item[0] for item in p_list]
      conjunctions.append({
          "House": house,
          "Sign": p_list[0][2],
          "Planets Involved": ", ".join(names),
      })
  return conjunctions


def compute_parashari_aspects(planets_data):
  aspect_hits = []
  for p, d in planets_data.items():
    h = d["house"]
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
      residents = [
          pl for pl, info in planets_data.items() if info["house"] == t
      ]
      aspect_hits.append({
          "Aspecting Planet": p,
          "Target House": t,
          "Aspect Received By": (
              ", ".join(residents) if residents else "Open Space"
          ),
      })
  return pd.DataFrame(aspect_hits)


# --- 5. Execution Pipeline ---
if submitted:
  natal_planets = {
      "Sun": {"deg": 17.32, "sign": "Sagittarius", "house": 9},
      "Moon": {"deg": 12.44, "sign": "Aquarius", "house": 11},
      "Mars": {"deg": 16.45, "sign": "Scorpio", "house": 8},
      "Mercury": {"deg": 1.88, "sign": "Sagittarius", "house": 9},
      "Jupiter": {"deg": 11.36, "sign": "Gemini", "house": 3},
      "Venus": {"deg": 12.48, "sign": "Capricorn", "house": 10},
      "Saturn": {"deg": 21.96, "sign": "Sagittarius", "house": 9},
      "Rahu": {"deg": 24.69, "sign": "Aquarius", "house": 11},
      "Ketu": {"deg": 24.69, "sign": "Leo", "house": 5},
  }

  df_karakas, k_dict = calculate_jaimini_karakas(natal_planets)
  conjunctions = compute_conjunctions(natal_planets)
  df_aspects = compute_parashari_aspects(natal_planets)

  tab1, tab2, tab3, tab4 = st.tabs(
      [T["tab1"], T["tab2"], T["tab3"], T["tab4"]]
  )

  with tab1:
    st.subheader(T["core_identity"])
    st.info(T["ak_saturn"])

    st.subheader(T["career_destiny"])
    st.success(T["amk_sun"])

    st.subheader(T["spouse_dynamics"])
    st.write(T["dk_mercury"])

    st.subheader(T["avastha_header"])
    for p, info in natal_planets.items():
      if info["deg"] <= 2.0:
        st.warning(
            f"⚠️ **{p} ({info['deg']:.2f}°) - Balyavastha (Inception State):**"
            " Raw karmic cycle requiring deliberate cultivation."
        )
      elif info["deg"] >= 28.0:
        st.error(
            f"⏳ **{p} ({info['deg']:.2f}°) - Vriddhavastha (Culminating"
            " State):** Karmic completion cycle."
        )

  with tab2:
    st.subheader("Planetary Conjunctions (Yutis)")
    for conj in conjunctions:
      with st.expander(
          f"House {conj['House']} ({conj['Sign']}): {conj['Planets Involved']}",
          expanded=True,
      ):
        if "Sun" in conj["Planets Involved"] and (
            "Mercury" in conj["Planets Involved"]
        ):
          st.write(T["budhaditya"])
        if "Sun" in conj["Planets Involved"] and (
            "Saturn" in conj["Planets Involved"]
        ):
          st.write(T["sunsat"])

    st.subheader("Parashari Drishti Matrix (Special Aspects)")
    st.dataframe(df_aspects, use_container_width=True)

  with tab3:
    st.subheader("Jaimini Chara Karakas (Degree Hierarchy)")
    st.dataframe(df_karakas, use_container_width=True)

  with tab4:
    st.subheader("Vimshottari Dasha Horizon")
    dasha_df = pd.DataFrame([
        {
            "Dasha Level": "Mahadasha",
            "Planet": "Saturn",
            "Period": "2008 - 2027",
            "Focus": "Karmic structuring & foundational mastery",
        },
        {
            "Dasha Level": "Antardasha (Upcoming)",
            "Planet": "Moon",
            "Period": "Starting Feb 2027",
            "Focus": "Public transition & enterprise launch",
        },
        {
            "Dasha Level": "Mahadasha (Upcoming)",
            "Planet": "Mercury",
            "Period": "2027 - 2044",
            "Focus": (
                "Intellectual commerce, software, authoring & major expansion"
            ),
        },
    ])
    st.table(dasha_df)

    st.subheader("K.N. Rao Double Transit Verification")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
      val_house = st.selectbox(
          "House to Validate:",
          [7, 10],
          format_func=lambda x: (
              "House 7: Relationship / Partnership Expansion"
              if x == 7
              else "House 10: Career Milestone / Enterprise Launch"
          ),
      )
    with col_v2:
      if val_house == 10:
        st.info(
            "⏳ **House 10 Status:** Saturn & Jupiter transit alignments are"
            " maturing toward the 2027 trigger window."
        )
      elif val_house == 7:
        st.success(
            "🎯 **House 7 Status:** Jupiter transit aspect active. Fosters"
            " strategic partnerships and collaborative enterprise."
        )
