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

# Choose a dataset
car_index = int(input('Choose the index of the car: '))
mark_and_model = files[car_index - 1]
print('You\'ve chosen:', mark_and_model, '\n')
time.sleep(1)
file_ = mark_and_model + '.csv'

# Read chosen dataset
df = pd.read_csv(directory + '/' + file_, sep=',')
df = df.dropna()

# Create features (age, mileage) and label (price)
array_x = df[[df.columns[2], df.columns[3]]]
array_y = df[df.columns[1]]

# Separate data in train and test
Xtrain, Xtest, Ytrain, Ytest = train_test_split(array_x, array_y, test_size=0.3)

# Polynome degree choice
degree_ = int(input('Choose the polynome degree for approximation: '))
poly = PolynomialFeatures(degree=degree_)

# LinearRegression
model = linear_model.LinearRegression()
transform_Xtrain = poly.fit_transform(Xtrain)
model.fit(transform_Xtrain, Ytrain)

# Predicted values
transform_Xtest = poly.fit_transform(Xtest)
Ypred = model.predict(transform_Xtest)

# General information about the data set
print()
print('Information about the chosen car from the data set:')
print('Amount of instances:', len(array_x))
print('Range for age:', (round(min(array_x[array_x.columns[0]]), 3), round(max(array_x[array_x.columns[0]]), 3)))
print('Range for mileage, km:', (round(min(array_x[array_x.columns[1]]), 3), round(max(array_x[array_x.columns[1]]), 3)))
print('Range for price, rubles:', (round(min(array_y), 3), round(max(array_y), 3)))

# Coefficient of determination R2
print('Coefficient of determination =', r2_score(Ytest, Ypred))

# Waiting input data for car price estimation
while True:
    try:
        age = float(input('Enter age for prediction: '))
        mileage = float(input('Enter mileage for prediction: '))
    except:
        print('You haven\'t entered any number or you\'ve done it wrong', 'The processing has finished', sep='\n')
        break
    else:
        xx = np.array([age, mileage], float)
        xx = xx.reshape(1, -1)
        print('price =', str(int(model.predict(poly.fit_transform(xx))[0])) + ' P')
