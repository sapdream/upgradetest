# -*- coding: utf-8 -*-
"""Copy of capstone_project_GE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17shBggJYp-lrYlrGpF4CKB_CO4vNPQbq
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

data = pd.read_csv('capstonedata.csv')

visit_date = data['visit_date']
#check visit_ date type

visit_date1=visit_date.astype("string")
#convert to string so that we can split the date and time

new = visit_date1.str.split(" ", n=1, expand=True)
visit_date2= new[0]
#split as new column

visit_date3= pd.to_datetime(visit_date2)
#convert back to date time

data2= data.drop(['visit_date'],axis=1)
#drop the visit_date column #drop object Visit Date

data2.insert(3,"visit_date",visit_date3,True) #insert datetime date
#insert back the date column only

doctor_id = data2['doctor_id']

m1 = doctor_id.ne(doctor_id.shift())
m2 = visit_date.ne(visit_date.shift())
data2['visit_count'] = data2.groupby((m1 | m2).cumsum()).cumcount().add(1).values
#count the number of patients in a day

data3 =data2.groupby(data2['visit_date'],as_index=False).sum('count') #,as_index=False group the count by date
Visdate = data3.visit_date

data3=data3.set_index('visit_date') #set the visit_date as index

import pandas_datareader.data as web
import datetime

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#display the max amount of columns and rows

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

plt.ylabel('Amount of patients')
plt.xlabel('date')
plt.xticks(rotation=45)

Vdate = data3.index
VCount= data3.visit_count
plt.plot(Vdate, VCount, )
#plot the date and count into a graph

train = data3[Vdate < pd.to_datetime("2022-11-01", format='%Y-%m-%d')]
test = data3[Vdate > pd.to_datetime("2022-11-01", format='%Y-%m-%d')]

#split the data into training and testing data

plt.plot(train, color='black')
plt.plot(test, color='red')
plt.ylabel('Number of Patients')
plt.xlabel('date')
plt.xticks(rotation=45)
plt.title("Train/Test split for Patient Data")
plt.show()

plt.legend()

from statsmodels.tsa.statespace.sarimax import SARIMAX

import streamlit as st

def getprediction(input_date):
  y = train['visit_count']

  ARMAmodel = SARIMAX(y, order = (1, 0, 1))
  ARMAmodel = ARMAmodel.fit()

  y_pred = ARMAmodel.get_forecast(len(test.index))
  y_pred_df = y_pred.conf_int(alpha = 0.05)
  y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
  y_pred_df.index = test.index
  y_pred_out = y_pred_df["Predictions"]

  return y_pred_out

def main():
  st.title('Clinic Peak Hour Prediction System')
  input_text = st.date_input("Enter Date to find busyness")

  results = getprediction(input_text)
  st.markdown(results)

if __name__ == "__main__":
    main()

"""#1. ARMA"""

y = train['visit_count']

ARMAmodel = SARIMAX(y, order = (1, 0, 1))
ARMAmodel = ARMAmodel.fit()

y_pred = ARMAmodel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05)
y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = test.index
y_pred_out = y_pred_df["Predictions"]

plt.plot(y_pred_out, test['visit_count'],  color='green', label = 'Predictions')
#use ARMA model to feed in train's visit_count and use test date as example for forecast

from sklearn.metrics import mean_squared_error
from math import sqrt
rmse = sqrt(mean_squared_error(test['visit_count'], y_pred_out))
#evaluate performance

"""# 1.ANN"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

data = pd.read_csv('gdrive/My Drive/Colab_Notebooks/capstoneproject/capstonedata.csv', parse_dates=['visit_date'], index_col='visit_date')
doctor_id = data['doctor_id']
data['date'] = data.index.date

doctor_id = data['doctor_id']
visit_date = data.index.to_series()
m1 = doctor_id.ne(doctor_id.shift())
m2 = visit_date.dt.date.ne(visit_date.dt.date.shift())
data['count'] = data.groupby((m1 | m2).cumsum()).cumcount().add(1).values

out = data.groupby(['date', 'doctor_id'])['count'].max().reset_index()
#redo the counting with a separate dataset

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, SpatialDropout1D
from keras.utils import to_categorical

#seperating the date and count
date = out['date']
count = out['count']

labels = pd.get_dummies(date)

X_train, X_test, y_train, y_test = train_test_split(count, labels, test_size=0.2, random_state=42)
# Split the data into training and testing sets

# Define the LSTM model architecture
embedding_dim = 100
model = Sequential()
model.add(Embedding(100, embedding_dim, input_length=100))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(len(labels.columns), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the LSTM model
epochs = 100
batch_size = 640
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

# Evaluate the LSTM model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

# Get training and validation loss
import matplotlib.pyplot as plt

train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Get training and validation accuracy
train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

# Plot loss
plt.figure(figsize=(10, 5))
plt.plot(train_loss, label='Training Loss', color='blue')
plt.plot(val_loss, label='Validation Loss', color='red')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot accuracy
plt.figure(figsize=(10, 5))
plt.plot(train_acc, label='Training Accuracy', color='blue')
plt.plot(val_acc, label='Validation Accuracy', color='red')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
