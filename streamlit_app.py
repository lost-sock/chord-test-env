import streamlit as st
from sandbox import get_product_df

st.title("Chord")

query = st.text_input("Product", value="")

if query:
  st.write("You searched for " + query)

  num_results = 5
  with st.spinner('Getting products...'):
    product_df = get_product_df(query)[['comments', 'score', 'summary']].head(num_results)

  st.table(product_df)