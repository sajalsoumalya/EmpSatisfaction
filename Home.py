import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config('Emp Satisfaction',layout="centered")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header('Emp Satisfaction')
col1, col2, col3, col4,col5 = st.columns([2,2,2,3,2])
with col1:
    Industry_type = st.selectbox(
        'Industry type',
        ('IT','Education','RealEstate')
    )
with col2:
    Age = st.number_input('Age',min_value=20,max_value=100)
with col3:
    Qualification = st.selectbox(
        'Qualification',
        ('Diploma','Bachelors','Masters','Professional/ others')
    )
with col4:
    Experience = st.selectbox(
        'Experience',
        ('1 to less than 5 years ','2.5 to less than 10 years','Above 10 years ')
    )
with col5:
    Gender = st.selectbox(
        "Gender",
        ('Male', 'Female'))
color = st.select_slider(
     'I feel fairly well satisfied with my present job',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Most days I am enthusiastic about my work',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Each day of work seems like it will never end',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I find real enjoyment in my work',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I consider my job rather unpleasant',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'It is not always easy for me to perform tasks on time',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'When I have a deadline to perform a certain task, I always finish it on time',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I always leave my tasks to the last minute',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Sometimes, I feel disappointed with my performance at work, because I know I could have done',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I felt downhearted and blue during the past few weeks',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I felt bothered during the past few weeks ',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I was emotionally stable and sure of myself during the past few weeks',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I felt cheerful, lighthearted during the past few weeks',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'I felt tired, worn out, used up, or exhausted during the past few weeks.',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Thoughts of being absent',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Discuss with coworkers about non-work issues',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Spent work time on personal matters',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Thoughts of leaving current job',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
color = st.select_slider(
     'Put less effort into job than should have',
     options=['Strongly Disagree', 'Disagree', 'Neutral', 'agree', 'strongly agree'])
if st.button('Submit'):
    st.write("Wow");