# -*- coding: utf-8 -*-
"""Random Forest vs Gradient Boosting

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MGEaa2Ha863OlHO18fMK9K1EA3tGZsck
"""

import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot  as plt
import seaborn as sns
from sklearn.preprocessing import  MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df = pd.read_csv("C:\\Users\\devro\\OneDrive\\Desktop\\MLCOE task 4 app\\boston.csv")

df.head()

df.info()

df.isnull().sum()

df.columns

"""## **EDA**"""

#Visualziing the outliers (if any)
fig, axes = plt.subplots(7,1, figsize = (25,25))
sns.boxplot(x = 'CRIM', data = df, ax = axes[0])
sns.boxplot(x = 'ZN', data = df, ax = axes[1])
sns.boxplot(x = 'INDUS', data = df, ax = axes[2])
sns.boxplot(x = 'CHAS', data = df, ax = axes[3])
sns.boxplot(x = 'NOX', data = df, ax = axes[4])
sns.boxplot(x = 'RM', data = df, ax = axes[5])
sns.boxplot(x = 'AGE', data = df, ax = axes[6])

fig, axes = plt.subplots(6,1, figsize = (20,20))
sns.boxplot(x = 'DIS', data = df, ax = axes[0])
sns.boxplot(x = 'RAD', data = df, ax = axes[1])
sns.boxplot(x = 'TAX', data = df, ax = axes[2])
sns.boxplot(x = 'PTRATIO', data = df, ax = axes[3])
sns.boxplot(x = 'B', data = df, ax = axes[4])
sns.boxplot(x = 'LSTAT', data = df, ax = axes[5])

#sns.pairplot(df)

#Analysing correlation
corr = df.corr()
sns.heatmap(corr, annot = True)

threshold = 0.7
corr_features = set()
for i in range(len(corr.columns)):
    for j in range(i):
        if abs(corr.iloc[i, j]) > threshold:
            colname = corr.columns[i]
            corr_features.add(colname)

print("Highly correlated features:", corr_features)

#Didn't performed feature selection as the performance was significantly reduced....

"""## **Data Preprocessing**"""

#removing outliers

col = ['CRIM', 'ZN', 'INDUS',  'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX',
       'PTRATIO', 'B', 'LSTAT']

for col in col:
    q1 = np.percentile(df[col], 25)
    q3 = np.percentile(df[col], 75)
    iqr = q3 - q1
    u = q3 + 1.5*iqr
    l = q1 - 1.5*iqr
    df[col] = np.where(df[col]>u,u, np.where(df[col]<l,l, df[col]))

#visualizing if the outliers were removed or not...
'''
fig, axes = plt.subplots(13,1, figsize = (45,45))
sns.boxplot(x = 'CRIM', data = df, ax = axes[0])
sns.boxplot(x = 'ZN', data = df, ax = axes[1])
sns.boxplot(x = 'INDUS', data = df, ax = axes[2])
sns.boxplot(x = 'CHAS', data = df, ax = axes[3])
sns.boxplot(x = 'NOX', data = df, ax = axes[4])
sns.boxplot(x = 'RM', data = df, ax = axes[5])
sns.boxplot(x = 'AGE', data = df, ax = axes[6])
sns.boxplot(x = 'DIS', data = df, ax = axes[7])
sns.boxplot(x = 'RAD', data = df, ax = axes[8])
sns.boxplot(x = 'TAX', data = df, ax = axes[9])
sns.boxplot(x = 'PTRATIO', data = df, ax = axes[10])
sns.boxplot(x = 'B', data = df, ax = axes[11])
sns.boxplot(x = 'LSTAT', data = df, ax = axes[12])
'''

#Scaling the data
'''
scl = MinMaxScaler()
scl_df = scl.fit_transform(df)
scl_df = pd.DataFrame(scl_df, columns = df.columns)
'''

#seperating the input and target variables
x = df.drop(['MEDV'], axis = 1)
y = df['MEDV']

#performing train test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

#Random Forest
rf = RandomForestRegressor(random_state=42)

#Gradeient Boosting
gbr = GradientBoostingRegressor(random_state = 42, n_estimators = 300)

#Testing the model using appropriate metrics

reg_tot = [rf, gbr]

for a in reg_tot:
    a.fit(x_train, y_train)
    y_pred = a.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    cvs = np.mean(cross_val_score(a, x, y, cv = 5, scoring = 'r2'))

    print(f"Regressor: {a.__class__.__name__}")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"R2 score : {r2}")
    print(f"Cross Validation Score: {cvs}")
    print("\n")

"""Clearly we can see, Boosting provides better performance than Random Forest."""

#Deplying the better performing model
joblib.dump(gbr, open('Boosting.pkl', 'wb'))

