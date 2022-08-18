from distutils.log import error
from multiprocessing.sharedctypes import Value
import pickle
from pathlib import Path
from tabnanny import check
from typing_extensions import Self
import matplotlib.pyplot as plt

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit


from collections import Counter

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="EmpSatisfaction", page_icon=":bar_chart:",)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


import random
r = random.random()
cred = credentials.Certificate('empsatisfaction.json')
firebase_admin.initialize_app(cred,{'databaseURL': "https://empsatisfaction-default-rtdb.firebaseio.com"}, name=str(r))
ref = db.reference('Survey/')


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

st.title("EmpSatisfaction")
st.markdown("##")
x1 = pd.ExcelFile("./survey.xlsx")

# ---- SIDEBAR ----
#authenticator.logout("Logout", "sidebar")
st.sidebar.title(f"Welcome ")
page = st.sidebar.selectbox('Pages',options=['Analise','Create'])
if page == 'Analise':
    survey_list = get_survey_list()
    selected_survey = st.selectbox(
    "Select The Survey:",
    options=survey_list
    )
    if selected_survey is not None:
        survey = ref.child(selected_survey).order_by_key().get()
        del survey["name"]
        del survey["uid"]
        survey_lenght = len(survey)
        st.subheader(survey_lenght,"number of People Attended This Survey")
        satis = []
        for keys,val in survey.items():
            satis.append(val['Satisfaction'])
        count = Counter(satis)
        labels = list(count)
        sizes = list(count.values())
        #explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes,labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal') 
        st.pyplot(fig1)
if page == 'Create':
    email = st.text_input('Email',placeholder="Enter your Email")
    survey_name = st.text_input('Survey Name',placeholder="Enter your Survey Name")
    companey_name = st.text_input('Companey Name',placeholder="Enter your Companey Name")
    if st.button("Create"):
        value = check(survey_name)
        if value == True:
            ref.child(survey_name).set({
                "companey_name":companey_name,
                "email":email
            })
            st.success("Survey Created")
        else:
            st.error(":error: Survey name already exist")


# ---- MAINPAGE ----

