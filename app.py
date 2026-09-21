import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(Text):
    Text = Text.lower()
    # tokenization
    Text = nltk.word_tokenize(Text)
    # Remove Special Characters (englih ya Alphanumeric)
    y = []
    for i in Text:
        if i.isalnum():
            y.append(i)

    Text = y[:]
    # upar jo kiya hai uska mtlb ye hai ki list ko aap kabhi bhi aise assign nhi kr skte kyuki list is mutable so we need to clone and assign like this
    y.clear()
    # remove stop words (jinka sentence formation me mtlb hota hai lkn genrealy meaning nhi hota is, are, etc)

    for i in Text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    Text = y[:]
    # further process of stemming
    y.clear()

    for i in Text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")

