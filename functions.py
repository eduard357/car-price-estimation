''' Separate N data elements in two parts:
train data with N*testPercent elements
test data with N*(1.0 - testPercent) elements '''
def split_train_test(array_x, array_y, testPercent):
    trainData_x = array_x[:round(len(array_x) * testPercent)]
    testData_x = array_x[round(len(array_x) * testPercent):]
    trainData_y = array_y[:round(len(array_y) * testPercent)]
    testData_y = array_y[round(len(array_y) * testPercent):]
    return trainData_x, testData_x, trainData_y, testData_y

