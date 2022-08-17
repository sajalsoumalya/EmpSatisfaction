import pyrebase
import streamlit as st

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

auth = firebase.auth()
def fetch():
     auth.get_account_info
name = st.text_input('Full Name',placeholder="Enter your Name")
email = st.text_input('Enter your Email',placeholder="Enter your Email")
password = st.text_input('Password',type="password",placeholder="Enter your Password")

def login(email,password):
     if email is not None:
          if password is not None:
               auth_status = auth.create_user_with_email_and_password(email,password)
               st.success("Your Account hass been Created")
          else:
               st.warning("Please Enter a Valid Password")
     else:
          st.warning("Please Enter a Valid Email")

st.button('Sign In',on_click=login, args=(email,password))


