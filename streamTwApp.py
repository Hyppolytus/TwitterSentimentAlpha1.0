import tweepy
import streamlit as st
import openai

# Authenticate to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

st.title("Twitter Search")

# Search bar
search_query = st.text_input("Enter a search query")
num_tweets = st.slider("Number of tweets to return", min_value=10, max_value=100, value=100, step=10)

if search_query:
    # Search for tweets using the Cursor object
    tweets = tweepy.Cursor(api.search_tweets, q=search_query, tweet_mode='extended').items(num_tweets)

    # Classify tweets (count the number of tweets based on their classifications)
    positive_tweets_num = 0
    negative_tweets_num = 0
    neutral_tweets_num = 0
    # Classify tweets (save the actual tweets based on their classifications)
    positive_tweets = []
    negative_tweets = []
    neutral_tweets = []
    for tweet in tweets:
        tweet_text = tweet.full_text
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Classify the sentiment of this tweet: {tweet_text}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        if "positive" in response.lower():
            positive_tweets_num += 1
            positive_tweets.append((tweet_text, tweet.user.screen_name, response))
        elif "negative" in response.lower():
            negative_tweets_num += 1
            negative_tweets.append((tweet_text, tweet.user.screen_name, response))
        else:
            neutral_tweets_num += 1
            neutral_tweets.append((tweet_text, tweet.user.screen_name, response))


    # Display tweets and their sentiment
    st.write("Positive tweets:", positive_tweets_num)
    st.write("Negative tweets:", negative_tweets_num)
    st.write("Neutral tweets:", neutral_tweets_num)

    # Display sentiment percentages
    total_tweets = positive_tweets_num + negative_tweets_num + neutral_tweets_num
    positive_percent_num = positive_tweets_num / total_tweets * 100
    negative_percent_num = negative_tweets_num / total_tweets * 100
    neutral_percent_num = neutral_tweets_num / total_tweets * 100
    st.write("Positive percent: {:.2f}%".format(positive_percent_num))
    st.write("Negative percent: {:.2f}%".format(negative_percent_num))
    st.write("Neutral percent: {:.2f}%".format(neutral_percent_num))

    # Display columns for tweets
    st.header("Positive tweets")
    for tweet, author, score in positive_tweets:
        st.write("- " * 20)
        st.write("Author:", author)
        st.write(tweet)
        st.write("Score:", score)
        
    st.header("Negative tweets")
    for tweet, author, score in negative_tweets:
        st.write("- " * 20)
        st.write("Author:", author)
        st.write(tweet)
        st.write("Score:", score)

    st.header("Neutral tweets")
    for tweet, author, score in neutral_tweets:
        st.write("- " * 20)
        st.write("Author:", author)
        st.write(tweet)
        st.write("Score:", score)
