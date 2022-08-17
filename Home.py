from urllib import request
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


option = st.sidebar.selectbox('',
     options=['Home','Sign Up','Sign In']
)
def logout(request):
    try:
        del request.session['token_id']
    except KeyError:
        pass
    return st.sidebar.warning("You're logged out.")

auth = firebase.auth()
st.header("Emplyee Satisfaction")
def login(email,password):
     if email is not None:
          if password is not None:
               auth_status = auth.sign_in_with_email_and_password(email,password)
               
               st.sidebar.success("Succefully Logged in")
               col1,col2 = st.columns([3,1])
               with col1:
                    st.sidebar.subheader("Welcome")
               with col2:
                    st.sidebar.button('Logout',on_click=logout, args=(request))
               st.write(auth_status)
          else:
               st.warning("Please Enter a Valid Password")
     else:
          st.warning("Please Enter a Valid Email")

def signup(email,password,name):
     if email is not None:
          if password is not None:
               auth_status = auth.create_user_with_email_and_password(email,password)
               st.sidebar.success("Account Succefully created")
               st.write(auth_status)
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
