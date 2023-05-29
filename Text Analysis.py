#!/usr/bin/env python
# coding: utf-8

# In[1]:


with open(r"C:\Users\deves\Desktop\BlackCoffer_assignment\MasterDictionary\positive-words.txt", 'r') as f:
    text = f.read()
positive_words = text.split()
with open(r"C:\Users\deves\Desktop\BlackCoffer_assignment\MasterDictionary\negative-words.txt", 'r') as t:
    text = t.read()
negative_words = text.split()


# In[2]:


import glob
stop_words = []
for filename in glob.glob(r"C:\Users\deves\Desktop\BlackCoffer_assignment\StopWords\*.txt"):
    with open(filename, 'r') as f:
        sw = f.read()
        stop_words.append(sw.split())


# In[3]:


for i in positive_words:
    if i in stop_words:
        positive_words.remove(i)
for i in negative_words:
    if i in stop_words:
        negative_words.remove(i)


# In[4]:


positive_negative_dictionary = {
    "positive": positive_words,
    "negative": negative_words,
}


# In[5]:


import re
def word_length(text):

    words = text.split()
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    return total_characters / total_words

def personal_pronouns(text):
    
    matches = re.findall(r'\b(I|i|We|My|Ours|we|my|ours|us|(?-i:us))\b', text)
    return len(matches)

def count_syllables(word):
    num_vowels = len(re.findall(r'[aeiou]', word))
    if re.search(r'[aeiou]$', word):
        num_vowels += 1
    if re.search(r'[bcdfghjklmnpqrstvwxyz]+$', word):
        num_vowels -= 1
    if re.search(r'(es|ed)$', word):
        num_vowels -= 1
    return num_vowels

def get_sentences(text):
    global sentences   
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence for sentence in sentences if sentence]
    return sentences

def get_average_sentence_length(text):
  
    number_of_sentences = len(get_sentences(text))
    number_of_words = len(text.split())
    average_sentence_length = number_of_words / number_of_sentences
    return average_sentence_length

def get_average_number_of_words_per_sentence(text):
    
    number_of_sentences = len(get_sentences(text))
    number_of_words = len(text.split())
    number_of_sentences_with_at_least_one_word = len([sentence for sentence in sentences if sentence])
    average_number_of_words_per_sentence = number_of_words / number_of_sentences_with_at_least_one_word
    return average_number_of_words_per_sentence


# In[6]:


import pandas as pd
columns = ["URL_ID", "Positive Score", "Negative Score", "Polarity score", "Subjectivity score", "Avg sentence length", "Percentage of complex words", "Fog index", "Avg number of words per sentence", "Complex word count", "Word count", "Syllable per word", "Personal pronouns", "Avg word length"]
df = pd.DataFrame(columns=columns)


# In[7]:


import glob
import nltk
import re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
for filename in glob.glob(r"C:\Users\deves\Desktop\BlackCoffer_assignment\scrape_data\*.txt"):
    with open(filename, 'r',encoding="utf-8") as f:
        data = f.read()
        URL_ID = re.findall("\d+", filename)[0]
        
        
        average_number_of_words_per_sentence = get_average_number_of_words_per_sentence(data)
        average_sentence_length = get_average_sentence_length(data)
        sentence = []
        sentences = nltk.sent_tokenize(data)
        for i in range(len(sentences)):
            review=re.sub('[^a-zA-Z]',' ',sentences[i])
            review=review.lower()
            review=review.split()
            review=[lemmatizer.lemmatize(word) for word in review if not word in stop_words] 
            review = " ".join(review)
            sentence.append(review)
        total_words = 0
        total_complex = 0
        positive_score = 0
        negative_score = 0
        for i in sentence:
            words = i.split()
            total_words += len(words)
            for j in i.split(" "):
                if count_syllables(j)>2:
                    total_complex += 1 
                if j in positive_negative_dictionary['positive']:
                    positive_score += 1
                elif j in positive_negative_dictionary['negative']: 
                    negative_score -=1
        Subjectivity_Score = abs((positive_score + negative_score)/ ((total_words) + 0.000001))  
        polarity_score = (positive_score + negative_score) / (positive_score - negative_score) + 0.000001
        percentage_of_complex = (total_complex / total_words) 
        fog_index = 0.4 * (average_sentence_length + percentage_of_complex) 
        Personal_pronouns=personal_pronouns(data)
        Avg_word_length=word_length(data) 
        word = data.split()
        count=[count_syllables(i) for i in words]
       
        Syllable_per_word=sum(count)
        df = df.append({
            'URL_ID': URL_ID ,
            'Avg number of words per sentence': average_number_of_words_per_sentence,
             "Positive Score":positive_score,
            "Negative Score":negative_score, 
            "Polarity score" : polarity_score,
            "Subjectivity score":Subjectivity_Score, 
            "Avg sentence length":average_sentence_length, 
            "Percentage of complex words":percentage_of_complex , 
            "Fog index":fog_index, 
            "Avg number of words per sentence":average_number_of_words_per_sentence,
            "Complex word count":total_complex, 
            "Word count": total_words,
            "Personal pronouns":Personal_pronouns,
            "Avg word length":Avg_word_length,
            "Syllable per word":Syllable_per_word
            },ignore_index=True)


# In[8]:


df.head()


# In[9]:


df.info()


# In[10]:


df['URL_ID'] = df['URL_ID'].astype('int64')


# In[11]:


df_input = pd.read_excel(r"C:\Users\deves\Desktop\BlackCoffer_assignment\Input.xlsx")


# In[12]:


df_input.info()


# In[13]:


merged_df = pd.merge(df, df_input, on='URL_ID')


# In[14]:


desired_order = ["URL_ID","URL","Positive Score", "Negative Score", "Polarity score", "Subjectivity score", "Avg sentence length", "Percentage of complex words", "Fog index", "Avg number of words per sentence", "Complex word count", "Word count", "Syllable per word", "Personal pronouns", "Avg word length"]


# In[15]:


merged_df = merged_df.reindex(columns=desired_order)


# In[16]:


merged_df


# In[18]:


merged_df = merged_df.sort_values(by='URL_ID')


# In[19]:


merged_df.to_excel("Output.xlsx",index = False)


# In[20]:


merged_df


# In[ ]:




