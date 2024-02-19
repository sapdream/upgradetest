# -*- coding: utf-8 -*-
"""capstone_v4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GMBXFYKjHX039JjxVRZmZudAgpiHqwVb
"""

import streamlit as st
import pickle
import datetime
import pandas as pd
#do training model
pickle_in = open('rf.pkl', 'rb')
model = pickle.load(pickle_in)

def load_data():
    data = pd.read_csv('out.csv')
    return data

def getprediction(input_date):
  data = load_data()
  input_date = input_date.strftime("%Y/%m/%d/")
  index_future_dates=pd.date_range(start='2024-01-26', end='2024-02-25')

  pred=model.predict(start=len(data),end=len(data)+30,typ='levels').rename('ARMA Predictions')
  pred.index = index_future_dates
  prediction = pred[input_date]
  prediction = round(prediction)

  return prediction

  #return y_pred_out

def main():
  st.title('Clinic Peak Hour Prediction System')
  input_text = st.date_input("Enter Date to find busyness")
  data = load_data()

  if st.button('Predict'):
      results = getprediction(input_text)
      st.markdown(results)
      maximum_count = max(data['count'])
      minimum_count = min(data['count'])
      highest_count = maximum_count - minimum_count
      if maximum_count > prediction and highest_count < prediction:
        print("Busy")
      else:
        print("Not Busy")

if __name__ == "__main__":
    main()
