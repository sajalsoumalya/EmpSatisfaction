import firebase_admin
import streamlit as st


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('empsatisfaction.json')
firebase_admin.initialize_app(cred,{'databaseURL': 'https://empsatisfaction-default-rtdb.firebaseio.com'})
firebase_admin.get_app()

"""try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate('empsatisfaction.json')
    firebase_admin.initialize_app(cred,{'databaseURL': 'https://empsatisfaction-default-rtdb.firebaseio.com'})
    firebase_admin.get_app()"""
ref = db.reference("py/")
users_ref = ref.child('users')
users_ref.set({
  'i':{
    'name':'SOUMALYA',
    'DOB':'11'
  }
})
"""
  "apiKey": "AIzaSyDmjZZKURIk-ldqoPMZ6b5UXcxaP51qvuk",
  "authDomain": "empsatisfaction.firebaseapp.com",
  "projectId": "empsatisfaction",
  "databaseURL": "https://empsatisfaction-default-rtdb.firebaseio.com",
  "storageBucket": "empsatisfaction.appspot.com",
  "messagingSenderId": "53038019314",
  "appId": "1:53038019314:web:886437c48be901df85d66b"
}
"""