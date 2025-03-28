import streamlit as st


def categorize(row):
    
    #High Blood Pressure and Diabetes Mellitus and Cholestrol in Blood
    if row['d_an_cv_6'] == 1 and row['d_an_met_1'] == 1 and row['d_an_met_2'] == 1:
        return 'All Three'

    elif row['d_an_cv_6'] == 1 and row['d_an_met_1'] == 1:
        return 'BP and Diabetes'
    
    elif row['d_an_cv_6'] == 1 and row['d_an_met_2'] == 1:
        return 'BP and Cholestrol'
    
    elif row['d_an_met_1'] == 1 and row['d_an_met_2'] == 1:
        return 'Diabetes and Cholestrol'
    
    else:
        if row['d_an_cv_6'] == 1:
            return 'BP'
        elif row['d_an_met_1'] == 1:
            return 'Diabetes'
        elif row['d_an_met_2'] == 1:
            return 'Cholestrol'
        else:
            return 'None' 

def diabetes_bp_stats(df):
    df['category'] = df.apply(categorize,axis=1)
    return df
