import openai
import streamlit as st
from sandbox import final_list, product_to_comment

st.title("Chord")

query = st.text_input("Product", value="")
st.write("You searched for " + query)

max_products = 3
max_comments = 3

for p in final_list[:3]:
  st.write("\n====================\n\n")
  st.write(" : ".join((p[0], str(p[1]) + "%")))

  relevant_comments = product_to_comment[p[0]][:max_comments]

  st.write("\n\n")
  st.write("\n\n".join(relevant_comments))

  formatted_relevant_comments = '[END]'.join(relevant_comments)

  st.write("\n\nSummary:\n")
  summary = openai.Completion.create(
    model="text-curie-001",
    prompt=f"Summarize the following comments on Reddit in a sentence or two: {formatted_relevant_comments}",
    max_tokens=100,
  )

  st.write(summary.choices[0].text)