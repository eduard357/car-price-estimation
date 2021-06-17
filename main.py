import os
import time
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split


# Set path to data sets directory
directory = './Data_sets'

# List all available data sets
files = os.listdir(directory)
for i in range(len(files)):
    files[i] = files[i].split('.csv')[0]

print('\n', 'List of available cars for analyze:')
files.sort()
for i in range(1, len(files) + 1):
    print(i, files[i - 1], sep='.')
print()

# LinearRegression - Ordinary least squares Linear Regression object
reg = linear_model.LinearRegression()

# Choose a dataset
car_index = int(input('Choose the index of the car: '))
mark_and_model = files[car_index - 1]
print('You\'ve chosen:', mark_and_model, '\n')
time.sleep(1)
file_ = mark_and_model + '.csv'

# Read in chosen dataset
df = pd.read_csv(directory + '/' + file_, sep=',')
df = df.dropna()

# Create independent arrays (age, mileage) and label array (price)
array_x1 = list(df[df.columns[2]])
array_x2 = list(df[df.columns[3]])
array_x = [[array_x1[i], array_x2[i]] for i in range(len(array_x1))]
array_y = list(df[df.columns[1]])

# Separate data in train and test
trainData_x, testData_x, trainData_y, testData_y = train_test_split(array_x, array_y, test_size=0.3)

# Training set X
x = np.array(trainData_x, float)

# Polynomial x train
degree_ = int(input('Choose the polynome degree for approximation: '))
poly = PolynomialFeatures(degree=degree_)
transform_x = poly.fit_transform(x)

# Training set Y
y = np.array(trainData_y, float)

# Train the model using the training sets
reg.fit(transform_x, y)

# Test set X
x_test = np.array(testData_x, float)

# Polynomial x test
transform_x_test = poly.fit_transform(x_test)

# Test set Y
y_test = np.array(testData_y, float)

# Predicted values
y_pred = reg.predict(transform_x_test)

# General information about the data set
print()
print('Information about the chosen car from the data set:')
print('Amount of instances:', len(array_x))
print('Range for age:', (round(min(array_x1), 3), round(max(array_x1), 3)))
print('Range for mileage:', (round(min(array_x2), 3), round(max(array_x2), 3)))
print('Range for price:', (round(min(array_y), 3), round(max(array_y), 3)))

# Coefficient of determination R2
print('Coefficient of determination =', r2_score(y_test, y_pred))

print('Where x1 - age;', 'x2 - mileage;', 'y - price', '\n')

while True:
    try:
        a = float(input('Enter x1 for prediction: '))
        b = float(input('Enter x2 for prediction: '))
    except:
        print('You haven\'t entered any number or you\'ve done it wrong', 'The processing has finished', sep='\n')
        break
    else:
        xx = np.array([a, b], float)
        xx = xx.reshape(1, -1)
        print('y =', str(int(reg.predict(poly.fit_transform(xx))[0])) + ' P')
