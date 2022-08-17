import random
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

r=random.randint(1,10000)
app_options = { 
  'projectId': 'empsatisfaction',
  'databaseURL': 'https://empsatisfaction-default-rtdb.firebaseio.com',
  'storageBucket': 'empsatisfaction.appspot.com'
  }

cred = credentials.Certificate('./empsatisfaction.json')
App = firebase_admin.initialize_app(cred,options=app_options, name=str(r))

from firebase_admin import auth
