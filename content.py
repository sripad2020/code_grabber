from urllib.parse import  urlparse
import requests,nltk,re,heapq
from bs4 import BeautifulSoup
url='https://www.google.com/search?q='
inp=input('enter the query: ')
urls=[]
out_put=[]
final_links=[]
output=[]
last=[]
def search(inp):
    data=requests.get(url+f'{inp}').text
    soup=BeautifulSoup(data,'html.parser')
    for links in soup.find_all('a'):
        href=links.get('href')
        urls.append(href)
    for i in urls:
        clean_url =i.split('/url?q=')[1:]
        if len(clean_url) !=0 :
            out_put.append(clean_url)
    for i in out_put:
        for j in i:
            final_links.append(j)
    for j in final_links:
        if 'https://support.google.com' not in j and 'https://accounts.google.com' not in j and 'https://www.youtube.com/' not in j:
            if 'https://stackoverflow.com/' not in j:
                output.append(j)
search(inp)
for i in output:
    parse=urlparse(i)
    url = parse.path
    last_slash_index = url.rfind('/')
    sa_index = url.find('&sa')
    url_without_param = url[:sa_index]
    a='https://',parse.netloc,url_without_param
    url = ''.join(a)
    last.append(url)
print('The size of reference is  ',len(last),'pages')
print('ENTER THE OPTION: ')
print('1. new outputs ')
print('0. for exit')
while True:
    for j in last:
        inp = int(input('> '))
        if inp==1 :
            para = []
            output = []
            r = requests.get(j)
            data = r.text
            soup = BeautifulSoup(data, features='lxml')
            for link in soup.find_all('p'):
                    g = link.get_text()
                    token = nltk.tokenize.sent_tokenize(g)
                    para.append(token)
            output=sum(para,[])
            stri = ' '.join(map(str, output))
            text = stri.lower()
            clean = re.sub('[^a-zA-Z]', ' ', text)
            clean2 = re.sub('\s +', ' ', clean)
            sentence_list = nltk.sent_tokenize(text)
            stopwords = nltk.corpus.stopwords.words('english')
            word_frequencies = {}
            for word in nltk.word_tokenize(clean2):
                if word not in stopwords:
                    if word not in word_frequencies:
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            maximum_frequency = max(word_frequencies.values())
            for word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] / maximum_frequency
            sentence_scores = {}
            for sentence in sentence_list:
                for word in nltk.word_tokenize(sentence):
                    if word in word_frequencies and len(sentence.split(' ')) < 30:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = word_frequencies[word]
                        else:
                            sentence_scores[sentence] += word_frequencies[word]
            summary = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
            sentence = ''.join(summary)
            pr = re.sub('\n+', ' ', sentence)
            text_cleaned = re.sub('{*?}', '', pr)
            sd = re.sub("{.*?}", '', text_cleaned)
            cleaned = re.sub('\*?', '', sd)
            print(cleaned.upper())