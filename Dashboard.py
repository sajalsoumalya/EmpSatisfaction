from lib2to3.pgen2 import driver
from logging import PlaceHolder
import matplotlib.pyplot as plt
import pandas as pd  
import streamlit as st
import numpy as np # np mean, np random 


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import plotly.express as px # interactive charts 
import time # to simulate a real time data, time loop 



from collections import Counter

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard Employee Satisfaction", page_icon=":bar_chart:",layout="wide",initial_sidebar_state="collapsed")
with open('Dashboard.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

import random
r = random.random()
if not firebase_admin._apps:
    cred = credentials.Certificate('empsatisfaction.json')
    firebase_admin.initialize_app(cred,{'databaseURL': "https://empsatisfaction-default-rtdb.firebaseio.com"})
ref = db.reference('Survey/')

#to get the url of the current page 
def get_curent_url():
    driver = webdriver.Chrome()
    get_url = driver.current_url
    return get_url
    # ---- READ EXCEL ----
@st.cache

# def get_data_from_excel(sheet_name):
#     df = pd.read_excel(
#         io="./survey.xlsx",
#         sheet_name=sheet_name,
#         na_filter = True
#     )
#     # Add 'hour' column to dataframe
#     #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
#     return df


def check(key):
    k = True
    value = ref.order_by_key().equal_to(key).get()
    length = len(list(value.keys()))
    if(length>0):
        k=False
    
    return k
#function to get the list of Surveys
def get_survey_list():
    survey_list = ref.order_by_key().get()
    return list(survey_list.keys())

from streamlit_option_menu import option_menu #for Menubar

menu = option_menu(None, ["Dashboard", "Create Survey","Manage Surveys"], 
    icons=['house', 'cloud-upload','gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

st.title("Emplyee Satisfaction Dashboard")
st.markdown("##")
#x1 = pd.ExcelFile("./survey.xlsx")
selected_survey = ''

if menu == 'Dashboard':
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
       
        if(survey_lenght<=0):
            #st.subheader(str(survey_lenght) + " number of people attended this survey")
            st.subheader("No one has attended this survey")
        else:
            satis = []
            df = pd.DataFrame(columns=["Qualification","Age","Experience","Gender","PRESENT JOB FEELING","ENTHUSIASM","WORKOVERLD","ENJOYMNT","UNPLSNTTASK","TOUGH PERFORMNCE","TIME MNGMNT","DISAPNTMNT","DOWNHRTED","BOTHRED","EMOSNAL STABLTY","CHEERUL","TIRED","ABSNT MIND","DISCUSS CO-WORKER","PERSNL MTTR","THOUGHT OF LEAVING","LESS EFFORT","Satisfaction"])
            #["Qualification","Age","Experience""Gender","PRESENT JOB FEELING","ENTHUSIASM","WORKOVERLD","ENJOYMNT","UNPLSNTTASK","TOUGH PERFORMNCE","TIME MNGMNT","DISAPNTMNT","DOWNHRTED","BOTHRED","EMOSNAL STABLTY","CHEERUL","TIRED","ABSNT MIND","DISCUSS CO-WORKER","PERSNL MTTR","THOUGHT OF LEAVING","LESS EFFORT"]
            for keys,val in survey.items():
                satis.append(val['Satisfaction'])
                row = []
                row.append(val["Qualification"])
                row.append(val["Age"])
                row.append(val["Experience"])
                row.append(val["Gender"])
                row.append(val["PRESENT JOB FEELING"])
                row.append(val["ENTHUSIASM"])
                row.append(val["WORKOVERLD"])
                row.append(val["ENJOYMNT"])
                row.append(val["UNPLSNTTASK"])
                row.append(val["TOUGH PERFORMNCE"])
                row.append(val["TIME MNGMNT"])
                row.append(val["DISAPNTMNT"])
                row.append(val["DOWNHRTED"])
                row.append(val["BOTHRED"])
                row.append(val["EMOSNAL STABLTY"])
                row.append(val["CHEERUL"])
                row.append(val["TIRED"])
                row.append(val["ABSNT MIND"])
                row.append(val["DISCUSS CO-WORKER"])
                row.append(val["PERSNL MTTR"])
                row.append(val["THOUGHT OF LEAVING"])
                row.append(val["LESS EFFORT"])
                row.append(val['Satisfaction'])
                df.loc[len(df.index)] = row

            placeholder = st.empty()
            with placeholder.container():
                # create three columns
                kpi1, kpi2, kpi3 = st.columns(3)
                # fill in those three columns with respective metrics or KPIs 
                kpi1.metric(label="Avarage Age ⏳", value=np.mean(df['Age']), delta= np.mean(df['Age']-10))
                kpi2.metric(label="Gender Ratio 💍", value= 'N/A', delta= 'N/A')
                kpi3.metric(label="Response Count ", value= survey_lenght)

                # create two columns for charts 

                fig_col1, fig_col2, fig_col3 = st.columns(3)
                with fig_col1:
                    st.markdown("### Density Heatmap")
                    fig = px.density_heatmap(data_frame=df, y = 'Age', x = 'Satisfaction')
                    st.write(fig)
                with fig_col2:
                    st.markdown("### Age Histogram")
                    fig2 = px.histogram(data_frame = df, x = 'Age')
                    st.write(fig2)
                with fig_col3:
                    st.markdown("### Pie of Satisfaction")
                    fig3 = px.pie(data_frame = df, values=sizes)
                    st.write(fig3)
                st.markdown("### Detailed Data View")
                st.dataframe(df)
                time.sleep(1)
if menu == 'Create Survey':
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
if menu == 'Manage Surveys':
    st.write("Survey Link")
    code = 'https://sajalsoumalya-empsatisfaction-dashboard-vda1pn.streamlitapp.com/Survey/?survey='+str(selected_survey)
    st.code(code)
# ---- MAINPAGE ----

