import os
import pandas as pd
import streamlit as st
from input_pipeline import *
from calculate_stats import *
from xgboost import XGBClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_selection import chi2,f_classif
from sklearn.ensemble import RandomForestClassifier

def remove_empty_rows(merged_df):
    for row in merged_df.iterrows():
        row = row[1]
        print(type(row['ID']))

def xg_boost_clf(X_train,X_test,y_train,y_test):
    clf = XGBClassifier(n_estimators=13, max_depth=7, learning_rate =1, objective='binary:logistic',num_classes=2)
    clf.fit(X_train,y_train)
    preds = clf.predict(X_test)
    accuracy = accuracy_score(y_test,preds)
    print(accuracy)
    feature_importance = clf.get_booster().get_score(importance_type='gain')

def univariate_anova_test(X_train,X_test,y_train,y_test):
    X = pd.concat([X_train,X_test])
    if isinstance(y_train,list):
        y = y_train+y_test
    else:
        y = pd.concat([y_train,y_test])

    f_values,p_values = f_classif(X,y)
    # Store results
    anova_results = pd.DataFrame({"Feature": X.columns, "F-Value": f_values, "P-Value": p_values})

    # Sort by Chi-Square Score
    anova_results = anova_results.sort_values(by="F-Value", ascending=False)
    # Display results
    print("Anova Feature Selection Results")
    print(anova_results)
    return f_values

def random_forest_clf(X_train,X_test,y_train,y_test):
    rf_clf = RandomForestClassifier(max_depth=2,random_state=0)
    rf_clf.fit(X_train,y_train)
    preds = rf_clf.predict(X_test)
    accuracy = accuracy_score(y_test,preds)
    print("Accuracy: ",accuracy)
    print("Classification Report")
    print(classification_report(y_test,preds))
    print(rf_clf.feature_importances_[:7])

def Feature_importance():
    df = pd.read_csv(os.path.join(os.getcwd(),'data','diabetes_binary_5050split_health_indicators_BRFSS2015.csv'),sep=',')
    target_labels = df['Diabetes_binary']
    df = df.drop('Diabetes_binary',axis=1)
    X_train,X_test,y_train,y_test = train_test_split(df,target_labels,test_size=0.2,shuffle=True,random_state=69)
    xg_boost_clf(X_train,X_test,y_train,y_test)