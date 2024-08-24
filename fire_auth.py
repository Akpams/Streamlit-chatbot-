import firebase_admin
from firebase_admin import credentials 
from firebase_admin import auth
import streamlit as st
import time
data_key = credentials.Certificate("streamlit-auth-9148c-dbe95cb0b776.json")
# firebase_admin.initialize_app(data_key)

def send_data(email, passw,username):  
    user =auth.create_user(email=email,password=passw, uid=username)
    return user
def get_email(email):
        user =auth.get_user_by_email(email)
        
        
