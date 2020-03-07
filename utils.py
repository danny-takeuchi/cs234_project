import pandas as pd
import numpy as np

def sampleKRows(k=5528):
    data = pd.read_csv('data/warfarin.csv', header=0)
    data = data.dropna(axis=0, subset=['Therapeutic Dose of Warfarin'])
    return data.sample(k, replace = False)

def isnan(value):
  return value != value

def extractFeatures(data, i):
    heightMean = data['Height (cm)'].mean()
    weightMean = data['Weight (kg)'].mean()
    row = data.iloc[i]
    if isnan(row['Age']):
        age = 0
    else:
        age = float(row['Age'].split('-')[0]) / 10.0 if row['Age'] != '90+' else 90

    if isnan(row['Height (cm)']):
        height = heightMean
    else:
        height = float(row['Height (cm)'])

    if isnan(row['Weight (kg)']):
        weight = weightMean
    else:
        weight = float(row['Weight (kg)'])

    asian = row['Race'] == 'Asian'
    black = row['Race'] == 'Black or African American'
    white = row['Race'] == 'White'
    race_na = row['Race'] == 'Unknown'
    ethnicity_hispanic = row['Ethnicity'] == 'Hispanic or Latino'
    ethnicity_not_hispanic = row['Ethnicity'] == 'not Hispanic or Latino'
    if isnan(row['Medications']):
        enzyme = 0
        amiodarone = 0
    else:
        med_list = row['Medications'].split(';')
        enzyme = ('carbamazepine' in med_list or 'phenytoin' in med_list or 'rifampin' in med_list or 'rifampicin' in med_list)
        amiodarone = ('amiodarone' in med_list)


    CYP_12 = 0
    CYP_13 = 0
    CYP_22 = 0
    CYP_23 = 0
    CYP_33 = 0
    CYP_NA = 0
    if row["Cyp2C9 genotypes"] == "*1/*2":
        CYP_12 = 1
    elif row["Cyp2C9 genotypes"] == "*1/*3":
        CYP_13 = 1
    elif row["Cyp2C9 genotypes"] == "*2/*2":
        CYP_22 = 1
    elif row["Cyp2C9 genotypes"] == "*2/*3":
        CYP_23 = 1
    elif row["Cyp2C9 genotypes"] == "*3/*3":
        CYP_33 = 1
    elif row["Cyp2C9 genotypes"] == "NA":
        CYP_NA = 1

    VKO_GA = 0
    VKO_AA = 0
    VKO_NA = 0
    if row["VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T"] == "A/G":
        VKO_GA = 1
    elif row["VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T"] == "A/A":
        VKO_AA = 1
    elif row["VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T"] == "NA":
        VKO_NA = 1
    features = np.array([asian, black, white, race_na, ethnicity_hispanic, ethnicity_not_hispanic, age, height, weight, enzyme, amiodarone, CYP_12, CYP_13, CYP_22,CYP_23, CYP_33, CYP_NA, VKO_GA, VKO_AA, VKO_NA])

    return features
