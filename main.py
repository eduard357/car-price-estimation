import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor

# Set path to directory with data sets
directory = './Data_sets'

# Get available data sets
files = os.listdir(directory)
for i, file in enumerate(files):
    files[i] = file.split('.csv')[0]

print('#########################################################################################')
print('                     Choice of the car whose price is to be predicted                    ')
print('#########################################################################################')

# List all available data sets
print('List of available cars for analyze:')
for i, file in enumerate(files):
    print(i + 1, file, sep='.')

# Choose a data set
car_index = int(input('\nChoose the index of the car: '))
brand_and_model = files[car_index - 1]
print(f'You\'ve chosen: {brand_and_model} \n')

# Create file path to the dataset
file_name = brand_and_model + '.csv'
file_path = directory + '/' + file_name

# Read chosen data set
data_set = pd.read_csv(file_path, encoding='cp1251')

print('#########################################################################################')
print('                            General info about the data set                              ')
print('#########################################################################################')

# Display number of rows in the data set
print('Cars number in the data set:', data_set.shape[0])

# Remove rows with missing target
data_set.dropna(axis=0, subset=['Цена, руб.'], inplace=True)

# Display number of rows in the data set after removing ones with missing target
print('Cars number in the data set after removing ones with missing target:', data_set.shape[0])

# Delete duplicate rows
data_set.drop_duplicates(inplace=True)
print('Final number of rows in the data set after deleting duplicates:', data_set.shape[0])

# Convert some columns from float to integer
for col in ['Цена, руб.', 'Год выпуска', 'Пробег, км.', 'Мощность двигателя, л/с', 'Налог, руб.']:
    data_set[col] = data_set[col].astype('int64')

# Display the range for price
print('Price ∈ [{:,}₽; {:,}₽]\n'.format(data_set['Цена, руб.'].min(), data_set['Цена, руб.'].max()))

# Drop uninformative columns
uninformative_columns = ['Название', 'Цвет', 'Налог, руб.', 'Положение руля', 'ПТС', 'Время владения, г.', 'Таможня',
                         'URL адрес']
data_set.drop(columns=uninformative_columns, inplace=True)

# Separate target from predictors
x = data_set.copy()
y = x.pop('Цена, руб.')

# Check whether there are any missing values in the predictors
assert not x.isnull().sum().any(), 'There are some missing values yet. The model cannot be fitted'

# Categorical columns
object_cols = [col for col in x.columns if x[col].dtypes == 'object']

# Encode categorical columns with integers
x_encoded = x.copy()
label_encoder = LabelEncoder()
for col in object_cols:
    x_encoded[col] = label_encoder.fit_transform(x[col])

# Define model
model = XGBRegressor(n_estimators=1000, learning_rate=0.0055, random_state=100)

print('#########################################################################################')
print('                                     Model accuracy                                      ')
print('#########################################################################################')

# Cross-validation
print('Cross-validation is being performed')
scores = -1 * cross_val_score(model, x_encoded, y, cv=5, scoring='neg_mean_absolute_error')

# Model accuracy
print('Mean Absolute Error = {:,}₽\n'.format(int(scores.mean())))

# Fit model
model.fit(x_encoded, y)

print('#########################################################################################')
print('                                    Prediction part                                      ')
print('#########################################################################################')

# Waiting input data for prediction
try:
    print('Values for year of manufacture ∈ [{}; {}]'.format(data_set['Год выпуска'].min(),
                                                             data_set['Год выпуска'].max()))
    year = int(input('Enter year for prediction: '))
    print('\nValues for mileage, (km) ∈ [{}; {}]'.format(data_set['Пробег, км.'].min(), data_set['Пробег, км.'].max()))
    mileage = int(input('Enter mileage for prediction: '))
    print('\nValues for body type ∈ {}'.format(list(data_set['Тип кузова'].unique())))
    body_type = input('Enter body type for prediction: ')
    print('\nValues for engine volume, (l) ∈ {}'.format(list(np.sort(data_set['Объем двигателя, л.'].unique()))))
    engine_volume = float(input('Enter engine volume for prediction: '))
    print('\nValues for engine power, (hp)" ∈ {}'.format(list(np.sort(data_set['Мощность двигателя, л/с'].unique()))))
    engine_power = int(input('Enter engine power for prediction: '))
    print('\nValues for engine type ∈ {}'.format(list(data_set['Тип двигателя'].unique())))
    engine_type = input('Enter engine type for prediction: ')
    print('\nValues for transmission type ∈ {}'.format(list(data_set['Тип коробки передач'].unique())))
    transmission = input('Enter transmission for prediction: ')
    print('\nValues for drive type ∈ {}'.format(list(data_set['Привод'].unique())))
    drive_type = input('Enter drive type for prediction: ')
    print('\nValues for state ∈ {}'.format(list(data_set['Состояние'].unique())))
    state = input('Enter state for prediction: ')
    print('\nValues for owners number ∈ {}'.format(list(np.sort(data_set['Число владельцев'].unique()))))
    owners_number = input('Enter number of owners for prediction: ')
except:
    print('\nYou haven\'t entered any value or you\'ve done it wrong.',
          'The processing has finished', sep='\n')
else:
    test_X = pd.DataFrame({'Год выпуска': [year], 'Пробег, км.': [mileage], 'Тип кузова': [body_type],
                           'Объем двигателя, л.': [engine_volume], 'Мощность двигателя, л/с': [engine_power],
                           'Тип двигателя': [engine_type], 'Тип коробки передач': [transmission],
                           'Привод': [drive_type], 'Состояние': [state],
                           'Число владельцев': [owners_number]})

    # Encode categorical columns with integers for test data
    test_encoded = test_X.copy()
    for col in object_cols:
        label_encoder.fit(x[col])
        test_encoded[col] = label_encoder.transform(test_X[col])

    # Prediction
    print('\nprice = {:,}₽'.format(int(model.predict(test_encoded))))
