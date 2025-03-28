import os
import pandas as pd

def preprocess_data(df):
    
    def missing_values():
        metadata_path = os.path.join(os.getcwd(),'data', 'NAKO_536_61223_export_baseln_MRT_PSN_wie_194_Metadaten.csv')
        metadata = pd.read_csv(metadata_path,delimiter=';')

        missings_dict = {}

        for row in metadata.iterrows():
            row = row[1]
            variable_name = row[0]
            missing_value = row[2]

            if not pd.isna(row[3]):
                if'(Missing)' in row[3]:

                    if variable_name in missings_dict:
                        missings_dict[variable_name].append(missing_value)
                    else:
                        missings_dict[variable_name] = [missing_value]
        return missings_dict

    return missing_values()


def visualise_missing_data(df,missings_dict):

    df_columns = {}

    for columns in df.columns:
        if columns in missings_dict.keys():
            count = df[columns].value_counts(dropna=False)
            #print(count)
            missing_values = 0
            #print(missings_dict[columns])
            for values in missings_dict[columns]:
                if values in count:
                    missing_values += count[values]
            if float('nan') in count:
                missing_values += count[float('nan')]
            df_columns[columns] = missing_values
    return df_columns

def merge_data(df):
    mri_data = pd.read_csv(os.path.join(os.getcwd(),'data', 'Fat_Fractions.csv'),sep=';')
    merged_df = pd.merge(df,mri_data,on='ID')
    merged_df['ff_Glu'] = merged_df.apply(lambda row :(row['ff_Glu_left']+row['ff_Glu_right'])/2,axis=1)
    return merged_df      




    