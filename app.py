from flask import Flask, render_template, request
from collections import defaultdict 
import requests 
import re
import json

app = Flask(__name__)

stopwords = ['','a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist,wordfreq)))

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

def validation(enteredRadio, flag, wordCount):
    value = 'true'
    if enteredRadio == 'passage':
        if not request.form['chapter'] or request.form['chapter'] == '0':
            value = 'false'
    if not flag or flag == 'OT' or flag == 'NT':
        value = 'false'
    if not wordCount:
        value = 'false'
    return value

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        
        #print(request.form)
        flag=request.form["book"]
        wordCount=int(request.form["wCount"])
        enteredRadio=request.form['userRadios']

        if validation(enteredRadio, flag, wordCount) == 'false':
            value = ''
            if enteredRadio == 'passage':
                if not request.form['chapter']:
                    value = ''
                else:
                    value = request.form['chapter']

            return render_template('index.html', words='true', verses='true', book=flag, wordC=wordCount, chapt=value, error='true')
        else:
            #https://getbible.net/json?p=Proverbs
            URL = "http://getbible.net/json"
            
            # defining a params dict for the parameters to be sent to the API 
            if(request.form['userRadios']=='passage'):
                PARAMS = {'p':flag+""+request.form['chapter'], 'v': 'web'}
            else:
                PARAMS = {'p':flag, 'v': 'web'} 
            
            #print(PARAMS)
            # sending get request and saving the response as response object 
            r = requests.get(url = URL, params = PARAMS) 
            #print('!!'+r.text+'!!')
            if r.text == 'NULL':
                print('yes!!')
                return render_template('index.html', words='true', verses='true', book=flag, wordC=wordCount, chapt=request.form['chapter'], error='true')
            else:
                # extracting data in json format 
                data1 = r.text
                
                # returns JSON object as a dictionary
                data = json.loads(data1[1:len(data1)-2]);

                chaptr=300
                #get verses of the entire book
                #print(data[data['type']])
                if data['type']=='book':
                    book = data['book'];
                    
                    verses='';
                    for i in book:#chapters
                        for j in book[str(i)]['chapter']:#verses
                            verses += book[str(i)]['chapter'][str(j)]['verse'][:-2];

                if data['type']=='chapter':
                    book = data['chapter'];
                    chaptr=data['chapter_nr'];
                    verses='';
                    for j in book:#verses
                        verses += book[str(j)]['verse'][:-2];
                        #print(book[str(j)]['verse'])
                            

                #"!?:;,.
                fullwordlist = re.split(r'[".,?;!:\(\)\s]\s*', verses.lower());
                wordlist = removeStopwords(fullwordlist, stopwords)
                dictionary = wordListToFreqDict(wordlist)
                sorteddict = sortFreqDict(dictionary)

                jsonString='{"words": {'
                frequentSet=set()
                for s in sorteddict[:wordCount]:
                    jsonString+='"'+str(s[1])+'":"'+str(s[0])+'",'
                    frequentSet.add(str(s[1]))

                jsonString=jsonString[:len(jsonString)-1]+"}}"

                jsonObject=json.loads(jsonString)

                verse='';
                verseTable=defaultdict(list)
                if data['type']=='book':
                    for i in book:#chapters
                        for j in book[str(i)]['chapter']:#verses
                            verse = book[str(i)]['chapter'][str(j)]['verse'][:-2];
                            vWordList=re.split(r'[".,?;!:\(\)\s]\s*', verse.lower());
                            intersect=frequentSet.intersection(set(vWordList))
                            if len(intersect)>0:
                                for key in intersect:
                                    verseTable[key].append(verse+"#"+str(i)+":"+str(j))
                
                if data['type']=='chapter':
                    for j in book:#verses
                        verse = book[str(j)]['verse'][:-2];
                        vWordList=re.split(r'[".,?;!:\(\)\s]\s*', verse.lower());
                        intersect=frequentSet.intersection(set(vWordList))
                        if len(intersect)>0:
                            for key in intersect:
                                verseTable[key].append(verse+"#"+str(data["chapter_nr"])+":"+str(j))

                return render_template('index.html', words=jsonString, verses=json.dumps(verseTable), book=flag, wordC=wordCount, chapt=chaptr, error='false')
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)