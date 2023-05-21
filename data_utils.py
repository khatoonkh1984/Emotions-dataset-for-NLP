import os
import re
import csv
import spacy
import pickle
from glob import glob
from tqdm import tqdm

import torch
from torch.utils.data import Dataset


NLP = spacy.load('en_core_web_sm')


def covert_dataframe_to_devided_folder(input_folder, output_folder):
    files =[]
    with open(input_folder, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(csv_reader):
            tweet_text = row[0]  # assuming the tweet text is in the first column
            emotion = row[1]  # assuming the label is in the second column

            if emotion not in files:
                files.append(emotion)
                # If not, create a new file object with write mode and store it in the dictionary
                subfolder = output_folder + "/" + emotion 
                # Create the subfolder if it does not exist
                os.makedirs(subfolder, exist_ok=True)
                # Define the output file name based on the tweet
                output_file = subfolder + "/" + f"{emotion}_{idx}.txt" 
                     #with open(output_file, 'w') as f:
                    #file_name = f"{emotion}_{idx}.txt"  # create a file name that includes the label and index
                   # Open the output file in write mode
                with open(output_file, "w") as output_txt:
                    # Write the tweet to the output file
                    output_txt.write(tweet_text)
            else:
                subfolder = output_folder + "/" + emotion 
                # Create the subfolder if it does not exist
                os.makedirs(subfolder, exist_ok=True)
                # Define the output file name based on the tweet
                output_file = subfolder + "/" + f"{emotion}_{idx}.txt" 
                     #with open(output_file, 'w') as f:
                    #file_name = f"{emotion}_{idx}.txt"  # create a file name that includes the label and index
                   # Open the output file in write mode
                with open(output_file, "w") as output_txt:
                    # Write the tweet to the output file
                    output_txt.write(tweet_text)
                    
                    

def tokenizer(text):
    text = re.sub(r"[\*\"“”\n\\…\+\-\/\=\(\)‘•:\[\]\|’;]", " ", str(text))
    text = re.sub(r"[ ]+", " ", text)
    text = re.sub(r"\!+", "!", text)
    text = re.sub(r"\,+", ",", text)
    text = re.sub(r"\?+", "?", text)
    return [x.text for x in NLP.tokenizer(text) if x.text != " "]


class Vocabulary(object):
    
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.word2index = {}
        self.word2count = {}
        self.index2word = {}
        self.count = 0
    
    def add_word(self, word):
        if not word in self.word2index:
            self.word2index[word] = self.count
            self.word2count[word] = 1
            self.index2word[self.count] = word
            self.count += 1
        else:
            self.word2count[word] += 1
    
    def add_sentence(self, sentence):
        for word in self.tokenizer(sentence):
            self.add_word(word)
            
    def __len__(self):
        return self.count

    
    
if __name__ == '__main__':
    pass
