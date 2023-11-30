import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

data = pd.read_csv('ThoiTiet_dulieu.csv')
X = data[['Max Temperature','Min Temperature','Wind Speed','Relative Humidity']]
y = data['Conditions']

classifier = DecisionTreeClassifier()
classifier.fit(X, y)

joblib.dump(classifier, 'dtm.joblib')
