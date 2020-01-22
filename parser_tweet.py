import json
import csv

import unidecode


def hashtagYear():
  with open('data/EGC_tweets.json', "rb") as t:
    tweets = json.load(t)

  dict_year_rt = {}
  graph = open('data/graph_tweet_hashtag.txt', 'w', encoding="utf8")
  for f in tweets :
    author = f['user']['name'].replace(" ", '_')
    year = f['created_at']
    year = year[len(year) - 4:len(year)]  # pour avoir que l'annee
    for t in f['entities']['hashtags'] :
      hashtag = t['text']
      if(year, hashtag) not in dict_year_rt.keys() :
        dict_year_rt[(year,hashtag)] = 0
      dict_year_rt[(year,hashtag)] += 1
  sorted_dict = sorted(dict_year_rt.items(), key=lambda t: t[1], reverse=True)
  year16=0
  year17=0
  year18=0
  year19=0
  for key,value in sorted_dict:
    hashtag = unidecode.unidecode(key[1])
    s = key[0] + " " + hashtag + " " + str(value)+ "\n"
    print(s)
    if(value>1 and key[0] =="2016"):
      graph.write(s)

  graph.close()
  print(len(sorted_dict))

def nbr_tweets_par_an():
  with open('data/EGC_tweets.json', "rb") as t:
    tweets = json.load(t)

  dict_year_rt = {}
  graph = open('data/graph_tweet_par_an.txt', 'w', encoding="utf8")
  for f in tweets :

    author = f['user']['name'].replace(" ", '_')  # nom de l'auteur du retweet
    year = f['created_at']
    year = year[len(year)-4:len(year)]#pour avoir que l'annee
    print(year)


    if year not in dict_year_rt.keys():  # Pour compter le nombre d'occurence des differentes origines des tweets selon l'annee
      dict_year_rt[year] = 0
    dict_year_rt[year] += 1

  for key , value in dict_year_rt.items():
    year =key
    stra = author + " " + year + " " + str(value) + "\n"
    print(stra)
    graph.write(stra)
  graph.close()
  print(dict_year_rt)

def occurence_origin_tweet():
  with open('data/EGC_tweets.json', "rb") as t:
    tweets = json.load(t)

  dict_name_rt = {}
  graph = open('data/graph_tweet.txt', 'w', encoding="utf8")

  for f in tweets:  # Pour chaque retweet de l'association EGC

    author = f['user']['name'].replace(" ", '_')  # nom de l'auteur du retweet

    if 'retweeted_status' in f.keys():  # Si retweeted statud existe , alors c'est un retweet d'un post d'un autre user
      name = f['retweeted_status']['user']['name'].replace(" ", '_')
    else:  # L'auteur a creer le tweet
      name = author

    if name not in dict_name_rt.keys():  # Pour compter le nombre d'occurence des differentes origines des tweets
      dict_name_rt[name] = 0
    dict_name_rt[name] += 1

    print("-----------------------------")
    # print(f["entities"]["user_mentions"])

    # print(f['retweeted_status']['user']['name'])
    # print("Nombre de retweets " ,f["retweet_count"])

  print(sorted(dict_name_rt.items(), key=lambda t: t[1], reverse=True))
  sorted_dict = sorted(dict_name_rt.items(), key=lambda t: t[1], reverse=True)
  sorted_dict = sorted_dict[:10]

  author = sorted_dict[0][0]

  for key in sorted_dict:
    name = unidecode.unidecode(key[0])
    stra = author + " " + name + " " + str(key[1]) + "\n"
    print(stra)
    graph.write(stra)
  print("-------------------------+++++++++")
  print(sorted_dict)

  graph.close()

#nbr_tweets_par_an()
hashtagYear()