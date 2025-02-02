# -*- coding: utf-8 -*-
"""Identify_bestsource_of_Recruitment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13AaD75-oWqHNPMFPKtdGogypy8ZUVGYs
"""

Simport pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/content/Recruitment_Data_updated.csv')

df.shape

df.head()

df2=df.drop_duplicates()

df2.shape

df2.isna().sum()

df2.dropna(inplace=True)

print('data has {} rows and {} columns'.format(df2.shape[0], df2.shape[1]))

df2.head()

df2.nunique()

df2.info()

df_ohe=pd.get_dummies(df2,columns=['recruiting_source'])

df_ohe.head()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_scaler=pd.DataFrame(scaler.fit_transform(df_ohe),columns=df_ohe.columns)

df_scaler

df_scaler['attrition'] = df_scaler['attrition'].apply(lambda x: 1 if x >= 0 else 0)

df_scaler

"""# Train Test Split"""

from sklearn.model_selection import train_test_split
# Define features and target variable
X = df_scaler.drop('attrition', axis=1)
y = df_scaler['attrition']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)

#random forest

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score,confusion_matrix

# Initialize and train the classifier
clf = RandomForestClassifier(random_state=7,n_estimators=50)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred)*100)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

import seaborn as sns

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

#logistic regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

lr=LogisticRegression(class_weight='balanced',solver='saga')
lr.fit(X_train,y_train)

y_pred1=lr.predict(X_test)

accuracy = accuracy_score(y_test, y_pred1)
print("Accuracy:", accuracy*100)
print(classification_report(y_test, y_pred1))
print(confusion_matrix(y_test, y_pred1))

import seaborn as sns

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred1)
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

#svm
from sklearn.svm import SVC

model=SVC(class_weight='balanced',random_state=7,kernel='linear')
model.fit(X_train,y_train)

y_pred_svc=model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred_svc)
print("Accuracy:", accuracy*100)
print(classification_report(y_test, y_pred_svc))
print(confusion_matrix(y_test, y_pred_svc))

import seaborn as sns

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred_svc)
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""# Visualization"""

df_groupby_sales = df2.groupby('recruiting_source')[['sales_quota_pct']].mean().sort_values(by='sales_quota_pct', ascending=False)
df_groupby_sales

df_groupby_sales.plot(kind='bar')
plt.ylabel('Sales Quota')
plt.xlabel('Recruiting Source')
plt.title('Sales Quota by Recruiting Source')
plt.show()

df_groupby_sales.plot(kind='pie',subplots=True, autopct='%1.1f%%',legend= False)
plt.ylabel('Sales Quota')
plt.xlabel('Recruiting Source')
plt.title('Sales Quota by Recruiting Source')
plt.show()

df_groupby_performance_rating = df2.groupby('recruiting_source')[['performance_rating']].mean().sort_values(by='performance_rating', ascending=False)
df_groupby_performance_rating

df_groupby_performance_rating.plot(kind='bar')
plt.ylabel('Performance Rating')
plt.xlabel('Recruiting Source')
plt.title('Performance Rating by Recruiting Source')
plt.show()

df_groupby_performance_rating.plot(kind='pie', subplots=True,autopct='%1.1f%%',legend= False)
plt.ylabel('Performance Rating')
plt.xlabel('Recruiting Source')
plt.title('Performance Rating by Recruiting Source')

df_groupby_attrition = df2.groupby('recruiting_source')[['attrition']].mean().sort_values(by='attrition', ascending=False)
df_groupby_attrition

df_groupby_attrition.plot(kind='bar')
plt.ylabel('Attrition')
plt.xlabel('Recruiting Source')
plt.title('Attrition by Recruiting Source')
plt.show()

df_groupby_attrition.plot(kind='pie',subplots=True, autopct='%1.1f%%',legend= False)
plt.ylabel('Attrition')
plt.xlabel('Recruiting Source')
plt.title('Attrition by Recruiting Source')

"""# Visulaization using GGPLOT"""

from plotnine.data import economics
from plotnine import ggplot, aes, geom_line,geom_bar,geom_point,geom_histogram,geom_boxplot,geom_col,ggtitle

(
    ggplot(df_groupby_sales.reset_index())
    + aes(x='recruiting_source', y='sales_quota_pct', fill='recruiting_source')
    + geom_col()
    + ggtitle('Sales Quota by Recruiting Source')

)

(
    ggplot(df_groupby_attrition.reset_index())
    + aes(x='recruiting_source', y='attrition', fill='recruiting_source')
    + geom_col()
    + ggtitle('Attrition by Recruiting Source')
)

df2.to_csv('Recruitment_Data_cleaned_updated.csv')
!ls



