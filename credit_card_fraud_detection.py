# -*- coding: utf-8 -*-
"""Credit Card Fraud Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wx6vFvIvqm_JZhtR-2nGzCVt2FkMv_Le
"""

# Import Kaggle to download the newest version of dataset
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print("Path to dataset files:", path)

# Importing OS for attaching the working files instead of temporary files
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Import all the necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Upload the dataset file and check the first five rows of the data to understand the dataset
data = pd.read_csv("/content/creditcard.csv")
data.head()

# display a concise summary of the dataset
data.info()

# Check the shape of the creditcard dataset
data.shape

# check for missing (null) values in the dataset
data.isnull().sum()

# Check if there are any duplicated values, if yes, remove them
data.duplicated()

# Check the summary of the statistical properties of the numerical columns in the dataset
data.describe()

# Check the distribution of the target variable 'Class'
class_distribution = data['Class'].value_counts()
class_distribution

# Classify the values as : 0 = "legit" and 1 = "fraud"
legit = data[data["Class"] == 0]
fraud = data[data["Class"] == 1]

# print the shape of the subsets
print(legit.shape)
print(fraud.shape)

"""The below code is a common technique used to balance the dataset by undersampling the majority class (non-fraudulent transactions) to match the number of instances in the minority class (fraudulent transactions)."""

# Sampling a subset of data
legit_sample = legit.sample(n=492)
print(legit_sample)

"""The purpose of the below code is to prepare a balanced dataset for training a machine learning model to predict fraud, where the class distribution is equal, addressing the class imbalance problem."""

# combine two datasets into a single DataFrame
data = pd.concat([legit_sample,fraud], axis=0)

data.shape

# Compute the mean of each numerical column in the data DataFrame, grouped by the "Class" column.
data.groupby("Class").mean()

# Separate the features (inputs) and the target variable (output) in the dataset
x = data.drop("Class", axis=1)
y = data["Class"]

# Split the data into training and testing sets (80% train, 20% test)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.20, random_state=42)

# Model Training
model = LogisticRegression()
model.fit(x_train, y_train)

# Model Evaluation
x_train_prediction = model.predict(x_train)
training_data_accuracy = accuracy_score(x_train_prediction, y_train)
print('Accuracy on Training data : ', training_data_accuracy)

x_test_prediction = model.predict(x_test)
test_data_accuracy = accuracy_score(x_test_prediction, y_test)
print('Accuracy score on Test Data : ', test_data_accuracy)

# Predict probabilities for the positive class
y_prob = model.predict_proba(x_test)[:, 1]

# Calculate precision-recall curve
from sklearn.metrics import accuracy_score, precision_recall_curve, auc
precision, recall, thresholds = precision_recall_curve(y_test, y_prob)

# Calculate AUPRC
auprc = auc(recall, precision)
print(f"AUPRC: {auprc}")

# Plot the precision-recall curve
import matplotlib.pyplot as plt
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()