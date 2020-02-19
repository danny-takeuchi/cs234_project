import pandas as pd

# Our first baseline - which returns a fixed dosage to all patients
def baseline_one():
	data = pd.read_csv('data/warfarin.csv', header=0)
	data = data.dropna(axis=0, subset=['Therapeutic Dose of Warfarin']) # remove patients which have no known Warfarin dosage

	subset_correct = data.loc[(data['Therapeutic Dose of Warfarin'] >= 21) & (data['Therapeutic Dose of Warfarin'] <= 49)]

	fraction_correct = subset_correct.shape[0] / (data.shape[0] - 1)
	print("Fraction correct: ", fraction_correct)

baseline_one()

# Our second baseline - Warfarin clinical dosing algorithm
def baseline_two():
	data = pd.read_csv('data/warfarin.csv', header=0)
	data = data.dropna(axis=0, subset=['Therapeutic Dose of Warfarin']) # remove patients which have no known Warfarin dosage

	for idx, row in data.iterrows():
		age = float(row['Age'].split('-')[0])/10.0
		height = float(row['Height (cm)'])
		weight = float(row['Weight (kg)'])
		asian = row['Race'] == 'Asian'
		black = row['Race'] == 'Black or African American'
		missing = row['Race'] == 'Unknown'
		med_list = row['Medications'].split(';')
		enzyme = 0 if row['Medications'] == 'NA' else ('carbamazepine' in med_list or 'phenytoin' in med_list or 'rifampin' in med_list or 'rifampicin' in med_list)
		amiodarone = ('amiodarone' in med_list)

		sqr_root_weekly_dose = 4.0376 - .2546*age + .0118*height + .0134*weight - .6752*asian \
							+ .406*black + .0443*missing + 1.2799*enzyme - .5695*amiodarone
		patient_daily_dose = sqr_root_weekly_dose**2 / 7.0

		patient_assigned = 'low'
		if patient_daily_dose >= 21 and <= 49:
			patient_assigned = 'med'
		elif patient_daily_dose > 49:
			patient_assigned = 'high'


		patient_actual = row['Therapeutic Dose of Warfarin'] 


baseline_two()