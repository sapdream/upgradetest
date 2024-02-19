# -*- coding: utf-8 -*-
"""Copy of capstone_project_GE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17shBggJYp-lrYlrGpF4CKB_CO4vNPQbq
"""


import streamlit as st
import pickle
import datetime
#do training model
pickle_in = open('rf.pkl', 'rb')
model = pickle.load(pickle_in)

def load_data():
    data = pd.read_csv('capstonedata.csv')
    return data

def getprediction(input_date):

  start_date = datetime.datetime(2024,2,19)
  end_date = datetime.datetime(2025,12,12)

  #y_pred = model.get_forecast(len(test.index))
  #y_pred_df = y_pred.conf_int(alpha = 0.05)
  y_pred_df["Predictions"] = model.predict(start = start_date, end = end_date)
  y_pred_df.index = input_date
  y_pred_out = y_pred_df["Predictions"]
  prediction = y_pred_out[input_date]

  return prediction

  #return y_pred_out

def main():
  st.title('Clinic Peak Hour Prediction System')
  input_text = st.date_input("Enter Date to find busyness")

  
  if st.button('Predict'):
      results = getprediction(input_text)
      st.markdown(results)

if __name__ == "__main__":
    main()
