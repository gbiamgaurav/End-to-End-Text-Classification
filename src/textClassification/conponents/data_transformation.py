
import os, sys
import pandas as pd
import nltk
import re
import string
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
nltk.download('stopwords')
from textClassification.entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.stemmer = nltk.SnowballStemmer("english")
        self.stopword = set(stopwords.words('english'))

    
    # Let's apply regex and do cleaning.
    def data_cleaning(self,words):
        words = str(words).lower()
        words = re.sub('\[.*?\]', '', words)
        words = re.sub('https?://\S+|www\.\S+', '', words)
        words = re.sub('<.*?>+', '', words)
        words = re.sub('[%s]' % re.escape(string.punctuation), '', words)
        words = re.sub('\n', '', words)
        words = re.sub('\w*\d\w*', '', words)
        words = [word for word in words.split(' ') if words not in self.stopword]
        words=" ".join(words)
        words = [self.stemmer.stem(words) for word in words.split(' ')]
        words=" ".join(words)

        return words
    

    def clean_and_transform(self):

        data = pd.read_csv(os.path.join(self.config.data_path,"data.csv"))
        
        data["Sentiment"].replace({'neutral':0},inplace=True)
        data["Sentiment"].replace({'positive':1}, inplace = True)
        data["Sentiment"].replace({'negative':2}, inplace = True)
        
        data['Sentence'] = data['Sentence'].apply(self.data_cleaning)

        data.to_csv(os.path.join(self.config.root_dir,'main_df.csv'), index=False)