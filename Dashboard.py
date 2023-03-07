from lib2to3.pgen2 import driver # for geting web url
from logging import PlaceHolder
import pandas as pd  # for dataframe
import streamlit as st #stremlit framework
import numpy as np # np mean, np random 
import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import plotly.express as px # interactive charts 
import time # to simulate a real time data, time loop 

from collections import Counter

from streamlit_option_menu import option_menu #for Menubar

import json

import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml

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



selected_comp = None
comp_email = None
selected_survey = None
survey_passcode = None
uploaded_csv = None

def uplaod_data_from_csv(df, comp, survey):
    features=x=df[df.columns[4:]].values
    loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
    result1 = loaded_model.predict(x)
    result_index = json.dumps(int(result1[0]))
    result_index = int(result_index)-1
    print(result_index)
    list_val=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree']
    print(list_val[result_index])
    slink = comp+'/'+survey
    for ind in df.index:
        s={
            "Qualification":df['Qualification'][ind],
            "Age":json.dumps(int(df['Age'][ind])),
            "Experience":df['Experience'][ind],
            "Gender":df['Gender'][ind],
            "ENTHUSIASM":json.dumps(int(df['ENTHUSIASM'][ind])),
            "WORKOVERLD":json.dumps(int(df['WORKOVERLD'][ind])),
            "ENJOYMNT":json.dumps(int(df['ENJOYMNT'][ind])),
            "UNPLSNTTASK":json.dumps(int(df['UNPLSNTTASK'][ind])),
            "TOUGH PERFORMNCE":json.dumps(int(df['TOUGH PERFORMNCE'][ind])),
            "TIME MNGMNT":json.dumps(int(df['TIME MNGMNT'][ind])),
            "DISAPNTMNT":json.dumps(int(df['DISAPNTMNT'][ind])),
            "DOWNHRTED":json.dumps(int(df['DOWNHRTED'][ind])),
            "BOTHRED":json.dumps(int(df['BOTHRED'][ind])),
            "EMOSNAL STABLTY":json.dumps(int(df['EMOSNAL STABLTY'][ind])),
            "CHEERUL":json.dumps(int(df['CHEERUL'][ind])),
            "TIRED":json.dumps(int(df['TIRED'][ind])),
            "ABSNT MIND":json.dumps(int(df['ABSNT MIND'][ind])),
            "DISCUSS CO-WORKER":json.dumps(int(df['DISCUSS CO-WORKER'][ind])),
            "PERSNL MTTR":json.dumps(int(df['PERSNL MTTR'][ind])),
            "THOUGHT OF LEAVING":json.dumps(int(df['THOUGHT OF LEAVING'][ind])),
            "LESS EFFORT":json.dumps(int(df['LESS EFFORT'][ind])),
            "Satisfaction":list_val[result_index]
            }
        ref.child(slink).push().set(s)

df = pd.DataFrame(
    columns=[
        "Qualification","Age","Experience","Gender",
        "ENTHUSIASM","WORKOVERLD","ENJOYMNT","UNPLSNTTASK",
        "TOUGH PERFORMNCE","TIME MNGMNT","DISAPNTMNT",
        "DOWNHRTED","BOTHRED","EMOSNAL STABLTY",
        "CHEERUL","TIRED","ABSNT MIND","DISCUSS CO-WORKER",
        "PERSNL MTTR","THOUGHT OF LEAVING",
        "LESS EFFORT","Satisfaction"
        ],dtype=np.int8)
df_csv = pd.DataFrame(columns=["Qualification","Age","Experience","Gender","ENTHUSIASM","WORKOVERLD","ENJOYMNT","UNPLSNTTASK","TOUGH PERFORMNCE","TIME MNGMNT","DISAPNTMNT","DOWNHRTED","BOTHRED","EMOSNAL STABLTY","CHEERUL","TIRED","ABSNT MIND","DISCUSS CO-WORKER","PERSNL MTTR","THOUGHT OF LEAVING","LESS EFFORT"])

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
demo_csv = convert_df(df_csv)


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#authenticator = stauth.Authenticate(names,usernames,hashed_passwords,"sales_dashboard", "abcdef",cookie_expiry_days= 30)
log_tab1,log_tab2,log_tab3,log_tab4 = st.tabs(["Login","Register","Forget Password","Change Password"])
with log_tab1:
    name, authentication_status, username = authenticator.login('Login', 'main')
    if st.session_state["authentication_status"]:
        st.markdown(
    """
<style>
    [data-baseweb="tab-list"],
    [data-baseweb="tab-border"]{
        display:none;
    }

    .stTabs{
        display:block;
    }</style>
""",
    unsafe_allow_html=True,
)
        menu = option_menu(None, ["Dashboard", "Create Survey","Manage Surveys"], 
        icons=['house', 'cloud-upload','gear','user'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
        if menu == 'Dashboard':
            tit_col1,tit_col2 = st.columns([8,2])
            tit_col1.subheader(f'Welcome to Employee Satisfaction Dashboard Mr.*{st.session_state["name"]}*')
            with tit_col2:
                authenticator.logout('Logout', 'main')
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
                        ch = selected_comp+'/'+selected_survey
                        survey = ref.child(ch).order_by_key().get()
                        survey_passcode = str(survey["passcode"])
                        del survey["passcode"]
                        survey_lenght = len(survey)
                        if(survey_lenght<=0):
                            #st.subheader(str(survey_lenght) + " number of people attended this survey")
                            st.subheader("No one has attended this survey")
                        else:
                            for vals in survey:
                                val = survey[vals]
                                row = [
                                    val["Qualification"],val["Age"],val["Experience"],val["Gender"],
                                    val["ENTHUSIASM"],val["WORKOVERLD"],val["ENJOYMNT"],val["UNPLSNTTASK"],
                                    val["TOUGH PERFORMNCE"],val["TIME MNGMNT"],val["DISAPNTMNT"],
                                    val["DOWNHRTED"],val["BOTHRED"],val["EMOSNAL STABLTY"],
                                    val["CHEERUL"],val["TIRED"],val["ABSNT MIND"],val["DISCUSS CO-WORKER"],
                                    val["PERSNL MTTR"],val["THOUGHT OF LEAVING"],
                                    val["LESS EFFORT"],val["Satisfaction"]
                                ]
                                print(type(val))
                                # row.append(val['Qualification'])
                                # row.append(val['Age'])
                                # row.append(val['Experience'])
                                # row.append(val['Gender'])
                                # row.append(val['ENTHUSIASM'])
                                # row.append(val['WORKOVERLD'])
                                # row.append(val['ENJOYMNT'])
                                # row.append(val['UNPLSNTTASK'])
                                # row.append(val['TOUGH PERFORMNCE'])
                                # row.append(val['TIME MNGMNT'])
                                # row.append(val['DISAPNTMNT'])
                                # row.append(val['DOWNHRTED'])
                                # row.append(val['BOTHRED'])
                                # row.append(val['EMOSNAL STABLTY'])
                                # row.append(val['CHEERUL'])
                                # row.append(val['TIRED'])
                                # row.append(val['ABSNT MIND'])
                                # row.append(val['DISCUSS CO-WORKER'])
                                # row.append(val['PERSNL MTTR'])
                                # row.append(val['THOUGHT OF LEAVING'])
                                # row.append(val['LESS EFFORT'])
                                # row.append(val['Satisfaction'])
                                df.loc[len(df.index)] = row
                                #df = df.append(val, ignore_index = True)

            female = df['Gender'].tolist().count('Female')
            male = df['Gender'].tolist().count('Male')
            ratio = str(male) +"    :"+str(female)

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
                    companey_name = st.text_input('Company Name',placeholder="Enter your Companey Name", value=st.session_state["name"], disabled= True)
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
                                code = 'https://empsatisfaction.streamlit.app/Survey/?survey='+str(link)
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
                    survey_name = str(selected_survey)
                    survey_nam = survey_name.replace(" ", "_")
                    link = selected_comp+'&survey='+survey_nam
                    code = 'https://empsatisfaction.streamlit.app/Survey/?survey='+str(link)
                    st.code(code)
                with col2:
                    st.write("Delete Survey")
                    if st.button('Delete'):
                        st.write("Deleted")
                row2_col1, row2_col2 = st.columns([5,5])
                uploaded_file = None
                with row2_col1:            
                    uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type = ['csv'])

                with row2_col2:
                    if uploaded_file is not None:
                        uploaded_csv = pd.read_csv(uploaded_file)
                        st.dataframe(uploaded_csv)
                        
                        if st.button("Upload data"):
                            uplaod_data_from_csv(uploaded_csv,selected_comp,selected_survey)
                    else:
                        st.subheader("Please use the refarence Templete.csv")
                        st.download_button(
                            "Download Tamplate CSV",
                            demo_csv,
                            "tamplate.csv",
                            "text/csv",
                            key='download-csv'
                        )
            
        # ---- MAINPAGE ----
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
#    elif st.session_state["authentication_status"] is None:
#        st.warning('Please enter your username and password')
with log_tab2:
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)
    with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
with log_tab3:
    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
        if username_forgot_pw:
            st.success('New password sent securely')
            # Random password to be transferred to user securely
        if authenticator.forgot_password('Forgot password') is None:
            st.markdown("##")
        else:
            st.error('Username not found')
    except Exception as e:
        st.error(e)
with log_tab4:
    if authentication_status:
        try:
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)