# -*- coding: utf-8 -*-
"""Capstone Project ML Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uTGu_PcJWL_I5mCRfsf3ek5eNQtOGrhz

# ***DATA SCIENCE- CAPSTONE PROJECT BY ANKIT KUMAR VERMA***

# ***Data preparation***
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing the libraries

import numpy as np
# numpy is aliased as np
import pandas as pd
# pandas is aliased as pd
import matplotlib.pyplot as plt
# matplotlib.pyplot is aliased as plt
import seaborn as sns
# seaborn is aliased as sns
# %matplotlib inline

import warnings
warnings.filterwarnings('ignore')

# Loading the dataset
car = pd.read_csv('/content/CAR DETAILS.csv')
car

# showing the first 5 rows
car.head()

# showing the last 5 rows
car.tail()

"""**Basic Understanding of the Dataset.**"""

# showing dimension of the dataset
car.shape

"""Observation :

This Data have 4340 rows and 8 columns
"""

# showing columns
car.columns

# checking the datatypes
car.dtypes

# showing the information about the dataset
car.info()

"""**Observation :**

From the above output we can see -

There are 4340 rows and 8 columns.
There are 3 numerical columns i.e.. Year, Selling Price, Kms Driven.
There are 5 categorical columns i.e.. Car Name, Fuel, Seller Type, Transmission, Owner.
There are no null values in the dataset.
"""

# Extracting Numerical and Categorical columns
cat_cols = car.select_dtypes(include=['object'])
print(cat_cols.columns)
num_cols = car.select_dtypes(exclude=['O'])
print(num_cols.columns)

# showing descriptive statistical analysis
car.describe()

# showing the infomaton about categorical columns
car.describe(include='O')

"""# ***Data Preprocessing and Data Cleaning:***

***Checking for Outliers***
"""

# Plotting BoxPlot for checking for outliers
sns.boxplot(car,palette='viridis')

"""From this Plot we can see that Selling_price column has so many outliers.So, we will remove these outliers."""

# Removing Outliers

column = car['selling_price']
q1 = np.percentile(column, 25)
q3 = np.percentile(column, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
car['selling_price'] = column[(column > lower_bound) & (column < upper_bound)]

sns.boxplot(car,palette='rocket')

"""# ***Handling Duplicate Values***"""

# checking for duplicate values
car.duplicated().sum()

# Dropping the duplicate values
car.drop_duplicates(inplace=True)
car.shape

"""**Observation :**

---



After dropping duplicate values there are only 3574 rows are left in the dataset with 8 columns.

**Handling Missing Values:**
"""

# checking the null values
car.isnull().sum()

"""**Observation :**

As there are there are very less no. of null values in the dataset so we will drop these null values.
"""

# Dropping the null values
car.dropna(inplace=True)

# checking for null values
car['selling_price'].isnull().any()

"""#**Checking for Unique values**"""

# checking for unique values
car.nunique()

# checking for unique values of  name column
car['name'].unique()

# checking for unique values of  year column
car['year'].unique()

# checking for unique values of selling_price column
car['selling_price'].unique()

# checking for unique values of km_driven column
car['km_driven'].unique()

# checking for unique values of fuel column
car['fuel'].unique()

# checking for unique values of seller_type column
car['seller_type'].unique()

# checking for unique values of transmission column
car['transmission'].unique()

# checking for unique values of owner column
car['owner'].unique()

"""# **Feature Engineering**"""

# creating a brand column using the name of the car
car['brand'] = car['name'].apply(lambda x:x.split()[0])

# checking the unique values of the brand and showing the first 5 rows of brand column
print(car['brand'].nunique())
print(car['brand'].unique())
print(car['brand'].head())

# Saving this updated dataset for visualization by converting into new csv file
car.to_csv('car_updated.csv')

"""# **Visualizing Target Feature**

It is clear that the target feature is 'selling_price' which is the price of the car.
"""

car['selling_price']

# Showing Car Price Distribution plot
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
sns.distplot(car["selling_price"],color="red",kde=True)
plt.title("Car Price Distribution",fontweight="black",pad=20,fontsize=15)

# Showing Car Price Spread plot
plt.subplot(1,2,2)
sns.boxplot(y=car["selling_price"],palette="Set2")
plt.title("Car Price Spread",fontweight="black",fontsize=15)
plt.tight_layout()
plt.show()

# Graphical Analysis of Car Price
car["selling_price"].agg(["min","mean","median","max","std","skew"]).to_frame().T

"""Insights :

We can clearly observe that our Car Price Feature is Slightly Rightly Skewed Distribution.

We can clearly observe that there is a significant difference between mean & median value.

We can also make an insight that most of the car's price is below 3,25,000.

The Majority of the Car falls between 20,000 to 11,65,000.

# ***Conversion of Categorical Features to Numerical Features.***

For this Conversion we will use Label Encoding for converting all the Categorical Features to numerical Features.

# **Label Encoding**
"""

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
columns = ['fuel','seller_type','transmission','owner']
for col in columns:
  car[col] = le.fit_transform(car[col])

car.head()

"""# ***Selecting independent and the dependent features from the dataset***"""

x = car.drop(['selling_price','name','brand'],axis=1) # x denotes independent features
y = car['selling_price']                              # y denotes dependent variable
print(type(x))
print(type(y))
print(x.shape)
print(y.shape)

"""# ***Train Test Split***

Dividing the data into training and testing data
"""

from sklearn.model_selection import train_test_split

print(3388*0.25)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=1)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

"""# **Creating functions to evaluate the Regression Evaluation Metrics, Model Score.**"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def reg_eval_metrics(ytest, ypred):
    mae = mean_absolute_error(ytest, ypred)
    mse = mean_squared_error(ytest, ypred)
    rmse = np.sqrt(mean_squared_error(ytest, ypred))
    print("MAE:", mae)
    print("MSE:", mse)
    print("RMSE:", rmse)

def mscore(model):
    print('Training Score',model.score(x_train,y_train)) # Trainng R2 score
    print('Testing Score',model.score(x_test,y_test))    # Testing R2 Score

"""# ***Importing the ML Regression libraries***"""

from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor
from xgboost import XGBRegressor

"""# ***1. Linear Regression***"""

# Building the Linear Regression Model
lin_reg = LinearRegression()
lin_reg.fit(x_train,y_train)

# Computing Training and Testing score
mscore(lin_reg)

# Generating Prediction
ypred_lr = lin_reg.predict(x_test)
print(ypred_lr)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_lr)

# Evaluating Model : R2 score
r2_lr = r2_score(y_test,ypred_lr)*100
r2_lr

"""# ***2. Ridge Regression***"""

# Building the Ridge Regression Model
ridge = Ridge(alpha=10)
ridge.fit(x_train,y_train)

# Computing Training and Testing score
mscore(ridge)

# Generating Prediction
ypred_ridge = ridge.predict(x_test)
print(ypred_ridge)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_ridge)

# Evaluating Model : R2 score
r2_ridge = r2_score(y_test,ypred_ridge)*100
r2_ridge

"""# ***3. Lasso Regression***"""

# Building the Lasso Regression Model
lasso = Lasso(alpha=0.1)
lasso.fit(x_train,y_train)

# Computing Training and Testing score
mscore(lasso)

# Generating Prediction
ypred_lasso = lasso.predict(x_test)
print(ypred_lasso)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_lasso)

# Evaluating Model : R2 score
r2_lasso = r2_score(y_test,ypred_lasso)*100
r2_lasso

"""# ***4. Random Forest Regression***"""

# Building the RandomForest Regression Model
rf = RandomForestRegressor(n_estimators=100)
rf.fit(x_train,y_train)

# Computing Training and Testing score
mscore(rf)

# Generating Prediction
ypred_rf = rf.predict(x_test)
print(ypred_rf)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_rf)

# Evaluating Model : R2 score
r2_rf = r2_score(y_test,ypred_rf)*100
r2_rf

"""# ***5. K-Nearest Neighbors Regression***"""

# Building the KNeighbors Regression Model
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(x_train,y_train)

# Computing Training and Testing score
mscore(knn)

# Generating Prediction
ypred_knn = knn.predict(x_test)
print(ypred_knn)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_knn)

# Evaluating Model : R2 score
r2_knn = r2_score(y_test,ypred_knn)*100
r2_knn

"""# ***6. Decision Tree Regression***"""

# Building the DecisionTree Regression Model
dt = DecisionTreeRegressor(criterion='absolute_error')
dt.fit(x_train,y_train)

# Computing Training and Testing score
mscore(dt)

# Generating Prediction
ypred_dt = dt.predict(x_test)
print(ypred_dt)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_dt)

# Evaluating Model : R2 score
r2_dt = r2_score(y_test,ypred_dt)*100
r2_dt

"""# ***7. Gradient Boosting Regression***"""

# Building the DecisionTree Regression Model
gbr = GradientBoostingRegressor()
gbr.fit(x_train,y_train)

# Computing Training and Testing score
mscore(gbr)

# Generating Prediction
ypred_gbr = gbr.predict(x_test)
print(ypred_gbr)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_gbr)

# Evaluating Model : R2 score
r2_gbr = r2_score(y_test,ypred_gbr)*100
r2_gbr

"""# ***8. AdaBoost Regression***"""

# Building the AdaBoost Regression Model
adab = AdaBoostRegressor()
adab.fit(x_train,y_train)

# Computing Training and Testing score
mscore(adab)

# Generating Prediction
ypred_adab = adab.predict(x_test)
print(ypred_adab)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_adab)

# Evaluating Model : R2 score
r2_adab = r2_score(y_test,ypred_adab)*100
r2_adab

"""# ***9. XGBoost Regression***"""

# Building the XGBoost Regression Model
xgb = XGBRegressor()
xgb.fit(x_train,y_train)

# Computing Training and Testing score
mscore(xgb)

# Generating Prediction
ypred_xgb = xgb.predict(x_test)
print(ypred_xgb)

# Evaluating the model : mean_absolute_error, mean_squared_error, root_mean_squared_error
reg_eval_metrics(y_test,ypred_xgb)

# Evaluating Model : R2 score
r2_xgb = r2_score(y_test,ypred_xgb)*100
r2_xgb

"""# ***Comparing Different Regression Models***

Creating a dataframe showing R2_score of each model
"""

# Creating a dataframe showing R2_score of each model
models = pd.DataFrame({
    'Model': ['Linear Regression','Ridge Regression','Lasso Regression','RandomForest Regressor','KNeighbors Regressor','DecisionTree Regressor','GradientBoosting Regressor','AdaBoost Regressor','XGBoost Regressor'],
    'Score': [r2_lr,r2_ridge,r2_lasso,r2_rf,r2_knn,r2_dt,r2_gbr,r2_adab,r2_xgb]})

models.sort_values(by='Score',ascending=False)

"""# ***Plotting R2_score of each model on a bar graph***"""

# plotting R2_score of each model on a bar graph
sns.barplot(x=models['Model'],y=models['Score'],palette='ocean')
plt.xticks(rotation=90)
plt.show()

"""> Hence, we can conclude that GradientBoosting Regressor is the best model

# ***Generating Predictions on Test data using GradientBoosting Regressor***
"""

print(x_train.shape)
print(x_test.shape)
print(x.shape)
print(y.shape)

"""# ***Final model (GradientBoosting Regressor) based on Evaluation from models dataframe***"""

best_model = GradientBoostingRegressor(n_estimators=80)
best_model.fit(x,y)

"""# ***Generating Prediction on test data***"""

ypred = best_model.predict(x_test)
print(ypred)

"""# ***Save the Model***"""

import pickle
loaded_model = pickle.load(open('model.pkl', 'rb'))  # rb = read binary
loaded_model.predict(x_test)

"""# ***Load the Model***"""

loaded_model = pickle.load(open('model.pkl', 'rb'))  # rb = read binary
loaded_model.predict(x_test)

"""# ***Creating a Random Dataset and Applying the saved model to predict the target column for the new dataframe.***

Taking sample of Random 20 Points from the CAR_DETAILS Dataset
"""

random = car.sample(20)
random_df = random.drop('selling_price',axis=1)
random_df

# Conversion of random_df to csv file.
random_df.to_csv('data_sample')

# Loading car_sample dataset
sample_data = pd.read_csv('/content/data_sample')
sample_data

# showing first 5 rows
sample_data.head()

# showing last 5 rows
sample_data.tail()

# showing dimension of the dataset
sample_data.shape

# showing columns
sample_data.columns

# Dropping unnecessary columns
sample_data = sample_data.drop(['Unnamed: 0','name','brand'],axis=1)
sample_data.columns

# making prediction on sample data
predicted_selling_price = loaded_model.predict(sample_data)
print(predicted_selling_price)

#  Compare the actual data and predicted data
new_data_with_predictions = random.copy()
new_data_with_predictions["predicted_selling Price"] = predicted_selling_price

# Print the actual and predicted data
print("Actual Selling Price and Predicted Selling Price for 20 cars brands with their name are :- ")
new_data_with_predictions[["name","brand","selling_price", "predicted_selling Price"]]