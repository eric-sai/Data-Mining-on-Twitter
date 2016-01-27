import glob
import os
import re
import math
from parser1 import parseTokensFromText
import json
import nltk
def read_file(document,extend):
        tf_by_docid={}
        atid={}
        os.chdir(document)
        for file in glob.glob(extend):
                f=open(file,'r', encoding='utf-8',errors='ignore')
                for line in f:
                        line_object=json.loads(line)
                        tweet_text = line_object['text']
                    #    if '#' in tweet_text:
                    #            atid= file+ line_object['id_str']
                        text=re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet_text)
                      #  text = re.sub(r"@\S+", "",text)
                  #      print(text)
                        tweet_id =file + line_object['id_str']
                        parsedTokenList=parseTokensFromText(text)
                       # only consider nouns
                    #    parsedTokenList=nltk.pos_tag(parseTokensFromText(text))
                       # print(parsedTokenList)
                        tf_by_docid[tweet_id]=tf={}
                        for term in parsedTokenList:
                    #            if term[1]=='NN':
                                tf[term]=tf.get(term, 0) + 1
      #  print(tf_by_docid)
        return tf_by_docid,atid

def calculate_df(tf_by_docid):
    df = {}
    for docid in tf_by_docid:
        for term in tf_by_docid[docid]:
            df[term] = df.get(term, 0) + 1
    return df
def cal_avel(tf_by_docid,N):
        avel=0.0
        for docid in tf_by_docid:
                avel=avel+len(tf_by_docid[docid])
        avel=avel/N
        return avel
def AIG(tf_by_docid,query):
        df={}
        df1={}
        for docid in tf_by_docid:
                for term1 in query:
                        if term1 in tf_by_docid[docid]:
                                df1[term1]=ddf={}
                                for term2 in tf_by_docid[docid]:
                                        df[term2]=df.get(term2,0)+1
                                        if term1 != term2:
                                                ddf[term2]=ddf.get(term2,0)+1
                        else:
                                for term2 in tf_by_docid[docid]:
                                        df[term2]=df.get(term2,0)+1
        return df,df1
def calculate_Dice(df,df1,query, N):
        ret={}
        for term1 in query:
                if term1 in df1:
                        for term2 in df1[term]:
                                ret[term2]= ret.get(term2,0)+ 2*df1[term1][term2]/(df[term1]+df[term2])
        return ret
def calculate_Jaccard(df,df1,query,N):
        ret = {}
        for term1 in query:
                if term1 in df1:
                        for term2 in df1[term]:
                                ret[term2]=ret.get(term2,0)+df1[term1][term2]/(df[term1]+df[term2]-df1[term1][term2])
        return ret                        
def calculate_okapiBM25(tf,df,N,avel):
        return {term : ((tf[term]*(1.2+1))* math.log((float(N)-df[term]+0.5)/(df[term]+0.5))/(tf[term]+1.2*(1-0.75+(0.75*len(tf)/avel))))\
                for term in tf}

def calculate_okapiBM25s(tf,df,tsv,R,N):
        tfidf={}
        for term in tf:
                if term in tsv:
                        tfidf[term]=((tf[term]*(1.2+1))* float(1/3)*math.log(((tsv[term]+0.5)/(R-tsv[term]))/((df[term]-tsv[term]+0.5)/(N-df[term]-R+tsv[term]+0.5))))
                else:
                        tfidf[term]=0.0
        return tfidf

def calculate_tfidf(tf, df, N):
        return {term : math.log(tf[term]+1) * math.log(float(N)/df[term])\
                for term in tf}
def calculate_AIG(df,df1,query,N):
        ret={}
        for term1 in query:
                if term1 in df1:
                        for term2 in df1[term1]:
                                ret[term2]=ret.get(term2,0)+math.log(1+N*(df1[term1][term2]/(df[term1]*df[term2])))
        return ret
def make_invidx_by_OkapiBM25s(document, extend,tsv):
        tf_by_docid,atid = read_file(document,extend)
        df, N = calculate_df(tf_by_docid), len(tf_by_docid)
        invidx= {term : {} for term in df}
        R= len(tsv)
        for docid in tf_by_docid:
                tfidf = calculate_okapiBM25s(tf_by_docid[docid], df,tsv,R,N)
                for term in tfidf:
                        invidx[term][docid]=tfidf[term]
                
        return invidx
        
                        
def make_index_AIG(document,extend,query):
        invidx={}
        tf_by_docid,atid=read_file(document,extend)
        df,df1=AIG(tf_by_docid,query)
       # print("df",df)
       # print("df1",df1)
        N=len(tf_by_docid)
        score=calculate_AIG(df,df1,query,N)
       # print("score",score)
        for term in score:
                invidx[term]={}
        for docid in tf_by_docid:
                for term in tf_by_docid[docid]:
                        if term in score:
                                invidx[term][docid]=score[term]
                            #print(invidx[term][docid])
        return invidx
                
def make_invidx(document, extend):
    tf_by_docid,atid = read_file(document,extend)
   # print(tf_by_docid)
    df, N = calculate_df(tf_by_docid), len(tf_by_docid)
   # print(df,N)
    invidx, length_by_docid = {term : {} for term in df}, {}
    
    for docid in tf_by_docid:
        tfidf = calculate_tfidf(tf_by_docid[docid], df, N)
       # print(tfidf)
        length = length_by_docid[docid] = \
                 math.sqrt(sum([value**2 for value in tfidf.values()]))
        for term in tfidf:
            invidx[term][docid] = tfidf[term] / length

    return invidx, length_by_docid
def make_invidx_by_OkapiBM25(document,extend):
        tf_by_docid,atid = read_file(document,extend)
        df, N = calculate_df(tf_by_docid), len(tf_by_docid)
        invidx, length_by_docid = {term : {} for term in df}, {}
        avel=cal_avel(tf_by_docid,N)
        for docid in tf_by_docid:
                tfidf = calculate_okapiBM25(tf_by_docid[docid], df, N,avel)
                for term in tfidf:
                        invidx[term][docid]=tfidf[term]
        return invidx
def make_invidx_by_OkapiBM251(document,extend):
        tf_by_docid,atid = read_file(document,extend)
        df, N = calculate_df(tf_by_docid), len(tf_by_docid)
        invidx, length_by_docid = {term : {} for term in df}, {}
        avel=cal_avel(tf_by_docid,N)
        for docid in tf_by_docid:
                tfidf = calculate_okapiBM25(tf_by_docid[docid], df, N,avel)
                for term in tfidf:
                        invidx[term][docid]=tfidf[term]
        return invidx,tf_by_docid,df,N
