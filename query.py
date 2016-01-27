from nltk.corpus import wordnet
import re
import math
from parser1 import parseTokensFromText
def get_query(document):
    fin=open(document)
    query = re.findall(r'<num> Number: (\d+)\n\n<title> (.+)',fin.read())
    fin.close()
    dic={num:title for num, title in query}
    return dic
def calculate_query(dic):
    query_by_number={}
    for num in sorted(dic.keys()):
        parsedQuery=parseTokensFromText(dic[num])
       # if qe == 1:
       #     query=wordNet(parsedQuery)
        query=parsedQuery
#        print(parsedQuery) didn't record every query's term frequency
        query_by_number[num]=qf={}
        for term in query:
        #for term in parsedQuery:
            qf[term]= qf.get(term,0) + 1
        for term in query:
            qf[term]=math.log(qf[term]+1) 
    return query_by_number
def sum_score(document,k):
    s={}
    for term in document:
        for docid in document[term]:
               # print(term,docid)
                if docid in s:
                    s[docid]=s[docid]+document[term][docid]
                else:
                    s[docid]=document[term][docid]
    return sorted([(s[docid], docid) for docid in s], reverse=True)[:k]

def sum_keyword(document,query,k):
    s={}
    for term in document:
        if term in query:
            for docid in document[term]:
               # print(term,docid)
                    if docid in s:
                        s[docid]=s[docid]+document[term][docid]
                    else:
                        s[docid]=document[term][docid]
    return sorted([(s[docid], docid) for docid in s], reverse=True)[:k]
#def DiceScore(dic,df):
#        query_by_number={}
#    for num in sorted(dic.keys()):
#        parsedQuery=parseTokensFromText(dic[num])
#       # if qe == 1:
       #     query=wordNet(parsedQuery)
 #       query=parsedQuery
#        print(parsedQuery) didn't record every query's term frequency
#        query_by_number[num]=qf={}
#        for term in query:
            
    
def pivoted_length(document, length_by_docid,avg_length,query,k,sl):
    simi={}
    for num in sorted(query.keys()):
        s = {}
        for term in query[num]:
            for docid in document.get(term,{}):
        #        print(num,docid)
                if docid in s:
                    s[docid]=s[docid]+query[num][term]*document[term][docid]
                else:
                    s[docid]=query[num][term]*document[term][docid]
        for docid in s:
            s[docid]=s[docid]/float(avg_length/length_by_docid[docid]*(1-sl)+ sl)
        simi[num] = sorted([(s[docid], docid) for docid in s], reverse=True)[:k]
    return simi

def cosine_distance(document, query,k):
    simi={}
    for num in sorted(query.keys()):
        s = {}
        for term in query[num]:
            for docid in document.get(term,{}):
        #        print(num,docid)
                if docid in s:
                    s[docid]=s[docid]+query[num][term]*document[term][docid]
                else:
                    s[docid]=query[num][term]*document[term][docid]
        simi[num] = sorted([(s[docid], docid) for docid in s], reverse=True)[:k]
    return simi
def score(document,query,k):
    simi={}
    for num in sorted(query.keys()):
        s = {}
        for term in query[num]:
            for docid in document.get(term,{}):
        #        print(num,docid)
                if docid in s:
                    s[docid]=s[docid]+document[term][docid]
                else:
                    s[docid]=document[term][docid]
        simi[num] = sorted([(s[docid], docid) for docid in s], reverse=True)[:k]
    return simi
def wordNet(query):
 #   print(query)
    newQuery=[]
    for word in query:
        newQuery.append(word)
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                newQuery.append(lemma.name())
  #  print(newQuery)
    return newQuery

# calculate dot product for two vectors
def dot_product(vec_1, vec_2):
    return sum([vec_1[t]*vec_2[t] for t in vec_1 if t in vec_2])

# query expansion function, return expanded query
# 1. sum all query-term vectors to query_vec
# 2. calculate similarity between query_vec and other term vectors
#    save as result list [(simi, term)] and sort decreasingly
# 3. calculate average weight of query and
#              average similarity of top-k terms in result
# 4. add top-k terms into query with rescaled similarities as weights
#    similarities are rescaled by multiplying a factor in order to
#    make the average weight of query doesn't change
def expand_query(pstinv, query, k):
    query_vec = {}
    for num in query:
        query_vec[num]=q={}
        for term in query[num]:
            for docid in pstinv.get(term, {}):
                q[docid] = q.get(docid, 0) + pstinv[term][docid]
               # print('qDoc',q[docid])
        result = sorted([(dot_product(q, pstinv[term]), term) \
                     for term in pstinv if term not in query[num]], reverse=True)
        #print(result)
        avg_qry_weight = sum(query[num].values()) / len(query[num])
      #  print('average query weight',avg_qry_weight)
        avg_exp_weight = sum([simi for (simi, term) in result[:k]]) / k
      #  print('average_exp_weight',avg_exp_weight)
        for (simi, term) in result[:k]:
            query[num][term] = simi * (avg_qry_weight / avg_exp_weight)
    return query
