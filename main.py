import tweepy
from rake_nltk import Rake
from textblob import TextBlob
import matplotlib.pyplot as plt
import tweepy_keys as tk

def percentage(part, whole):
    return 100 * float(part)/float(whole)


r = Rake()

auth = tweepy.OAuthHandler(tk.consumer_key, tk.consumer_secret)
auth.set_access_token(tk.access_token, tk.access_token_secret)

api = tweepy.API(auth)
searchItem = input("Enter keyword/hashtag to search about: ")
noOfSearchItems = int(input("Enter how many tweets to analyze: "))
tweets = tweepy.Cursor(api.search, q=searchItem).items(noOfSearchItems)

positive = 0
negative = 0
neutral = 0
polarity = 0

for tweet in tweets:
    myTweet = tweet.text
    list1 = myTweet.split()
    for i in list1:
        if (i.startswith('http') or i.startswith('@')):
            list1.remove(i)
    myNewTweet = " ".join(list1)
    r.extract_keywords_from_text(myNewTweet)
    keywords = r.get_ranked_phrases()
    new_tweet = " ".join(keywords)
    analysis = TextBlob(new_tweet)
    polarity += analysis.sentiment.polarity

    if(analysis.sentiment.polarity == 0):
        neutral += 1
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
    elif (analysis.sentiment.polarity > 0.00):
        positive += 1


positive = percentage(positive, noOfSearchItems)
negative = percentage(negative, noOfSearchItems)
neutral = percentage(neutral, noOfSearchItems)
polarity = percentage(polarity, noOfSearchItems)

positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')

print("How people are reacting on " + searchItem + " by analyzing " + str(noOfSearchItems) + " tweets. ")
if(polarity == 0):
    print("Neutral")
elif(polarity < 0.00):
    print("Negative")
if(polarity > 0.00):
    print("Positive")

labels = ['Positive ['+str(positive)+'%]', 'Neutral ['+str(neutral)+'%]', 'Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc='best')
plt.title("How people are reacting on " + searchItem + " by analyzing " + str(noOfSearchItems) + " tweets. ")
plt.axis('equal')
plt.tight_layout()
plt.show()