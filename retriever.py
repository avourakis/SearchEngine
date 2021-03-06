import mmap
import os
import re
import csv
import serialization as sr
import json
import math
from tkinter import *

def extract_index(file_name):
    print('Loading Inverted Index... \n')
    inverted_index = sr.extract_index(file_name)
    print('Inverted Index has been loaded \n')
    return inverted_index

def user_input():
    
    #Window
    master = Tk()
    master.title("Search Engine")
    #master.pack(fill=BOTH, expand=1)
    master.geometry("500x300")

    #Logo
    path = "Noodle1.gif"
    img = PhotoImage(file=path)
    panel = Label(master, image=img)
    panel.place(x=170,y=80)
    
    #Search Form
    query = Entry(master)
    query.place(x= 160, y = 150)
    
    #Button
    search_button = Button(master, text = "Search", command=lambda q=query: retrieve(query.get()))
    search_button.place(x =200, y = 190)

    
    master.mainloop()

def retrieve(query):

    # tsv = open('C:\SCHOOL\INF 141\SearchEngine\WEBPAGES_CLEAN\\bookkeeping.tsv')
    file_name = 'inverted_index.pickle'
    inverted_index = extract_index(file_name)

    try:
        user_query = str(query) #computer science
        queries = user_query.split() #[computer, science]

        stop_words = ('a', 'around', 'and', 'every', 'for', 'from', 'in' \
                  'is', 'it', 'not', 'on', 'one', 'the', 'to', 'under')

        N = 37497

        ranking_dict = dict()

        for query in queries:
            if query not in stop_words:
                for doc in inverted_index[query]:
                    d = doc.docID
                    dl= [str(x) for x in re.findall(r'\b\d+\b', d)]
                    docid = dl[0] + '/' + dl[1]

                    tf_idf = 1 + math.log(doc.term_frequency) #term frequency adjustment
                    tf_idf += math.log(N/len(inverted_index[query])) #inverted document frequency adjustment
                    #print(tf_idf)
                    tf_idf += doc.special

                    if docid in ranking_dict:
                        ranking_dict[docid] += tf_idf
                    else:
                        ranking_dict[docid] = tf_idf

        ranking_dict = sorted(ranking_dict.items(), key = lambda x : (-x[1] , x[0]))

        result_urls = []

        with open('C:\SCHOOL\INF 141\SearchEngine\WEBPAGES_CLEAN\\bookkeeping.json') as json_data:
            jd = json.load(json_data)
            for (key,value) in ranking_dict:
                result_urls.append(jd[key])

        for url in result_urls:
            print(url)
    except:
        print("that word was not found")
        pass

if __name__ == "__main__":
    #retrieve()
    user_input()

