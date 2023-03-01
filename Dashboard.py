from lib2to3.pgen2 import driver
from logging import PlaceHolder
import matplotlib.pyplot as plt
import pandas as pd  
import streamlit as st


from collections import Counter

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="EmpSatisfaction", page_icon=":bar_chart:",)
with open('Dashboard.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import random
r = random.random()
if not firebase_admin._apps:
    cred = credentials.Certificate('empsatisfaction.json')
    firebase_admin.initialize_app(cred,{'databaseURL': "https://empsatisfaction-default-rtdb.firebaseio.com"})
ref = db.reference('Survey/')

def get_curent_url():
    driver = webdriver.Chrome()
    get_url = driver.current_url
    return get_url
    # ---- READ EXCEL ----
@st.cache
def get_data_from_excel(sheet_name):
    df = pd.read_excel(
        io="./survey.xlsx",
        sheet_name=sheet_name,
        na_filter = True
    )
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
def check(key):
    k = True
    value = ref.order_by_key().equal_to(key).get()
    length = len(list(value.keys()))
    if(length>0):
        k=False
    
    return k
def get_survey_list():
    survey_list = ref.order_by_key().get()
    return list(survey_list.keys())

st.title("Emplyee Satisfaction Dashboard")
st.markdown("##")
x1 = pd.ExcelFile("./survey.xlsx")

# ---- SIDEBAR ----
#authenticator.logout("Logout", "sidebar")
st.sidebar.title(f"Welcome ")
page = st.sidebar.selectbox('Pages',options=['Analyze','Create'])
if page == 'Analyze':
    survey_list = get_survey_list()
    selected_survey = st.selectbox(
    "Select The Survey:",
    options=survey_list
    )
    if selected_survey is not None:
        survey = ref.child(selected_survey).order_by_key().get()
        del survey["companey_name"]
        del survey["email"]
        survey_lenght = len(survey)
        st.write("Survey Link")
        code = 'https://sajalsoumalya-empsatisfaction-dashboard-vda1pn.streamlitapp.com/Survey/?survey='+str(selected_survey)
        st.code(code)
        if(survey_lenght>0):
            st.subheader(str(survey_lenght) + " number of people attended this survey")
        else:
            st.subheader("No one has attended this survey")
        satis = []
        for keys,val in survey.items():
            satis.append(val['Satisfaction'])
        count = Counter(satis)
        labels = list(count)
        sizes = list(count.values())
        #explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes,labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal') 
        st.pyplot(fig1)
if page == 'Create':
    placeHolder = st.empty()
    with placeHolder.form("create_survey"):
        email = st.text_input('Email',placeholder="Enter your Email")
        survey_name = st.text_input('Survey Name',placeholder="Enter your Survey Name")
        companey_name = st.text_input('Company Name',placeholder="Enter your Companey Name")
        submitted = st.form_submit_button("Create")
    if submitted:
        value = check(survey_name)
        if value == True:
            survey_name = str(survey_name)
            survey_nam = survey_name.replace(" ", "_")
            ref.child(survey_nam).set({
                "companey_name":companey_name,
                "email":email
            })
            with placeHolder:
                    st.success("Survey Created")
                    code = 'https://sajalsoumalya-empsatisfaction-dashboard-vda1pn.streamlitapp.com/Survey/?survey='+str(survey_nam)
                    st.code(code)
        else:
            st.error(":error: Survey name already exist")


# ---- MAINPAGE ----

