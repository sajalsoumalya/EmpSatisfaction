import pyrebase
import streamlit as st

config = {
  "apiKey": "AIzaSyDmjZZKURIk-ldqoPMZ6b5UXcxaP51qvuk",
  "authDomain": "empsatisfaction.firebaseapp.com",
  "projectId": "empsatisfaction",
  "databaseURL": "https://empsatisfaction-default-rtdb.firebaseio.com",
  "storageBucket": "empsatisfaction.appspot.com",
  "messagingSenderId": "53038019314",
  "appId": "1:53038019314:web:886437c48be901df85d66b"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)

# Get a reference to the database service
db = firebase.database()

# data to save
data = {
    "name": "Mortimer 'Morty' Smith"
}

# Pass the user's idToken to the push method
results = db.child("users").push(data, user['idToken'])
