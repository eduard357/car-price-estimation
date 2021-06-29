from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import os

# Set path to data sets directory
directory = './Data_sets'

# Get data sets name
files = os.listdir(directory)
for i in range(len(files)):
    files[i] = files[i].split('.csv')[0]

# List all available data sets
print('\n', 'List of available cars for analyze:', sep='')
files.sort()
for i in range(1, len(files) + 1):
    print(i, files[i - 1], sep='.')
print()

# Choose a dataset
car_index = int(input('Choose the index of the car: '))
mark_and_model = files[car_index - 1]
print('You\'ve chosen:', mark_and_model, '\n')
file_name = mark_and_model + '.csv'
file_path = directory + '/' + file_name

# Read chosen dataset
df = pd.read_csv(file_path, encoding='cp1251')

# Display number of rows in the dataset
print('Cars number in the dataset: = ', df.shape[0])

# Remove rows with missing target
df.dropna(axis=0, subset=['Цена, руб.'], inplace=True)

# Display number of rows in the dataset after removing rows with missing target
print('Cars number in the dataset after removing ones with missing target: = ', df.shape[0])

# Delete duplicate rows
df.drop_duplicates(inplace=True)
print('Current number of rows in the dataset after deleting duplicates: {}'.format(df.shape[0]))

# Target data
target_column = 'Цена, руб.'
y = df[target_column]

# Separate target from predictors
X = df.drop(axis=1, columns=target_column)

# Drop uninformative columns
uninformative_columns = ['Название', 'Таможня', 'URL адрес', 'ПТС', 'Руль', 'Налог, руб.', 'Цвет']
X.drop(axis=1, columns=uninformative_columns, inplace=True)

# Check whether there are no missing values in the predictors
if X.isnull().sum().any():
    raise ValueError('There are some missing values yet. The model cannot be fitted')
else:
    print('There are no missing values')

# Categorical columns
object_cols = [col for col in X.columns if X[col].dtypes == 'object']

# Label encoding. Make copy to avoid changing original data
label_X = X.copy()

# Apply label encoder to each column with categorical data
label_encoder = LabelEncoder()
for col in object_cols:
    label_X[col] = label_encoder.fit_transform(X[col])

# Define model
model = XGBRegressor(n_estimators=1000, learning_rate=0.0055)

# Cross-validation
scores = -1 * cross_val_score(model, label_X, y,
                              cv=5,
                              scoring='neg_mean_absolute_error')

print('Average Mean Absolute Error = {}₽'.format(int(scores.mean())))

# Fit model
model.fit(label_X, y)

# Display the range for price
print('Price ∈ [{:,}₽; {:,}₽]'.format(int(df['Цена, руб.'].min()), int(df['Цена, руб.'].max())))

# Waiting input data for prediction
while True:
    try:
        print('Values for "age" ∈ [{}; {}]'.format(df['Год выпуска'].min(), df['Год выпуска'].max()))
        age = int(input('Enter age for prediction: '))
        print('Values for "mileage" ∈ [{}; {}]'.format(df['Пробег, км.'].min(), df['Пробег, км.'].max()))
        mileage = int(input('Enter mileage for prediction: '))
        print('Values for "body_type" ∈ {}'.format(df['Кузов'].unique()))
        body_type = input('Enter body_type for prediction: ')
        print('Values for "engine_volume" ∈ {}'.format(np.sort(df['Объем двигателя, л.'].unique())))
        engine_volume = float(input('Enter engine_volume for prediction: '))
        print('Values for "engine_power" ∈ {}'.format(np.sort(df['Мощность двигателя, л/с'].unique())))
        engine_power = int(input('Enter engine_power for prediction: '))
        print('Values for "engine_type" ∈ {}'.format(df['Двигатель'].unique()))
        engine_type = input('Enter engine_type for prediction: ')
        print('Values for "transmission" ∈ {}'.format(df['Коробка передач'].unique()))
        transmission = input('Enter transmission for prediction: ')
        print('Values for "wheel_drive" ∈ {}'.format(df['Привод'].unique()))
        wheel_drive = input('Enter wheel_drive for prediction: ')
        print('Values for "state" ∈ {}'.format(df['Состояние'].unique()))
        state = input('Enter state for prediction: ')
        print('Values for "owners_counter" ∈ {}'.format(np.sort(df['Число владельцев'].unique())))
        owners_counter = input('Enter owners_counter for prediction: ')
    except:
        print('You haven\'t entered any number or you\'ve done it wrong', 'The processing has finished', sep='\n')
        break
    else:
        test_X = pd.DataFrame({'Год выпуска': [age], 'Пробег, км.': [mileage], 'Кузов': [body_type],
                               'Объем двигателя, л.': [engine_volume], 'Мощность двигателя, л/с': [engine_power],
                               'Двигатель': [engine_type], 'Коробка передач': [transmission],
                               'Привод': [wheel_drive], 'Состояние': [state],
                               'Число владельцев': [owners_counter]})
        # Label encoding for test data
        label_test_X = test_X.copy()
        for col in object_cols:
            label_encoder.fit(X[col])
            label_test_X[col] = label_encoder.transform(test_X[col])
        # Prediction
        print('price =', str(int(model.predict(label_test_X))) + '₽')
