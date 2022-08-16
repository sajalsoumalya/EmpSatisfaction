import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth

#from .Home import Experience  # pip install streamlit-authenticator


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="EmpSatisfaction", page_icon=":bar_chart:",)

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

st.title("EmpSatisfaction")
st.markdown("##")
x1 = pd.ExcelFile("./survey.xlsx")

sheet = st.selectbox(
    "Select The Survey:",
    options=x1.sheet_names
)
if sheet is not None:
    df = get_data_from_excel(sheet)

    # ---- SIDEBAR ----
    #authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome ")
    st.dataframe(df)
    # ---- MAINPAGE ----



    st.markdown("""---""")
