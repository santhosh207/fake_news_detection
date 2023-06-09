import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import re
import string

def make_prediction(text1):
    df_fake = pd.read_csv("Fake.csv")
    df_true = pd.read_csv("True.csv")
    df_fake["class"] = 0
    df_true["class"] = 1
    for i in range(23480, 23470, -1):
        df_fake.drop([i], axis=0, inplace=True)
    for i in range(21416, 21406, -1):
        df_true.drop([i], axis=0, inplace=True)
    df_marge = pd.concat([df_fake, df_true], axis=0)
    df = df_marge.drop(["title", "subject", "date"], axis=1)
    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W", " ", text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    df["text"] = df["text"].apply(wordopt)
    x = df["text"]
    y = df["class"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)
    from sklearn.linear_model import LogisticRegression
    LR = LogisticRegression()
    LR.fit(xv_train, y_train)
    pred_lr = LR.predict(xv_test)

    def output_lable(n):
        if n == 0:
            return "Fake News"
        elif n == 1:
            return "Not A Fake News"

    def manual_testing(news):
        testing_news = {"text": [news]}
        new_def_test = pd.DataFrame(testing_news)
        new_def_test["text"] = new_def_test["text"].apply(wordopt)
        new_x_test = new_def_test["text"]
        new_xv_test = vectorization.transform(new_x_test)
        pred_LR = LR.predict(new_xv_test)

        return print("\n\nLR Prediction: {}".format(output_lable(pred_LR[0])))

    manual_testing(text1)

make_prediction('hello how are you')