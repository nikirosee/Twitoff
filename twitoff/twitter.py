"""Retrieve and requests tweets from the DS API"""
import requests
import spacy
from .models import DB, Tweet, User


nlp = spacy.load("my_model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


# Add and updates tweets
def add_or_update_user(username):
    """
    Adds and updates the user with twitter handle 'username'
    to our database
    """
    # TODO: Figure out how to properly update users when the update route is visited
    try:
        r = requests.get(
            f"https://lambda-ds-twit-assist.herokuapp.com/user/{username}")
        user = r.json()
        user_id = user["twitter_handle"]["id"]

        # This either resepectively grabs or creates a user for our db
        db_user = (User.query.get(user_id)) or User(id=user_id, name=username)
        # This adds the db_user to our database
        DB.session.add(db_user)

        tweets = user["tweets"]
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet["full_text"])
            db_tweet = Tweet(
                id=tweet["id"], text=tweet["full_text"], vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()