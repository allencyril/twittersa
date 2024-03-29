import streamlit as st
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
	        content:'Made by Ancy,Anju,Jini and Allen'; 
            visibility: visible;
	        display: block;
	        position: relative;
	        #background-color: red;
	        padding: 5px;
	        top: 2px;
            }</style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
import base64
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns


consumerKey = "SlsjzcIAIvCBB28yOfENAEKSw"
consumerSecret = "QfInAqeamF1VLkqT2RHbwLhJKGUDCVluEbBK4TJWQuZ3yTcKV4"
accessToken = "1364651022220632065-QA9DBsooYYgKBYWcvo7FrNtI5pzB6I"
accessTokenSecret = "biork7paK92ClMgFNHuS9Drl6VH2xWO1rAlPXS3dVui3q"

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)





def app():
    st.title("Twitter Sentiment Analyzer")

    activities = ["Tweet Analyzer", "Generate Twitter Data"]

    choice = st.sidebar.selectbox("Select Your Activity", activities)

    if choice == "Tweet Analyzer":        

        raw_text = st.text_area("Enter the exact twitter handle of the Personality (without @)")


        Analyzer_choice = st.selectbox("Select the Activities",
                                       ["Show Recent Tweets","Visualize the Sentiment Analysis"])

        if st.button("Analyze"):

            if Analyzer_choice == "Show Recent Tweets":

                st.success("Fetching last 5 Tweets")

                def Show_Recent_Tweets(raw_text):

                    # Extract 100 tweets from the twitter user
                    posts = api.user_timeline(screen_name=raw_text, count=100, lang="en", tweet_mode="extended")

                    def get_tweets():
                        l = []
                        i = 1
                        for tweet in posts[:5]:
                            l.append(tweet.full_text)
                            i = i + 1
                        return l

                    recent_tweets = get_tweets()
                    return recent_tweets

                recent_tweets = Show_Recent_Tweets(raw_text)

                st.write(recent_tweets)

            else:

                def Plot_Analysis():

                    st.success("Generating Visualisation for Sentiment Analysis")

                    posts = api.user_timeline(screen_name=raw_text, count=100, lang="en", tweet_mode="extended")

                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

                    # Create a function to clean the tweets
                    def cleanTxt(text):
                        text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
                        text = re.sub('#', '', text)  # Removing '#' hash tag
                        text = re.sub('RT[\s]+', '', text)  # Removing RT
                        text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink

                        return text

                    # Clean the tweets
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)

                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity

                    # Create a function to get the polarity
                    def getPolarity(text):
                        return TextBlob(text).sentiment.polarity

                    # Create two new columns 'Subjectivity' & 'Polarity'
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)

                    def getAnalysis(score):
                        if score < 0:
                            return 'Negative'
                        
                        else:
                            return 'Positive'

                    df['Analysis'] = df['Polarity'].apply(getAnalysis)

                    return df

                df = Plot_Analysis()

                st.write(sns.countplot(x=df["Analysis"], data=df))

                st.pyplot(use_container_width=True)





    else:

        st.subheader("This tool fetches the last 100 tweets from the twitter handle and analyse the polarity of each tweet")

        user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")


        def get_data(user_name):

            posts = api.user_timeline(screen_name=user_name, count=100, lang="en", tweet_mode="extended")

            df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

            def cleanTxt(text):
                text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
                text = re.sub('#', '', text)  # Removing '#' hash tag
                text = re.sub('RT[\s]+', '', text)  # Removing RT
                text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
                return text

            # Clean the tweets
            df['Tweets'] = df['Tweets'].apply(cleanTxt)


            # Create a function to get the polarity
            def getPolarity(text):
                return TextBlob(text).sentiment.polarity

            
            
            df2= df['Tweets'].apply(getPolarity)
            

            def getAnalysis(score):
                if score < 0:
                    return 'Negative'

                
                else:
                    return 'Positive'
             

            df['Analysis'] = df2.apply(getAnalysis)
            return df

        if st.button("Show Data"):
            st.success("Fetching Last 100 Tweets")

            df = get_data(user_name)

            st.write(df)



st.set_option('deprecation.showPyplotGlobalUse', False)
if __name__ == "__main__":
    app()
