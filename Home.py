from urllib import request
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import streamlit as st
import random
r = random.random()
cred = credentials.Certificate('empsatisfaction.json')
firebase_admin.initialize_app(cred,{'databaseURL': "https://empsatisfaction-default-rtdb.firebaseio.com",},name=str(r))
uid = '7GhfrXkzObPyMbWxOwXqtkhr8qg2'

firebaseConfig = {
  'apiKey': "AIzaSyDmjZZKURIk-ldqoPMZ6b5UXcxaP51qvuk",
  'authDomain': "empsatisfaction.firebaseapp.com",
  'databaseURL': "https://empsatisfaction-default-rtdb.firebaseio.com",
  'projectId': "empsatisfaction",
  'storageBucket': "empsatisfaction.appspot.com",
  'messagingSenderId': "53038019314",
  'appId': "1:53038019314:web:28903d9e19e140fd85d66b"
}

firebase =pyrebase.initialize_app(firebaseConfig)

autho = firebase.auth()
dbs = firebase.database()

surveys = dbs.child("Survey").order_by_key().order_by_child("uid").equal_to(uid).get()
st.write(surveys)
option = st.sidebar.selectbox('',
     options=['Home','Sign Up','Sign In']
)

st.header("Emplyee Satisfaction")
def login(email,password):
     if email is not None:
          if password is not None:
               auth_status = autho.sign_in_with_email_and_password(email,password)
               st.sidebar.success("Succefully Logged in")
               uid = auth_status['localId']
               st.sidebar.subheader("Welcome " + auth_status['displayName'])
               st.sidebar.button('Logout')
               st.write(auth_status)
               Companies = dbs.child("Survey").order_by_child("uid").equal_to(uid).get()
               st.write(Companies)
          else:
               st.warning("Please Enter a Valid Password")
     else:
          st.warning("Please Enter a Valid Email")

def signup(email,password,name):
     if email is not None:
          if password is not None:
               user = auth.create_user(
               email=email,
               email_verified=False,
               password=password,
               display_name=name,
               disabled=False)
               print('Sucessfully created new user: {0}'.format(user.uid))
               st.sidebar.success("Account Succefully created")
          else:
               st.warning("Please Enter a Valid Password")
     else:
          st.warning("Please Enter a Valid Email")
if option =="Sign In":
     st.sidebar.subheader("Sign In")
     email = st.sidebar.text_input('Enter your Email',)
     password = st.sidebar.text_input('Password',type="password")
     st.sidebar.button('Sign In',on_click=login, args=(email,password))
if option =="Sign Up":
     st.sidebar.subheader("Sign Up")
     name = st.sidebar.text_input('Full Name')
     email = st.sidebar.text_input('Enter your Email')
     password = st.sidebar.text_input('Password',type="password")
     st.sidebar.button('Sign Up',on_click=signup, args=(email,password,name))
