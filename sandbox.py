
# Input: query, retrieved relevant Reddit pages (question, all responses), all products and brands listed on those pages

# Output: list of ranked product recommendations, an explanation for each, and a list of Reddit posts for each explanation

# Steps: 
# 1) Create product:score map and brand:score map.
# 2) For each comment: for each product/brand, assign sentiment from 0-1 (might have to normalize). Add to appropriate map.
# 3) Distribute brand scores among products with that brand proportional to the # times they were mentioned? (think about edge cases here)
# 4) Generate list of products, ranked by scores.
# 5) For each product in the list, retrieve *n* comments via BERT embeddings + KNN.
# 6) Summarize these comments.

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import np
import faiss
import openai
import pickle
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from praw_auth import reddit
from oai_auth import auth as oai_auth_info
from test_data_8fltsy import products, brands

openai.organization = oai_auth_info["organization"]
openai.api_key = oai_auth_info["api_key"]

try:
  all_comments_text = pickle.load(open("8fltsy_comments", "rb"))
except (OSError, IOError) as e:
  submission = reddit.submission('8fltsy')
  all_comments = submission.comments.list()
  all_comments_text = [f'[{i}] ' + all_comments[i].body for i in range(len(all_comments))]
  pickle.dump(all_comments_text, open("8fltsy_comments", "wb"))

# print("\n\n========\n\n".join(all_comments_text))

try:
  sentiments = pickle.load(open("8fltsy_sentiments", "rb"))
except (OSError, IOError) as e:
  sentiment_pipeline = pipeline('sentiment-analysis', model='siebert/sentiment-roberta-large-english')
  sentiments = sentiment_pipeline(all_comments_text)
  pickle.dump(sentiments, open("8fltsy_sentiments", "wb"))

product_scores = {}
product_to_comment = {}

for i in range(len(products)):
  product_list = products[i]
  sentiment = round(sentiments[i]['score']) * (1 if sentiments[i]['label'] else -1)

  for product in product_list:
    product_scores[product] = product_scores.get(product, 0) + sentiment
    product_to_comment[product] = product_to_comment.get(product, []) + [all_comments_text[i]]

# for i in range(len(brands)):
#   brand_list = brands[i]
#   sentiment = round(sentiments[i]['score']) * (1 if sentiments[i]['label'] else -1)

final_list = list(product_scores.items())
score_sum = sum([p[1] for p in final_list])
final_list = [(p[0], round(p[1]/score_sum * 100)) for p in final_list]
final_list.sort(key=lambda p: p[1], reverse=True)

# ========= substituted with retrieval of comments mentioning product, ranked by votes =========

# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# product_embeddings = np.array([model.encode(p[0]) for p in final_list]).astype("float32")
# comment_embeddings = np.array([model.encode(comment) for comment in all_comments_text]).astype("float32")

# index = faiss.IndexFlatL2(comment_embeddings.shape[1])
# index.add(comment_embeddings)

# product_to_related_reviews = {}

# for i in range(len(product_embeddings)):
#   D, I = index.search(np.array([product_embeddings[i]]), k=3)
#   comment_index = I.flatten().tolist()

#   related_comments = [all_comments_text[i] for i in comment_index]
#   product_to_related_reviews[final_list[i][0]] = related_comments

# print("\n".join([" : ".join((p[0], str(p[1]) + "%")) for p in final_list]))

# ================================================================================================

max_products = 3
max_comments = 3

for p in final_list[:3]:
  print("\n====================\n\n")
  print(" : ".join((p[0], str(p[1]) + "%")))

  relevant_comments = product_to_comment[p[0]][:max_comments]

  print("\n\n")
  print("\n\n".join(relevant_comments))

  formatted_relevant_comments = '[END]'.join(relevant_comments)

  print("\n\nSummary:\n")
  summary = openai.Completion.create(
    model="text-curie-001",
    prompt=f"Summarize the following comments on Reddit in a sentence or two: {formatted_relevant_comments}",
    max_tokens=100,
  )

  print(summary.choices[0].text)