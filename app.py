# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 02:23:11 2022

@author: HP
"""

#!pip install streamlit
#!pip install --upgrade ipython

import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go


countries = ['brazil', 'united states']
intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today()-timedelta(days=30)
end_date = datetime.today()


@st.cache(allow_output_mutation=True)
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df


def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig


# CRIANDO UMA BARRA LATERAL
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Select Country:", countries)
acoes = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Select the Asset:", acoes)
from_date = st.sidebar.date_input('Start Date:', start_date)
to_date = st.sidebar.date_input('End Date:', end_date)
interval_select = st.sidebar.selectbox('Interval:', intervals)
carregar_dados = st.sidebar.checkbox('Load Data')


grafico_line = st.empty()
grafico_candle = st.empty()

# elementos centrais da página
st.title('Stock Monitor')

st.header('Action')

st.subheader('Graphical Visualization')


if from_date > to_date:
    st.sidebar.error('Start Date greater than End Date')
else:
    df = consultar_acao(stock_select, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)
        if carregar_dados:
            st.subheader('Data')
            dados = st.dataframe(df)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)