import json
import csv



with open('data/EGC_tweets.json', "rb") as t:
  tweets = json.load(t)

graph = open('data/graph_tweet.csv', 'w', encoding="utf8")

for f in tweets:
  author = f['user']['name']
  if 'retweeted_status' in f.keys():
    name = f['retweeted_status']['user']['name']
    stra = author + "," + name + "\n"
    graph.write(stra)
  else:
    stra = author + "," + author + "\n"
    graph.write(stra)
  ''' 
    if name not in dict_name_rt.keys():
        dict_name_rt[name] = 0
    dict_name_rt[name] += 1
  else :
    name = f['user']['name']
    if name not in dict_name_rt.keys():
        dict_name_rt[name] = 0
    dict_name_rt[name] += 1
    '''

  print("-----------------------------")
  #print(f["entities"]["user_mentions"])

  #print(f['retweeted_status']['user']['name'])
  #print("Nombre de retweets " ,f["retweet_count"])

