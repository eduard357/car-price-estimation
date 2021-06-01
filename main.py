import os
import time
from functions import split_train_test
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

# Set path to data sets directory
directory = './Data_sets'

# List all available data sets
files = os.listdir(directory)
for i in range(len(files)):
    files[i] = files[i].split('.csv')[0]

print('\n', 'Список доступных машин для анализа данных:')
files.sort()
for i in range(1, len(files) + 1):
    print(i, files[i - 1], sep='.')
print()

# Initial data
testPercent = 0.5  # Part of train data regarding test data

# LinearRegression - Ordinary least squares Linear Regression class
reg = linear_model.LinearRegression()

# Choose a dataset
car_index = int(input('Выберите номер машины: '))
mark_and_model = files[car_index - 1]
print('Вы выбрали машину:', mark_and_model, '\n')
time.sleep(1)
file_ = mark_and_model + '.csv'

# Read in chosen dataset
df = pd.read_csv(directory + '/' + file_, sep=',')
df = df.dropna()

# Create independent arrays (age, mileage) and dependent array price
array_x1 = list(df[df.columns[2]])
array_x2 = list(df[df.columns[3]])
array_x = [[array_x1[i], array_x2[i]] for i in range(len(array_x1))]
array_y = list(df[df.columns[1]])

# Separate data in train and test
trainData_x, testData_x, trainData_y, testData_y = split_train_test(array_x, array_y, testPercent)

# Training set X
x = np.array(trainData_x, float)

# Polynomial x train
degree_ = int(input('Укажите степень полинома для аппроксимации: '))
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
print('Информация по выбранным массивам:')
print('Количество экземпляров:', len(array_x))
print('Диапазон для ' + '\'' + 'Год выпуска' + '\':', (round(min(array_x1), 3), round(max(array_x1), 3)))
print('Диапазон для ' + '\'' + 'Пробег' + '\':', (round(min(array_x2), 3), round(max(array_x2), 3)))
print('Диапазон для ' + '\'' + 'Стоимость' + '\':', (round(min(array_y), 3), round(max(array_y), 3)))

# Coefficient of determination R2
print('Коэффициент детерминации =', r2_score(y_test, y_pred))

print('Где x1 - Год выпуска;', 'x2 - Пробег;', 'y - Стоимость', '\n')

while True:
    try:
        a = float(input('Введите x1 для прогноза: '))
        b = float(input('Введите x2 для прогноза: '))
    except:
        print('Вы не ввели число или сделали это неправильно', 'Работа завершена', sep='\n')
        break
    else:
        xx = np.array([a, b], float)
        xx = xx.reshape(1, -1)
        print('y =', str(int(reg.predict(poly.fit_transform(xx))[0])) + ' P')
