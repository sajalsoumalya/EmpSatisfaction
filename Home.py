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

email = st.text_input('Enter your Email',)
password = st.text_input('Password',type="password")

if st.button('Sign In') and {email,password} is not None:
     #auth.create_user_with_email_and_password(email,password)
     auth.sign_in_with_email_and_password(email,password)
     st.write(auth.get_account_info(email))
else:
     st.write('Opps')