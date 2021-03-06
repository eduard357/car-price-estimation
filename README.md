# Car price estimation

This project is intended for car price estimation using XGBoost algorithm. 

Project contents: 
1. Data sets with some car models.
2. Parser to get information from actual ads on the website www.auto.ru. 
3. Machine learning model based on XGBoost regression algorithm. 

## Installation

The following command will clone the repository to your local machine.

```bash
git clone https://github.com/eduard357/car-price-estimation.git
```

Use the package manager pip to install all required libraries.

```bash
pip install -r requirements.txt
```

## Usage

To run the prediction model, use following command from work directrory.

```bash
python ./main.py
```

## Example

At first one has to choose a data set with an available car from "Data_sets" directory. Some general info is displayed as well. 

![alt text](https://github.com/eduard357/car-price-estimation/blob/master/Images/general_info.PNG)

Then the MAE metric is calculated. After that the prediction part takes place where one has to select the features of a car.

![alt text](https://github.com/eduard357/car-price-estimation/blob/master/Images/prediction_part1.PNG)

Finally the estimated price is derived.

![alt text](https://github.com/eduard357/car-price-estimation/blob/master/Images/prediction_part2.PNG)
