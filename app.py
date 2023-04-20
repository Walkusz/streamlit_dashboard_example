import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title='My Page', layout='wide')
df_spending = pd.read_csv('DP_LIVE_03042023200203463.csv')
df_spending.set_index(['LOCATION', 'TIME'], inplace=True)

df_gdp = pd.read_csv('DP_LIVE_03042023202405420.csv')
df_gdp.set_index(['LOCATION', 'TIME'], inplace=True)

df = pd.merge(df_spending['Value'], df_gdp['Value'], left_index=True, right_index=True, suffixes=('_SPENDING', '_GDP'))
df.reset_index(inplace=True)
df['TIME'] = df['TIME'].astype(str)
countries = df['LOCATION'].unique()


selected = st.multiselect('Country', countries)
if selected:
    df = df[df['LOCATION'].isin(selected)]

height = 400
font_size = 5

c_gdp = alt.Chart(df, title='GDP').mark_line().encode(
     x='TIME', y=alt.Y('Value_GDP', title=''), color='LOCATION')
c_spending = alt.Chart(df, title='Spending').mark_line().encode(
     x='TIME', y='Value_SPENDING', color='LOCATION')

c_spending = c_spending.configure_legend(orient='bottom').configure_axis(labelFontSize=font_size, titleFontSize=font_size)
c_gdp = c_gdp.configure_legend(orient='bottom').configure_axis(labelFontSize=font_size, titleFontSize=font_size)

col1, col2 = st.columns(2)
col1.altair_chart(c_gdp, use_container_width=True)
col2.altair_chart(c_spending, use_container_width=True)

col1, col2 = st.columns(2)

