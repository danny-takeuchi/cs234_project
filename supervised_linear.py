import pandas as pd
import numpy as np
import math
import utils
from sklearn.linear_model import LogisticRegression

numToCategory = {0:'low', 1:'med', 2:'high'}
categoryToNum = {'low':0, 'med':1, 'high':2}

def to_one_hot(idx):
  vec = [0,0,0]
  vec[idx] = 1
  return vec

def assign_category(dose):
  patient_assigned = 'low' 
  if dose >= 21 and dose <= 49:
    patient_assigned = 'med'
  elif dose > 49:
    patient_assigned = 'high'
  return patient_assigned

def isnan(value):
  return value != value

def getFeatures(row, heightMean, weightMean):
    if isnan(row['Age']):
      age = 0
    else:
      age = float(row['Age'].split('-')[0])/10.0 if row['Age']!='90+' else 90

    if isnan(row['Height (cm)']):
      height = heightMean
    else:
      height = float(row['Height (cm)'])

    if isnan(row['Weight (kg)']):
      weight = 0
    else:
      weight = float(row['Weight (kg)'])

    asian = row['Race'] == 'Asian'
    black = row['Race'] == 'Black or African American'
    missing = row['Race'] == 'Unknown'
    if isnan(row['Medications']):
      enzyme = 0
      amiodarone = 0
    else:
      med_list = row['Medications'].split(';')
      enzyme = ('carbamazepine' in med_list or 'phenytoin' in med_list or 'rifampin' in med_list or 'rifampicin' in med_list)
      amiodarone = ('amiodarone' in med_list)

    features = [age, height, weight, asian, black, missing, enzyme, amiodarone]
    return features

# Online supervised learning.
# We are using 8 features, same as from baseline 2. 
def supervised():
  data = utils.sampleKRows()
  heightMean = data['Height (cm)'].mean()
  weightMean = data['Weight (kg)'].mean()
  correct = 0
  
  # Initializing the multi-layer perceptron.
  X_train = [[0] * 8, [0]*8]
  y_train = [0, 1]
  clf = LogisticRegression(random_state=0, max_iter=2000)
  clf.fit(np.array(X_train), np.array(y_train))

  counter = 0
  for idx, row in data.iterrows():
    print(counter)
    print('Accuracy: ', correct/counter if counter!= 0 else 0)
    counter += 1

    if counter == 5:
      X_train = X_train[2:]
      y_train = y_train[2:]

    features = getFeatures(row, heightMean, weightMean)
    predicted = clf.predict([np.array(features)])
    predicted_category = numToCategory[predicted[0]]

    patient_actual = row['Therapeutic Dose of Warfarin'] 
    actual_category = assign_category(patient_actual)

    # Refit the data.
    X_train.append(features)
    y_train.append(categoryToNum[actual_category])
    clf.fit(np.array(X_train), np.array(y_train))

    if predicted_category == assign_category(patient_actual):
      correct += 1

  fraction_correct = correct / (data.shape[0] - 1)
  print('Supervised Learning')
  print('Fraction correct: ', fraction_correct)
   
supervised()
