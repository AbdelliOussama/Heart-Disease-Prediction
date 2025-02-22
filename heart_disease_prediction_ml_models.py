# -*- coding: utf-8 -*-
"""heart-disease-prediction-ml-models.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SiwbOr5clC9MvwsBR7PkBFFtndPZOXxE

## ***Name : `Fawad Ali Shaikh`***
## ***Dataset :***  [***`UCI Heart Disease`***](https://www.kaggle.com/datasets/redwankarimsony/heart-disease-data)

## ***Import Libraries***
"""

# install catboost library

pip install "dask[dataframe]"

# to handle data
import pandas as pd
import numpy as np

# to visualize data
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# to preprocess data

from sklearn.preprocessing import StandardScaler,MinMaxScaler,LabelEncoder
from sklearn.impute import SimpleImputer,KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer



# machine learning tasks
from sklearn.model_selection import cross_val_score,train_test_split,GridSearchCV, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier



#metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_absolute_error,mean_squared_error,r2_score

# ignore warnings

import warnings
warnings.filterwarnings('ignore')

"""## ***Load the Dataset***"""

# Load dataset
url = 'url = 'https://raw.githubusercontent.com/AbdelliOussama/Heart-Disease-Prediction/refs/heads/main/heart_disease_uci.csv'
df = pd.read_csv(url)
df.head()

from google.colab import drive
drive.mount('/content/drive')

"""##***Expolratory Data Analysis (EDA)***"""

df.shape

print(f'Number of rows: {df.shape[0]}')
print(f'Number of columns: {df.shape[1]}')

# Columns in the dataset

print(df.columns)

# Inforamtion about dataset

df.info()

# unique values in columns

df.nunique()

# check null values in percentage

print(df.isnull().sum().sort_values(ascending=False))

# Heatmap of missing values

fig = plt.figure(figsize=(12,6))
sns.heatmap(df.isnull(),cbar=True,cmap='Blues')
plt.title('Heatmap of Missing Values')
plt.show()

"""### ***Impute Missing Values***"""

df.info()

# check null values in percentage

print(df.isnull().sum().sort_values(ascending=False)/len(df)*100)

# split data into numerical & categorical columns

num_cols = [col for col in df.columns if df[col].dtype!='O']
cat_cols = [col for col in df.columns if col not in num_cols]

# impute missing values in numeric columns using iterative imputer

df[num_cols] = IterativeImputer().fit_transform(df[num_cols])

# check null values

print(df.isnull().sum().sort_values(ascending=False)/len(df)*100)

# Impute categorical columns using Random Forest Classifier

for col in cat_cols:
    # Separate data into known and unknown values for the current column
    known_data = df[df[col].notna()]
    unknown_data = df[df[col].isna()]

    # Check if there are any unknown values to impute
    if unknown_data.shape[0] > 0:  # Proceed only if there are unknown values
        # Define features and target for the Random Forest model
        # Exclude categorical features from X_known
        X_known = known_data.drop(columns=[col] + cat_cols)  # Exclude all cat_cols
        y_known = known_data[col]
        X_unknown = unknown_data.drop(columns=[col] + cat_cols) # Exclude all cat_cols

        # Create and fit LabelEncoder for the target variable
        encoder = LabelEncoder()
        y_known_encoded = encoder.fit_transform(y_known)

        # Create and train a Random Forest classifier
        model = RandomForestClassifier()
        model.fit(X_known, y_known_encoded)

        # Predict missing values and impute them in the DataFrame
        imputed_values = model.predict(X_unknown)
        imputed_values = encoder.inverse_transform(imputed_values)  # Inverse transform to get original labels
        df.loc[df[col].isna(), col] = imputed_values

# check null values

print(df.isnull().sum().sort_values(ascending=False))

# Heatmap of missing values

fig = plt.figure(figsize=(12,6))
sns.heatmap(df.isnull(),cbar=True,cmap='Blues')
plt.title('Heatmap of Missing Values')
plt.show()

"""***So we have 0 null values in the dataset***



---

## ***Let's Deal with Outliers***
"""

df.info()

# Boxplot of numeric columns using for loop
plt.figure(figsize=(20, 30))

# Extend the colors list to have at least as many colors as num_cols
colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'brown', 'cyan', 'magenta']

# Adjusted subplot grid to 4 rows, 2 columns to accommodate 8 plots
for i, col in enumerate(num_cols):
    plt.subplot(4, 2, i+1)  # Changed to 4 rows, 2 columns
    sns.boxplot(x=df[col], color=colors[i % len(colors)]) # Use modulo operator to cycle through colors
    plt.title(col)
plt.show()

# row where trestbps is 0

df[df['trestbps']==0]

# remove row where trestbps is 0

df.drop(df[df['trestbps']==0].index,inplace=True)

# make Boxplot of numeric columns using for loop
plt.figure(figsize=(20, 30))

# Extend the colors list to have at least as many colors as num_cols
colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'brown', 'cyan', 'magenta']

# Adjusted subplot grid to 4 rows, 2 columns to accommodate 8 plots
for i, col in enumerate(num_cols):
    plt.subplot(4, 2, i+1)  # Changed to 4 rows, 2 columns
    sns.boxplot(x=df[col], color=colors[i % len(colors)]) # Use modulo operator to cycle through colors
    plt.title(col)
plt.show()

"""* ***So we have removed one outlier from our data***"""

df.info()

"""---

### ***Let's again Explore the dataset***
"""

df.info()

"""### ***Explore data based on Sex & Age***"""

# Explore age column

df['age'].describe()

"""*  ***Maximum age is 77***
*   ***Minimum age is 28***
* ***Mean is 53***




"""

df['age'].unique()

print(df['age'].value_counts().sort_values(ascending=False))

# histplot of age using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df['age'], kde=True)
plt.axvline(df['age'].mean(),color='red')
plt.axvline(df['age'].median(),color='green')
plt.axvline(df['age'].mode()[0],color='blue')

# print the values of mean, median & mode
print('Mean',df['age'].mean())
print('Median',df['age'].median())
print('Mode',df['age'].mode())

df['sex'].value_counts()

print(df.groupby('sex')['age'].value_counts())

# histplot of age having color by sex

fig = px.histogram(df,x='age',title='Age Distribution',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

"""* ***So most of the males & females in the age of 54-55 are affected by this.***
* ***Males are affected more than females.***

### ***Explore data based on Dataset & Sex***
"""

df['dataset'].unique()

df['dataset'].value_counts()

# countplot of dataset

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='dataset', hue='sex')
plt.title('Countplot of Dataset')
plt.show()

"""*   ***So, in the dataset cleveland has more patients (304)***
*   ***Switzerland has less patients (123)***
* ***Most males are from Hungary anf least from Switzerland.***
* ***Most females are from Cleveland and least from VA Long Beach	.***

### ***Explore the Age with dataset column***
"""

# histplot of age color by dataset

fig = px.histogram(df,x='age',title='<b><i>Age Distribution based on Dataset<i><b>',color='dataset')
fig.update_layout(width=1200, height=600)
fig.show()

# histplot using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df,x='age',hue='dataset')
plt.title('Age Distribution based on Dataset')
plt.show()

# print mean, median and mode

print('Mean',df.groupby('dataset')['age'].mean())
print('-------------------')
print('Median',df.groupby('dataset')['age'].median())
print('-------------------')
print('Mode',df.groupby('dataset')['age'].agg(pd.Series.mode))

"""* ***Mean of the dataset column is different***
* ***Median is different***
* ***Mode is also different***

***So Mean, Median & Mode of dataset column (Cleveland, Hungary, Switzerland and VA Long Beach) is different***

### ***Explore CP (Chest Pain)***
"""

# value counts of cp

df['cp'].value_counts()

# histogram of cp based on age

fig = px.histogram(df,x='age',title='CP Distribution',color='cp')
fig.update_layout(width=1200, height=600)
fig.show()

# print mean, median and mode

print('Mean',df.groupby('cp')['age'].mean())
print('-------------------')
print('Median',df.groupby('cp')['age'].median())
print('-------------------')
print('Mode',df.groupby('cp')['age'].agg(pd.Series.mode))

# counplot of cp based on sex

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='cp', hue='sex')
plt.title('Countplot of CP')
plt.show()

"""* ***Most Male and Female are affected by asymptomatic angina***
***Least Male and Female are affected by typical angina***
"""

# counplot of cp based on dataset

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='cp', hue='dataset')
plt.title('Countplot of CP')
plt.show()

"""* ***Most of the asymptomatic patients are from Cleveland and least from Switzerland***
***Hungary has most atypical agina patients Switzerland has least***
***Cleveland, Hungary, Switzerland and VA Long Beach has least typical angina patients***

### ***Explore trestbps (Resting Blood Pressure)***
"""

# Value counts

df['trestbps'].value_counts()

# describe trestbps

df['trestbps'].describe()

# histplot of trestbps based on sex

fig = px.histogram(df,x='trestbps',title='Resting Blood Pressure',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# histplot of trestbps based on sex using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df,x='trestbps',hue='sex',kde = True)
plt.title('Resting Blood Pressure')
plt.show()

"""***This shows the distribution of `trestbps` based on `sex`***

### ***Explore Chol (Cholestrol)***
"""

# Value counts

df['chol'].value_counts()

# describe chol

df['chol'].describe()

# histplot of chol based on sex

fig = px.histogram(df,x='chol',title='Cholestrol',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# histplot of chol based on sex using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df,x='chol',hue='sex',kde = True)
plt.title('Cholestrol')
plt.show()

"""***This shows that chol is not normally distributed***

### ***Explore fbs (Fasting Blood Sugar)***
"""

# Value Counts

df['fbs'].value_counts()

# histplot of fbs based on sex

fig = px.histogram(df,x='fbs',title='Fasting Blood Sugar',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# Countplot of fbs

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='fbs', hue='sex')
plt.title('Countplot of FBS')
plt.show()

"""***This shows that most males & females have no fbs***

### ***Explore restecg (Resting Electrocardiographic Results)***
"""

# Value Counts

df['restecg'].value_counts()

# histplot of restecg based on sex

fig = px.histogram(df,x='restecg',title='Resting Electrocardiographic Results ',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# Countplot of fbs

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='restecg', hue='sex')
plt.title('Countplot of Resting Electrocardiographic Results')
plt.show()

"""* ***Most males & females have `normal` restecg***
* ***Females have least `st-t abnormality`***
"""

# Countplot of fbs

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='restecg', hue='dataset')
plt.title('Countplot of FBS')
plt.show()

"""* ***Most of the patients from all dataset (Cleveland, Hungary, Switzerland & VA Long Beach) have `normal` restecg***
* ***Cleveland has most Iv `hypertrophy` patients***
* ***VA Long Beach has more `st-t abnormality` patients***

### ***Explore thalch (Maximum Heart Rate Achieved)***
"""

# Value Counts

df['thalch'].value_counts()

# describe

df['thalch'].describe()

# histplot of thalch based on sex

fig = px.histogram(df,x='thalch',title='Maximum Heart Rate Achieved',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# histplot of thalch based on sex using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df,x='thalch',hue='sex',kde = True)
plt.title('Maximum Heart Rate Achieved')
plt.show()

"""* ***This shows that it is not normally distributed***

### ***Explore exang (Exercise-Induced Angina)***
"""

# Value Counts

df['exang'].value_counts()

# histplot of exang based on sex

fig = px.histogram(df,x='exang',title='Exercise-Induced Angina',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# Countplot of exang based on sex

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='exang', hue='sex')
plt.title('Countplot of Exercise-Induced Angina')
plt.show()

"""* ***Most males anf females have false exang***"""

# Countplot of exang based on dataset

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='exang', hue='dataset')
plt.title('Countplot of Exercise-Induced Angina')
plt.show()

"""* ***VA Long Beach has more true `exang` patients and Switzerland has least true exang patients***
* ***Cleveland and Hungary has most false exang patients***

### ***Explore oldpeak (Depression)***
"""

# Value Counts

df['oldpeak'].value_counts()

# describe

df['oldpeak'].describe()

# histplot of oldpeak based on sex

fig = px.histogram(df,x='oldpeak',title='Depression',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# histplot of oldpeak based on sex using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df,x='oldpeak',hue='sex',kde = True)
plt.title('Depression')
plt.show()

"""* ***This shows that it is not normally distributed***

### ***Explore slope (Slope of the peak exercise ST segment)***
"""

# Value Counts

df['slope'].value_counts()

# histplot of slope based on sex

fig = px.histogram(df,x='slope',title='Slope of the peak exercise ST segment',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# Countplot of slope

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='slope', hue='sex')
plt.title('Countplot of Slope')
plt.show()

"""* ***Males have more `flat slope` and least` doensloping slope`***
* ***Females have more `upsloping slope` and least `doensloping slope`***
"""

# Countplot of slope

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='slope', hue='dataset')
plt.title('Countplot of FBS')
plt.show()

"""* ***Hungary, Cleveland & VA LongBeach have more `falt slope` patients***
* ***Hungary has least `doensloping` patients***

### ***Explore ca (Coronary Artery Calcification)***
***Coronary artery calcification is a buildup of calcium that can predict your cardiovascular risk. Symptoms like chest pain usually don’t happen until you’ve had it for a while. There are two main forms of coronary artery disease: stable ischemic heart disease and acute coronary syndrome.***
"""

# Value Counts

df['ca'].value_counts()

# describe

df['ca'].describe()

# histplot of ca based on sex

fig = px.histogram(df,x='ca',title='Coronary Artery Calcification',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# histplot of ca based on sex using seaborn

fig = plt.figure(figsize=(12,6))
sns.histplot(df,x='ca',hue='sex',kde = True)
plt.title('Coronary Artery Calcification')
plt.show()

"""* ***This shows that it is not normally distributed***

### ***Explore thal (Thalassemia)***
"""

# Value Counts

df['thal'].value_counts()

# histplot of thal based on sex

fig = px.histogram(df,x='thal',title='Thalassemia',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

# Countplot of thal

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='thal', hue='sex')
plt.title('Countplot of Thalassemia')
plt.show()

"""* ***Most males have `Thalassemia (Reversible Defect)`***
* ***Most females have `Thalassemia (Normal)`***
* ***Both males & females have least `Thalassemia (Fixed Defect)`***
"""

# Countplot of thal

fig = plt.figure(figsize=(12,6))
sns.countplot(df,x ='thal', hue='dataset')
plt.title('Countplot of Thalassemia based on Dataset')
plt.show()

"""* ***VA Long Beach has most Thalassemia (Reversible defect) patients***
* ***Cleveland has most Thalassemia (Normal) patients***
* ***VA Long Beach has least Thalassemia (Normal) patients***

### ***Explore num***
***NUM specified whether a patient has the presence or absence of heart disease.A score of 120/80 is optimal, and 140/90 is normal for most people. Higher readings mean that arteries aren’t responding right to the force of blood pushing against artery walls (blood pressure), directly raising the risk of heart attack or stroke.***
"""

# Value Counts

df['num'].value_counts()

# describe

df['num'].describe()

# histplot of num based on sex

fig = px.histogram(df,x='num',title='Heart Disease',color='sex')
fig.update_layout(width=1200, height=600)
fig.show()

"""## ***Apply Machine Learning***
***We predict our target value `num` & use this column to predict heart disease.***

***Num has 5 values `0, 1, 2, 3, 4` which states five types of heart disease***
"""

# Split data into X and y

X = df.drop('num',axis=1)
y = df['num']

# Categorical Columns

cat_cols

# label encode categorical variables

le = LabelEncoder()
X['sex'] = le.fit_transform(X['sex'])
X['dataset'] = le.fit_transform(X['dataset'])
X['cp'] = le.fit_transform(X['cp'])
X['fbs'] = le.fit_transform(X['fbs'])
X['restecg'] = le.fit_transform(X['restecg'])
X['exang'] = le.fit_transform(X['exang'])
X['slope'] = le.fit_transform(X['slope'])
X['thal'] = le.fit_transform(X['thal'])

# Train Test the data

X_train, X_test, y_train, y_test = train_test_split(X,y , test_size=0.2, random_state=42)

# Create a dictionaries of list of models to evaluate performance
models = {
          'LogisticRegression' : LogisticRegression(random_state=42),
          'SVC' : SVC(random_state=42),
          'DecisionTreeClassifier' :DecisionTreeClassifier(random_state=42),
          'RandomForestClassifier' :RandomForestClassifier(random_state=42),
          'KNeighborsClassifier' : KNeighborsClassifier(),
          'GradientBoostingClassifier' : GradientBoostingClassifier(random_state=42),
          'XGBClassifier' : XGBClassifier(),
          'AdaBoostClassifier': AdaBoostClassifier(random_state=42),
          'GaussianNB': GaussianNB(), # Changed to only the model
          'LGBMClassifier': LGBMClassifier(verbose =-1, random_state=42),
          'CatBoostClassifier': CatBoostClassifier(verbose=0, random_state=42)
          }

# train and predict each model with evaluation metrics as well making a for loop to iterate over the models

model_scores = []
for name, model in models.items():
    # fit each model from models on training data
    model.fit(X_train, y_train)

    # make prediction from each model
    y_pred = model.predict(X_test)
    metric = mean_absolute_error(y_test, y_pred)
    model_scores.append((name, metric))

    # print the performing metric
    print(name, 'MSE: ', mean_squared_error(y_test, y_pred))
    print(name, 'R2: ', r2_score(y_test, y_pred))
    print(name, 'MAE: ', mean_absolute_error(y_test, y_pred))
    print('\n')

# selecting the best model from all above models with evaluation metrics sorting method
refine_models = sorted(model_scores, key=lambda x: x[1], reverse=False)
for model in refine_models:
    print('Mean absolute error for', f"{model[0]} is {model[1]: .2f}")

"""## ***Hyperparamter Tuning***"""

# Create a dictionaries of list of models to evaluate performance

models = {
    'LogisticRegression': (LogisticRegression(random_state=42), {'model__penalty': ['l1', 'l2'],'model__C': [0.001, 0.1, 1],'model__solver': ['liblinear', 'saga']}),
    'SVC': (SVC(random_state=42), {'model__kernel': ['linear'],'model__degree': [2]}),
    'DecisionTreeClassifier': (DecisionTreeClassifier(random_state=42), {'model__max_depth': [None, 5, 10], 'model__splitter': ['best', 'random']}),
    'RandomForestClassifier': (RandomForestClassifier(random_state=42), {'model__n_estimators': [10, 100, 1000], 'model__max_depth': [None, 5, 10]}),
    'KNeighborsClassifier': (KNeighborsClassifier(), {'model__n_neighbors': np.arange(3, 100, 2), 'model__weights': ['uniform', 'distance']}),
    'GaussianNB': (GaussianNB(), {'model__var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4]}),
    'GradientBoostingClassifier': (GradientBoostingClassifier(random_state=42), {'model__loss': ['log_loss', 'exponential'], 'model__n_estimators': [10, 100, 1000]}),
    'AdaBoostClassifier': (AdaBoostClassifier(random_state=42), {'model__n_estimators': [10, 100, 1000], 'model__learning_rate': [0.1, 0.01, 0.001]}),
    'LGBMClassifier': (LGBMClassifier(max_depth=10,min_data_in_leaf=20,num_leaves=31,learning_rate=0.01,n_estimators=200,lambda_l1=0.1,lambda_l2=0.1,boosting_type='gbdt'), {}),
    'CatBoostClassifier': (CatBoostClassifier(verbose=0, random_state=42), {'model__iterations': [100, 500, 1000], 'model__learning_rate': [0.01, 0.1, 1.0]}),
    'XGBClassifier': (XGBClassifier(use_label_encoder=False, eval_metric='logloss'), {}),
}

results = []

# Train and predict each model with evaluation metrics
for name, (model, params) in models.items():
    # Create a pipeline with the model
    pipeline = Pipeline(steps=[('model', model)])

    # Create a grid search CV to tune the hyperparameters
    grid_search = GridSearchCV(pipeline, params, cv=5)

    # Fit the pipeline
    grid_search.fit(X_train, y_train)

    # Make predictions
    y_pred = grid_search.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # print the performing metric
    print(name, 'MSE: ', mean_squared_error(y_test, y_pred))
    print(name, 'R2: ', r2_score(y_test, y_pred))
    print(name, 'MAE: ', mean_absolute_error(y_test, y_pred))
    print('\n')

    # Store results
    results.append({"Model": name, "MSE": mse, "R2": r2, "MAE": mae})

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(results)

# Select the best model based on the lowest MSE
best_model = results_df.loc[results_df['MAE'].idxmin()]

print("\nBest Model:")
print(best_model)

# Sort the results DataFrame by MSE in ascending order
sorted_results_df = results_df.sort_values(by='MAE')

# Set the aesthetics of the plot
sns.set(style="darkgrid", palette="pastel")

# Create a bar plot
plt.figure(figsize=(12, 6))
bars = plt.bar(sorted_results_df['Model'], sorted_results_df['MAE'], color=sns.color_palette("viridis", len(sorted_results_df)))

# Highlight the best model
best_model_index = sorted_results_df['MAE'].idxmin()
bars[best_model_index].set_color('orange')

# Adding labels and title with enhanced font styling
plt.xlabel('Models', fontsize=14, fontweight='bold')
plt.ylabel('Mean Absolute Error ', fontsize=12, fontweight='bold')
plt.title('Model Performance Comparison ', fontsize=16, fontweight='bold')
plt.xticks(rotation=90, fontsize=12, fontweight='medium')
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adding a shadow effect to the bars
for bar in bars:
    bar.set_edgecolor('black')
    bar.set_linewidth(1.5)
    bar.set_alpha(0.9)  # Slight transparency for better visibility

# Add data labels on top of the bars with more styling
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2),
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Show the plot with a tight layout
plt.tight_layout()
plt.show()

"""## ***So the best the model is  `GradientBoosting Classifier`***

## ***If you like `upvote` it and `share`.***
"""

!jupyter nbconvert --to script heart-disease-prediction-ml-models.ipynb

!ls -lh
