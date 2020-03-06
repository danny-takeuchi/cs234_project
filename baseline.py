import pandas as pd
import math

# Our first baseline - which returns a fixed dosage to all patients
def baseline_one():
  data = pd.read_csv('data/warfarin.csv', header=0)
  data = data.dropna(axis=0, subset=['Therapeutic Dose of Warfarin']) # remove patients which have no known Warfarin dosage

  subset_correct = data.loc[(data['Therapeutic Dose of Warfarin'] >= 21) & (data['Therapeutic Dose of Warfarin'] <= 49)]

  fraction_correct = subset_correct.shape[0] / (data.shape[0] - 1)
  print('Baseline one')
  print("Fraction correct: ", fraction_correct)

baseline_one()

def assign_category(dose):
  patient_assigned = 'low' 
  if dose >= 21 and dose <= 49:
    patient_assigned = 'med'
  elif dose > 49:
    patient_assigned = 'high'
  return patient_assigned

def isnan(value):
  return value != value

# Our second baseline - Warfarin clinical dosing algorithm
def baseline_two():
  data = pd.read_csv('data/warfarin.csv', header=0)
  data = data.dropna(axis=0, subset=['Therapeutic Dose of Warfarin']) # remove patients which have no known Warfarin dosage
  heightMean = data['Height (cm)'].mean()
  weightMean = data['Weight (kg)'].mean()
  correct = 0

  for idx, row in data.iterrows():
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

    sqr_root_weekly_dose = 4.0376 - .2546*age + .0118*height + .0134*weight - .6752*asian \
              + .406*black + .0443*missing + 1.2799*enzyme - .5695*amiodarone
    patient_weekly_dose = sqr_root_weekly_dose**2
    patient_actual = row['Therapeutic Dose of Warfarin'] 

    if assign_category(patient_weekly_dose) == assign_category(patient_actual):
      correct += 1

  fraction_correct = correct / (data.shape[0] - 1)
  print('Baseline two')
  print('Fraction correct: ', fraction_correct)
   
baseline_two()
