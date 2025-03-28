
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
from input_pipeline import *
from calculate_stats import *
from images_page import *

st.set_page_config(page_title='Medical Visualisation',page_icon=':bar_chart:',layout='wide')
#st.title('Medical Visualisation',)
st.markdown("<h1 style='text-align: center; color: white;'>Medical Visualisation</h1>", unsafe_allow_html=True)

_ = """st.header('Upload File')
uploaded_file = st.file_uploader('')
if uploaded_file == None:
    st.info("Upload a file to start visualising!",icon='ℹ️')
    st.stop()"""

uploaded_file = os.path.join(os.getcwd(),'data', 'NAKO_536_61223_export_baseln_MRT_PSN_wie_194.csv')
data = pd.read_csv(uploaded_file,delimiter=';')

df = pd.DataFrame(data)
#st.data_editor(df)
missing_dict = preprocess_data(df)
missing_stats = visualise_missing_data(df,missing_dict)

_ = """x_label = st.text_input("Enter the x_label", key='x_label')
y_label = st.text_input("Enter the y_label", key='y_label')
plot_button = st.button('Create a Plot')
if plot_button:
    print(df.columns)
    if x_label in df.columns and y_label in df.columns:
        print("valid labels")
        fig = px.line(df,x=x_label,y=y_label,title=f'{x_label} Vs {y_label}')
        fig.show()"""


keys = list(missing_stats.keys())
values_list = list(missing_stats.values())
fig = px.bar(values_list,x=keys,y=values_list,labels= {'x':'Features','y':'Missing Values'})

df = diabetes_bp_stats(df)
bins = list(range(20,90,10))
labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]



fig3 = px.box(df,x='basis_sex',y='anthro_fettmasse')

merged_df = merge_data(df)
fig4 = px.violin(merged_df,x='category',y='ff_Glu',color="basis_sex",box=True,hover_data=merged_df.columns,
                 color_discrete_sequence=["#636EFA", "#EF553B"])
fig4.for_each_trace(lambda t: t.update(name="Male" if t.name == "1" else "Female"))

st.subheader('Missing Values')
with st.expander("🔍 Click to Expand/Collapse - Missing Values"):
    st.plotly_chart(fig,use_container_width=True)

col1,col2 = st.columns(2)
with col1:
    st.subheader('Metabolic Diseases')
with col2:
    cat = st.selectbox('Categorize By:',['Gender','Age'],index=1)
if cat == 'Gender':
    grouped_df = df.groupby(['category','basis_sex']).size().reset_index(name='count')
    male_data = grouped_df[grouped_df['basis_sex'] == 1]
    female_data = grouped_df[grouped_df['basis_sex'] == 2]
    col1 , col2 = st.columns(2)
    with col1:
        fig2 = px.pie(male_data,values='count',names='category',title='Male')
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2)
    with col2:
        fig5 = px.pie(female_data,values='count',names='category',title='Female')
        st.plotly_chart(fig5)
else:
    df['age_group'] = pd.cut(df['basis_age'],bins=bins,labels=labels,right=True)
    grouped_df = df.groupby(['category','age_group']).size().reset_index(name='count')
    fig2 = px.histogram(grouped_df,x='age_group',y='count',color='category')
    st.plotly_chart(fig2)
    

st.subheader('FatMass Distribution')
col1,col2 = st.columns(2)
with col1:  
    with st.expander("🔍 Click to Expand/Collapse - FatMass Distribution"):
        st.plotly_chart(fig3)
with col2:
    with st.expander("🔍 Click to Expand/Collapse - FatMass Distribution"):
        st.plotly_chart(fig4)

Feature_importance()