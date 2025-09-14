import numpy as np
import pandas as pd

file_path = r"C:\Aditya\Computer Science\Machine Learning\Datasets\BreastCancer\Breast-cancer.csv"
dataset = pd.read_csv(file_path)
dataset['diagnosis'] = dataset['diagnosis'].replace({'M': 1, 'B': 0})

dataset = dataset.drop(columns=["Unnamed: 32"])

#Handling missing data
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')
imputed_data = imputer.fit_transform(dataset.iloc[:, 2:])  # Exclude 'id' and 'diagnosis' columns
dataset.iloc[:, 2:] = imputed_data  


# splitting the dataset into matrix of features and independent variable vector
x = dataset.drop(columns=["id", "diagnosis"])
y = dataset[["diagnosis"]]


#splitting the data into training set and test set

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

#Feature Scaling

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
# training the model
from sklearn.linear_model import LogisticRegression
logistic_classifier = LogisticRegression(random_state=0)
logistic_classifier.fit(x_train, y_train)
y_pred = logistic_classifier.predict(x_test)
y_pred = y_pred.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)
result = np.concatenate((y_pred, y_test), axis=1)

print(result)

#Predicting a single value
print(logistic_classifier.predict(sc.transform([[18.00, 12.38, 122.80,1001.01, 0.08471, 0.27760, 0.30010, 0.14820, 0.2419,	0.07871, 1.0950,	0.9053,	8.589,	153.40,	0.006399,	0.04904,	0.05373,	0.01587,	0.03003,	0.006193,	25.380,	17.33,	184.60,	2019.0,	0.16220,	0.66560,	0.7119,	0.2654,	0.4601,	0.11890]])))



#Metrics
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))


