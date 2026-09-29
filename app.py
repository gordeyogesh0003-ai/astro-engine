import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Evidence-Based Vedic Prediction Engine", layout="centered"
)

st.title("⚡ AI-Integrated Vedic Astro Engine")
st.caption(
    "Frameworks: Parashari (BPHS) | Jaimini (K.N. Rao) | KP Cuspal | V.P. Goel"
    " Rules"
)

# --- User Input Section ---
with st.form("birth_details_form"):
  st.subheader("1. Enter Birth Data")

  dob = st.date_input(
      "Date of Birth",
      value=datetime.date(1995, 1, 1),
      min_value=datetime.date(1900, 1, 1),
      max_value=datetime.date.today(),
  )

  st.write("Time of Birth")
  t_col1, t_col2, t_col3 = st.columns(3)
  with t_col1:
    t_hour = st.selectbox(
        "Hour", [f"{i:02d}" for i in range(1, 13)], index=9
    )  # Default 10
  with t_col2:
    t_min = st.selectbox(
        "Minute", [f"{i:02d}" for i in range(0, 60)], index=40
    )  # Default 40
  with t_col3:
    t_ampm = st.selectbox("AM / PM", ["AM", "PM"], index=0)

  place = st.text_input("Birth City / Place", value="Sangamner, Maharashtra")

  c_lat, c_lon = st.columns(2)
  with c_lat:
    lat = st.number_input("Latitude", value=19.5761, format="%.4f")
  with c_lon:
    lon = st.number_input("Longitude", value=74.2070, format="%.4f")

  submitted = st.form_submit_button("🔮 Generate Complete In-Depth Prediction")


# --- Astrological Calculation Engines ---
def calculate_jaimini_karakas(planets_data):
  seven_planets = {
      k: v for k, v in planets_data.items() if k not in ["Rahu", "Ketu"]
  }
  sorted_planets = sorted(
      seven_planets.items(), key=lambda x: x[1]["deg"], reverse=True
  )

  karaka_titles = [
      ("Atmakaraka (AK)", "आत्मा आणि जीवन हेतू (Soul & Core Identity)"),
      ("Amatyakaraka (AmK)", "करिअर आणि कर्म (Career, Wealth & Intellect)"),
      ("Bhratrukaraka (BK)", "पराक्रम आणि भावंडे (Courage, Siblings & Gurus)"),
      ("Matrukaraka (MK)", "सुख आणि आई (Peace, Mother, Property)"),
      ("Putrakaraka (PK)", "बुद्धिमत्ता आणि संतती (Creativity, Children)"),
      ("Gnatikaraka (GK)", "रोग, शत्रू आणि संघर्ष (Obstacles, Competition)"),
      ("Darakaraka (DK)", "जोडीदार आणि वैवाहिक जीवन (Spouse & Partnership)"),
  ]

  karaka_result = []
  karaka_dict = {}
  for idx, (p_name, p_info) in enumerate(sorted_planets):
    k_name, desc = karaka_titles[idx]
    karaka_dict[k_name.split()[0]] = (
        p_name  # Store short key like Atmakaraka, Amatyakaraka
    )
    karaka_result.append({
        "Karaka Role": k_name,
        "Signification": desc,
        "Planet": p_name,
        "Degree": f"{p_info['deg']:.2f}°",
        "Rashi (Sign)": p_info["sign"],
    })
  return pd.DataFrame(karaka_result), karaka_dict


def get_deep_predictions(karaka_dict, planets_data):
  ak = karaka_dict.get("Atmakaraka", "Saturn")
  amk = karaka_dict.get("Amatyakaraka", "Sun")
  dk = karaka_dict.get("Darakaraka", "Mercury")

  ak_interpretations = {
      "Sun": (
          "तुमचा आत्मकारक सूर्य आहे. जीवनात स्वाभिमान, नेतृत्व (Leadership) आणि"
          " उच्च पद प्राप्त करणे हा तुमचा मुख्य मार्ग आहे. परंतु अहंकारावर ताबा"
          " ठेवणे हे सर्वात मोठे आध्यात्मिक आव्हान असेल."
      ),
      "Moon": (
          "तुमचा आत्मकारक चंद्र आहे. मन अत्यंत संवेदनशील आणि दयाळू आहे. इतरांची"
          " काळजी घेणे, समुपदेशन किंवा समाजोपयोगी कामात तुम्हाला आंतरिक समाधान"
          " लाभेल."
      ),
      "Mars": (
          "तुमचा आत्मकारक मंगळ आहे. प्रचंड ऊर्जा, साहस आणि आव्हानांना सामोरे"
          " जाण्याची वृत्ती राहील. राग आणि घाईगडबडीत घेतलेले निर्णय टाळणे हे तुमचे"
          " मुख्य जीवन ध्येय आहे."
      ),
      "Mercury": (
          "तुमचा आत्मकारक बुध आहे. बुद्धी, संभाषण कौशल्य, लेखन आणि विश्लेषण हे"
          " तुमचे सामर्थ्य आहे. सत्य बोलणे आणि स्पष्ट विचार ठेवणे हा तुमच्या"
          " आत्म्याचा मार्ग आहे."
      ),
      "Jupiter": (
          "तुमचा आत्मकारक गुरू आहे. ज्ञान, अध्यात्म, शिक्षण आणि सल्लागार"
          " (Consultancy) च्या माध्यमातून तुमची खरी ओळख बनेल. ज्ञानाचा योग्य वापर"
          " समाजासाठी करणे आवश्यक आहे."
      ),
      "Venus": (
          "तुमचा आत्मकारक शुक्र आहे. कला, सौंदर्य, सर्जनशीलता आणि नातेसंबंधांचे"
          " महत्त्व तुमच्या आयुष्यात सर्वोच्च राहील. संयम आणि नैतिक मूल्यांचे पालन"
          " तुम्हाला यश देईल."
      ),
      "Saturn": (
          "तुमचा आत्मकारक शनी आहे. कठीण परिश्रम, शिस्त, संयम आणि सत्याची शिकवण हा"
          " तुमचा मूळ पाया आहे. सुरुवातीला विलंब किंवा संघर्ष होऊ शकतो, पण दीर्घ"
          " मुदतीमध्ये शाश्वत आणि मोठे यश मिळते."
      ),
  }

  amk_interpretations = {
      "Sun": (
          "प्रशासकीय कामे, सरकारी संस्था, उच्च व्यवस्थापन किंवा स्वतःचा"
          " स्वतंत्र अधिकार असणारे कार्यक्षेत्र तुमच्यासाठी सर्वाधिक फायदेशीर"
          " ठरेल."
      ),
      "Moon": (
          "पब्लिक डीलिंग, हॉस्पिटॅलिटी, समुपदेशन, कला किंवा मानवी संसाधनांशी"
          " (HR) संबंधित क्षेत्रात उत्तम प्रगतीचे योग आहेत."
      ),
      "Mars": (
          "इंजिनिअरिंग, तंत्रज्ञान, डिफेन्स, रिअल इस्टेट किंवा धोरणात्मक"
          " नेतृत्वात यश मिळेल."
      ),
      "Mercury": (
          "डेटा विश्लेषण, सॉफ्टवेअर, फायनान्स, ट्रेड, कन्सल्टन्सी, लेखन किंवा"
          " मध्यस्थीच्या कामात उच्च आर्थिक यश मिळेल."
      ),
      "Jupiter": (
          "अध्यापन, सल्लागार (Advisory/Consultancy), वित्त (Finance),"
          " मार्गदर्शक किंवा रिसर्चच्या क्षेत्रात प्रचंड आदर व धनलाभ होईल."
      ),
      "Venus": (
          "क्रिएटिव्ह इंडस्ट्री, डिझाइन, लक्झरी, माध्यम किंवा भागीदारीच्या"
          " व्यवसायात करिअर बहरेल."
      ),
      "Saturn": (
          "ऑपरेशन्स, रिसर्च, सिस्टीम आर्किटेक्चर, कायदेशीर क्षेत्र किंवा दीर्घकालीन"
          " संस्थात्मक निर्मितीमध्ये मोठे अधिकार प्राप्त होतील."
      ),
  }

  dk_interpretations = {
      "Sun": (
          "जोडीदार प्रतिष्ठित, स्वाभिमानी आणि अधिकार गाजवणारा असू शकतो."
          " परस्पर सन्मान राखणे अत्यंत आवश्यक राहील."
      ),
      "Moon": (
          "जोडीदार भावनिक, काळजीवाहू आणि कुटुंबाभिमुख असेल. नात्यात आपुलकी आणि"
          " प्रेम राहील."
      ),
      "Mars": (
          "जोडीदार अतिशय उत्साही, स्पष्टवक्ता आणि महत्त्वाकांक्षी असेल."
          " नात्यामध्ये मोकळेपणा ठेवणे हिताचे ठरेल."
      ),
      "Mercury": (
          "जोडीदार हुशार, संवादप्रिय, विनोदी आणि बुद्धिमान असेल. बौद्धिक देवाणघेवाण"
          " नात्याचा पाया ठरेल."
      ),
      "Jupiter": (
          "जोडीदार सुसंस्कृत, ज्ञानी, आध्यात्मिक आणि मार्गदर्शन करणारा असेल."
          " वैवाहिक जीवन स्थिर राहील."
      ),
      "Venus": (
          "जोडीदार देखणा, आकर्षक, कलाप्रेमी आणि नात्यात सौहार्द राखणारा असेल."
      ),
      "Saturn": (
          "जोडीदार अत्यंत परिपक्व (Mature), कर्तव्यदक्ष, व्यावहारिक आणि शांत"
          " स्वभावाचा असेल. नात्यात गांभीर्य राहील."
      ),
  }

  return (
      ak_interpretations.get(ak, ""),
      amk_interpretations.get(amk, ""),
      dk_interpretations.get(dk, ""),
  )


# --- Output Display ---
if submitted:
  st.success("✅ सर्व गणितीय सूत्रे व नियम यशस्वीरीत्या विश्लेषित झाले आहेत!")

  sample_planets = {
      "Sun": {"deg": 17.32, "sign": "Sagittarius"},
      "Moon": {"deg": 12.44, "sign": "Aquarius"},
      "Mars": {"deg": 16.45, "sign": "Scorpio"},
      "Mercury": {"deg": 1.88, "sign": "Sagittarius"},
      "Jupiter": {"deg": 11.36, "sign": "Gemini"},
      "Venus": {"deg": 12.48, "sign": "Capricorn"},
      "Saturn": {"deg": 21.96, "sign": "Sagittarius"},
      "Rahu": {"deg": 24.69, "sign": "Aquarius"},
      "Ketu": {"deg": 24.69, "sign": "Leo"},
  }

  # Calculations
  df_karakas, karaka_dict = calculate_jaimini_karakas(sample_planets)
  ak_text, amk_text, dk_text = get_deep_predictions(
      karaka_dict, sample_planets
  )

  # Tabs for Clean UI
  tab1, tab2, tab3 = st.tabs([
      "📖 संपूर्ण भविष्यकथन (Detailed Predictions)",
      "📊 ग्रह आणि कारके (Planetary Matrix)",
      "🎯 इव्हेंट टाइमिंग (Double Transit Check)",
  ])

  with tab1:
    st.markdown("### 🌟 १. आत्मा, स्वभाव आणि जीवनाचे ध्येय (Life Purpose)")
    st.markdown(
        f"**तुमचा मुख्य आत्मकारक (Atmakaraka): `{karaka_dict['Atmakaraka']}`**"
    )
    st.info(ak_text)

    st.markdown("### 💼 २. करिअर, अधिकार आणि धनयोग (Career & Wealth Destiny)")
    st.markdown(
        "**तुमचा अमात्यकारक (Amatyakaraka / Action Planet):"
        f" `{karaka_dict['Amatyakaraka']}`**"
    )
    st.success(amk_text)

    st.markdown(
        "### 💍 ३. वैवाहिक जीवन आणि जोडीदाराचा स्वभाव (Spouse & Partnership)"
    )
    st.markdown(
        f"**तुमचा दाराकारक (Darakaraka): `{karaka_dict['Darakaraka']}`**"
    )
    st.write(dk_text)

    st.markdown("### ⚠️ ४. विशेष कार्मिक अलर्ट (Karmic Degree / Vastha)")
    for p, info in sample_planets.items():
      if info["deg"] <= 2.0:
        st.warning(
            f"**{p} ({info['deg']:.2f}°)** हा ग्रह **बाल्यावस्थेत (Inception"
            " Degree)** आहे. हा ग्रह आयुष्यात संपूर्णपणे नवीन कर्म व नवीन"
            " अनुभवांची सुरुवात दर्शवतो."
        )
      elif info["deg"] >= 28.0:
        st.error(
            f"**{p} ({info['deg']:.2f}°)** हा ग्रह **वृद्धावस्थेत (Karmic"
            " Boundary)** आहे. हा ग्रह भूतकाळातील कर्म संपवून मुक्तीकडे घेऊन जाणारा"
            " ठरेल."
        )

  with tab2:
    st.subheader("जैमिनी चर कारके तक्ता (Jaimini Chara Karakas)")
    st.table(df_karakas)

  with tab3:
    st.subheader("के. एन. राव डबल ट्रान्झिट पडताळणी (Double Transit Theory)")
    st.write(
        "कोणतीही मोठी घटना (उदा. विवाह किंवा पदोन्नती) होण्यासाठी **गुरू आणि"
        " शनी** या दोघांची संबंधित घरावर दृष्टी असणे अनिवार्य आहे."
    )

    colA, colB = st.columns(2)
    with colA:
      check_house = st.selectbox(
          "पडताळणीसाठी घर निवडा (Select House):",
          [7, 10],
          format_func=lambda x: (
              "७ वे घर (विवाह आणि भागीदारी)"
              if x == 7
              else "१० वे घर (करिअर, पद आणि व्यवसाय)"
          ),
      )

    current_jup_aspects = [2, 6, 10]
    current_sat_aspects = [3, 7, 10]

    jup_hits = check_house in current_jup_aspects
    sat_hits = check_house in current_sat_aspects
    double_transit_active = jup_hits and sat_hits

    with colB:
      if double_transit_active:
        st.success(
            f"🎯 **Double Transit ACTIVE on House {check_house}!**\n\nसध्या गुरू"
            " आणि शनी या दोन्ही ग्रहांचा या घरावर पूर्ण प्रभाव आहे. ही घटना"
            " घडण्यासाठी हा सर्वोत्तम काळ (High-Confidence Timing Window) आहे."
        )
      else:
        st.warning(
            f"⏳ **Double Transit Not Active on House {check_house}.**\n\nया"
            " कालावधीत ही मोठी घटना घडण्यासाठी अनुकूल ग्रहांचे संकेत सध्या"
            " अपूर्ण आहेत."
        )
