import os
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor

# Set path to data sets' directory
directory = './Data_sets'

# Get data sets' name
files = os.listdir(directory)
for i in range(len(files)):
    files[i] = files[i].split('.csv')[0]

print('#############################################################')
print('#          Car choice whose price should be predicted        ')
print('#############################################################')

# List all available data sets
print('List of available cars for analyze:', sep='')
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

print('#############################################################')
print('#             General info about the data set                ')
print('#############################################################')

# Display number of rows in the data set
print('Cars number in the dataset: = ', df.shape[0])

# Remove rows with missing target
df.dropna(axis=0, subset=['Цена, руб.'], inplace=True)

# Display number of rows in the dataset after removing rows with missing target
print('Cars number in the dataset after removing ones with missing target: = ', df.shape[0])

# Delete duplicate rows
df.drop_duplicates(inplace=True)
print('Current number of rows in the dataset after deleting duplicates: {}'.format(df.shape[0]))

# Display the range for price
print('Price ∈ [{:,}₽; {:,}₽]\n'.format(int(df['Цена, руб.'].min()), int(df['Цена, руб.'].max())))

# Drop uninformative columns
uninformative_columns = ['Название', 'Таможня', 'URL адрес', 'ПТС', 'Руль', 'Налог, руб.', 'Цвет']
df.drop(columns=uninformative_columns, inplace=True)

# Separate target from predictors
X = df.copy()
y = X.pop('Цена, руб.')

# Check whether there are no missing values in the predictors
assert ~X.isnull().sum().any(), 'There are some missing values yet. The model cannot be fitted'

# Categorical columns
object_cols = [col for col in X.columns if X[col].dtypes == 'object']


# Object to category type conversion
def obj2categ(df):
    for col in object_cols:
        df[col] = df[col].astype('category')
    return df


# Categorical columns encoding
def label_encode(df):
    label_df = df.copy()
    for colname in label_df.select_dtypes(["category"]):
        label_df[colname] = label_df[colname].cat.codes
    return label_df


# Convert 'object' type to 'category' for train data
X = obj2categ(X)

# Encode categorical columns of train dataset
label_X = label_encode(X)

# Define model
model = XGBRegressor(n_estimators=1000, learning_rate=0.0055, random_state=100)

# Cross-validation
scores = -1 * cross_val_score(model, label_X, y,
                              cv=5,
                              scoring='neg_mean_absolute_error')

print('#############################################################')
print('#                    Model accuracy                          ')
print('#############################################################')

print('Average Mean Absolute Error = {}₽\n'.format(int(scores.mean())))

# Fit model
model.fit(label_X, y)

# Waiting input data for prediction
while True:
    print('#############################################################')
    print('#                    Prediction part                         ')
    print('#############################################################')
    try:
        print('Values for "age" ∈ [{}; {}]'.format(df['Год выпуска'].min(), df['Год выпуска'].max()))
        age = int(input('Enter age for prediction: '))
        print('\nValues for "mileage" ∈ [{}; {}]'.format(df['Пробег, км.'].min(), df['Пробег, км.'].max()))
        mileage = int(input('Enter mileage for prediction: '))
        print('\nValues for "body_type" ∈ {}'.format(df['Кузов'].unique()))
        body_type = input('Enter body_type for prediction: ')
        print('\nValues for "engine_volume" ∈ {}'.format(np.sort(df['Объем двигателя, л.'].unique())))
        engine_volume = float(input('Enter engine_volume for prediction: '))
        print('\nValues for "engine_power" ∈ {}'.format(np.sort(df['Мощность двигателя, л/с'].unique())))
        engine_power = int(input('Enter engine_power for prediction: '))
        print('\nValues for "engine_type" ∈ {}'.format(df['Двигатель'].unique()))
        engine_type = input('Enter engine_type for prediction: ')
        print('\nValues for "transmission" ∈ {}'.format(df['Коробка передач'].unique()))
        transmission = input('Enter transmission for prediction: ')
        print('\nValues for "wheel_drive" ∈ {}'.format(df['Привод'].unique()))
        wheel_drive = input('Enter wheel_drive for prediction: ')
        print('\nValues for "state" ∈ {}'.format(df['Состояние'].unique()))
        state = input('Enter state for prediction: ')
        print('\nValues for "owners_counter" ∈ {}'.format(np.sort(df['Число владельцев'].unique())))
        owners_counter = input('Enter owners_counter for prediction: ')
    except:
        print('\nYou haven\'t entered any number or you\'ve done it wrong.',
              'The processing has finished', sep='\n')
        break
    else:
        test_X = pd.DataFrame({'Год выпуска': [age], 'Пробег, км.': [mileage], 'Кузов': [body_type],
                               'Объем двигателя, л.': [engine_volume], 'Мощность двигателя, л/с': [engine_power],
                               'Двигатель': [engine_type], 'Коробка передач': [transmission],
                               'Привод': [wheel_drive], 'Состояние': [state],
                               'Число владельцев': [owners_counter]})

        # Alter 'object' type to 'category' for test data
        test_X = obj2categ(test_X)
        # Encode categorical columns of test data
        label_test = label_encode(test_X)
        # Prediction
        print('\nprice =', str(int(model.predict(label_test))) + '₽')
