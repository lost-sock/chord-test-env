# import requests

# app_id = "Zz0YSslrxGUeVHBTbAviIw"
# secret = "_iDzYRnZ9jRgtv3Y9tE9bcTixkuagg"

# auth = requests.auth.HTTPBasicAuth(app_id, secret)

# data = {
#   'grant_type': 'password',
#   'username': 'red-tip',
#   'password': 'aeonianriver0'
# }

# headers = {'User-Agent': 'ChordProductTest/0.0.1'}

# res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

# token = res.json()['access_token']
# headers['Authorization'] = f'bearer {token}'

# # api = 'https://oauth.reddit.com'
# # res = requests.get(f'{api}/r/stanford/hot', headers=headers)

# # posts = res.json()['data']['children']

# # for post in posts:
# #   print(post['data']['title'])

# comments = requests.get('https://www.reddit.com/r/BuyItForLife/comments/u0m6zp/')

# print(comments.json())