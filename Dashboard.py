from lib2to3.pgen2 import driver # for geting web url
from logging import PlaceHolder
import pandas as pd  # for dataframe
import streamlit as st #stremlit framework
import numpy as np # np mean, np random 


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import plotly.express as px # interactive charts 
import time # to simulate a real time data, time loop 

from collections import Counter

from streamlit_option_menu import option_menu #for Menubar

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Employee Satisfaction Dashboard", page_icon=":bar_chart:",layout="wide",initial_sidebar_state="collapsed")
with open('Dashboard.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

import random
r = random.random()
if not firebase_admin._apps:
    cred = credentials.Certificate('empsatisfaction.json')
    firebase_admin.initialize_app(cred,{'databaseURL': "https://empsatisfaction-default-rtdb.firebaseio.com"})
ref = db.reference('Survey/')

#to get the url of the current page 
@st.cache_data
def get_curent_url():
    driver = webdriver.Chrome()
    get_url = driver.current_url
    return get_url
    # ---- READ EXCEL ----


# def get_data_from_excel(sheet_name):
#     df = pd.read_excel(
#         io="./survey.xlsx",
#         sheet_name=sheet_name,
#         na_filter = True
#     )
#     # Add 'hour' column to dataframe
#     #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
#     return df
def check(key,name):
    k = True
    surveyref = db.reference('Survey/'+name)
    value = surveyref.order_by_key().equal_to(key).get()
    length = len(list(value.keys()))
    if(length>0):
        k=False
    return k
#function to get the list of Surveys

def get_company_list():
    company_list = ref.order_by_key().get()
    return list(company_list.keys())

def get_survey_list(cmp):
    ref2 = ref.child(cmp)
    survey_list = ref2.order_by_key().get()
    email = survey_list["email"]
    del survey_list["email"]
    return list(survey_list.keys()),email

from streamlit_option_menu import option_menu #for Menubar

menu = option_menu(None, ["Dashboard", "Create Survey","Manage Surveys"], 
    icons=['house', 'cloud-upload','gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

selected_comp = None
comp_email = None
selected_survey = None
survey_passcode = None
df = pd.DataFrame(columns=["Qualification","Age","Experience","Gender","ENTHUSIASM","WORKOVERLD","ENJOYMNT","UNPLSNTTASK","TOUGH PERFORMNCE","TIME MNGMNT","DISAPNTMNT","DOWNHRTED","BOTHRED","EMOSNAL STABLTY","CHEERUL","TIRED","ABSNT MIND","DISCUSS CO-WORKER","PERSNL MTTR","THOUGHT OF LEAVING","LESS EFFORT","Satisfaction"])

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
csv = convert_df(df)


if menu == 'Dashboard':
    st.title("Employee Satisfaction Dashboard")
    r_col1,r_col2 = st.columns(2)
    with r_col1:
        company_list = get_company_list()
        selected_comp = st.selectbox(
        "Select Your Company:",
        options=company_list
        )
    with r_col2:
        if selected_comp is not None:
            survey_list, comp_email = get_survey_list(selected_comp)
            selected_survey = st.selectbox(
            "Select Your survey:",
            options=survey_list
            )
            if selected_survey is not None:
               
                ref2 = ref.child(selected_comp)
                survey = ref2.child(selected_survey).order_by_key().get()
                survey_passcode = str(survey["passcode"])
                del survey["passcode"]
                survey_lenght = len(survey)
                if(survey_lenght<=0):
                    #st.subheader(str(survey_lenght) + " number of people attended this survey")
                    st.subheader("No one has attended this survey")
                else:
                    for keys,val in survey.items():
                        row = []
                        row.append(val["Qualification"])
                        row.append(val["Age"])
                        row.append(val["Experience"])
                        row.append(val["Gender"])
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
    female = df['Gender'].tolist().count('Female')
    male = df['Gender'].tolist().count('Male')
    ratio = str(male) +":"+str(female)

    placeholder = st.empty()
    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)
        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Compeny Name 💍", value=selected_comp, delta=comp_email)
        kpi2.metric(label="Response Count ", value= survey_lenght, delta = 'Employees')
        kpi3.metric(label="Gender Ratio ⏳", value= ratio, delta= 'Male:Female')

        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Density Heatmap")
            feature_list = df.columns.values.tolist()
            selected_feature = st.selectbox(
            "Select The Survey:",
            options=feature_list
            )
            fig = px.density_heatmap(data_frame=df, y = selected_feature, x = 'Satisfaction')
            st.write(fig)
        with fig_col2:
            st.markdown("### Age Histogram")
            fig2 = px.histogram(data_frame = df, x = 'Satisfaction')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
if menu == 'Create Survey':
    st.title("Create a Survey")
    placeHolder = st.empty()
    with placeHolder.form("Enter the Following Details"):
        companey_name = None
        email = None
        survey_name= None
        passcode = None
        submitted = None
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            companey_name = st.text_input('Company Name',placeholder="Enter your Companey Name")
        with row1_col2:
            email = st.text_input('Email',placeholder="Enter your Email")
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            survey_name = st.text_input('Survey Name',placeholder="Enter your Survey Name")
        with row2_col2:
            passcode = st.text_input('Survey Passcode',type="password", key="password")
        submitted = st.form_submit_button("Create")
        if submitted:
            #companey_nam = check(companey_nam)
            survey = check(survey_name,companey_name)
            if survey == True:
                survey_name = str(survey_name)
                survey_nam = survey_name.replace(" ", "_")
                ref.child(companey_name).set({
                    "email":email,
                })
                ch = companey_name+'/'+survey_nam
                ref.child(ch).set({"passcode":passcode})
                with placeHolder:
                        st.success("Survey Created")
                        link = companey_name+'&survey='+survey_nam
                        code = 'https://sajalsoumalya-empsatisfaction-dashboard-vda1pn.streamlitapp.com/Survey/?survey='+str(link)
                        st.code(code)
            else:
                st.error(":error: Survey name already exist")
if menu == 'Manage Surveys':
    selected_comp = None
    selected_survey = None
    survey_list = None
    df = []
    st.title("Manage Your Survey")
    row1_col1, row1_col2, row1_col3, = st.columns(3)
    with row1_col1:
        company_list = get_company_list()
        selected_comp = st.selectbox(
        "Select Your Company:",
        options=company_list
        )
    with row1_col2:
        if selected_comp is not None:
            selected_survey = None
            survey_list, comp_email = get_survey_list(selected_comp)
            selected_survey = st.selectbox(
            "Select Your survey:",
            options=survey_list
            )
            slink = selected_comp+'/'+selected_survey
            survey = ref.child(slink).order_by_key().get()
            survey_passcode = survey["passcode"]
            del survey["passcode"]
            survey_lenght = len(survey)
    with row1_col3:
        kp1,kp2= st.columns(2)
        kp1.metric(label="Response Count ", value= survey_lenght, delta = 'Employees')
        kp2.metric(label="Survey Count ", value= len(survey_list), delta = 'Surveys')
    if selected_survey is not None:
        survey = ref.child(selected_survey).order_by_key().get()
        col1, col2 = st.columns([7, 1])
        with col1:
            st.write("Survey Link")
            code = 'https://sajalsoumalya-empsatisfaction-dashboard-vda1pn.streamlitapp.com/Survey/?survey='+str(selected_survey)
            st.code(code)
        with col2:
            st.write("Delete Survey")
            if st.button('Delete'):
                st.write("Deleted")
        row2_col1, row2_col2 = st.columns([3,5])
        uploaded_file = None
        with row2_col1:            
            uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type = ['csv'])

        with row2_col2:
            if uploaded_file is not None:
                csv = pd.read_csv(uploaded_file)
                st.dataframe(csv)
            else:
                st.subheader("Please use the refarence Templete.csv")
                st.download_button(
                    "Download Tamplate CSV",
                    csv,
                    "file.csv",
                    "text/csv",
                    key='download-csv'
                )

# ---- MAINPAGE ----

