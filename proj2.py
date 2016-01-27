
#main running file. All the procesure are running here
import math
from math import sqrt
import nltk
from index import make_invidx
from index import make_invidx_by_OkapiBM25
from index import make_index_AIG
from query import get_query
from query import calculate_query
from query import cosine_distance
from query import expand_query
from query import pivoted_length
from query import score
from query import sum_keyword
from storage import saveIndex
from storage import loadIndex
from evaluation import readFile
from evaluation import precision
from evaluation import recall
from evaluation import printEva
from evaluation import MAP
from evaluation import Avp
from index import make_invidx_by_OkapiBM251
from index import make_invidx_by_OkapiBM25s
from index import read_file
from queryExapnsion import TSV
from query import sum_score
from userFeedback import userFeedback
from userFeedback import coWeight
from userFeedback import selectTopTerm
from evaluation import readFile
from evaluation import precision
from evaluation import MRR
import time
#file="C://TweetStudy//12//12//00_00.dat"
queryAddress="C://TweetStudy//12//12//query.txt"
documentAddress="C://TweetStudy//12//12/2"
extend={"*.dat"}
#extend={"00*.dat","01*dat","02*dat","03*.dat","04*dat","05*.dat","06*.dat","07*dat","08*dat","09*.dat"}
#extend={"10*.dat","11*dat","12*dat","13*.dat","14*dat","15*.dat","16*.dat","17*dat","18*dat","19*.dat"}
#extend={"20*.dat","21*.dat","22*.dat","23*.dat"}
index = "C://TweetStudy//12//12//00_query.txt"
resultAddress="C://TweetStudy//12//12//relevantList.txt"
def get_k(queryAddress,documentAddress,e):
    document1, length_by_docid1 = make_invidx(documentAddress, e)
    query1=calculate_query(get_query(queryAddress))
    simi1= cosine_distance(document1,query1,100)
    result=readFile(resultAddress)
    for num in simi1:
        for weight1,docid in simi1[num]:
            if docid in result:
                print(docid)
     
def get_topK(queryAddress,documentAddress,extend):
    for e in extend:
        document1, length_by_docid1 = make_invidx(documentAddress, e)
        document2 = make_invidx_by_OkapiBM25(documentAddress, e)
        
        
#print(document)
#print(length_by_docid)
#saveIndex(index, (document, length_by_docid))
#document, length_by_docid = loadIndex(index)
#get query
        query1=calculate_query(get_query(queryAddress))
        for num in query1:
            document3= make_index_AIG(documentAddress,e,query1[num])
            simi3=sum_score(document3,10)
            simi2=sum_keyword(document2,query1[num],10)
        #print(simi)     
        #document= make_index_AIG(documentAddress,e,query1[num])
        simi1= cosine_distance(document1,query1,10)
       # simi=sum_keyword(document, query1[num],10)
#print(query1)
#cosine similarity
#simi=score(document,query1,10)
#simi= cosine_distance(document,query1,10)

    #print(simi)
        for num in simi1:
            for weight1,docid in simi1[num]:
            #print(docid)
                for weight2,docid2 in simi2:
                    if docid==docid2:
                        print(docid2," : ",weight2)
                for weight3,docid3 in simi3:
                    if docid==docid3:
                        print(docid3,":",weight3)
            for weight2,docid2 in simi2:
                for weight3,docid3 in simi3:
                    if docid2==docid3:
                        print(docid3,":",weight3)
#        print(num, docid, ":",weight)

def queryExpand1(document,extend,queryAddress):
    invx ,tf_by_docid,df,N= make_invidx_by_OkapiBM251(document, extend)
    query1=calculate_query(get_query(queryAddress))
    simi4={}
    for num in query1:
        simi=sum_keyword(invx,query1[num],20)
        termSelected=TSV(tf_by_docid,df,N,simi)
        #print(termSelected)
        invx1=make_invidx_by_OkapiBM25s(document, extend,termSelected)
        a= sorted([(termSelected[term], term) for term in termSelected], reverse=True)[:10]
        print(a)
        for weight,term in a:
            query1[num][term]=weight
        simi4=sum_keyword(invx1,query1[num],1000)
        #print(simi4)
    return simi4
def userLogExpan(extend,documentAddress,queryAddress):    
    ses=userFeedback("C://TweetStudy//12//12//userFeedback3.txt")
#    print(ses)
    ret={}
    for e in extend:
        document1, length_by_docid1 = make_invidx(documentAddress, e)
        tf,atid=read_file(documentAddress,e)
      #  query1=calculate_query(get_query(queryAddress))
        dic=get_query(queryAddress)
        for num in dic:
            re=coWeight(ses,nltk.word_tokenize(dic[num]),document1,tf,atid)
            ret=selectTopTerm(re,10)
    return ret
def evaluation(extend, documentAddress, queryAddress,resultAddress):
    result=readFile(resultAddress)
    #print(result)
    #tf-idf
    for e in extend:
#        document1, length_by_docid1 = make_invidx(documentAddress, e)
        query1=calculate_query(get_query(queryAddress))
 #       simi1= cosine_distance(document1,query1,1000)
        retrieval =0.0
        relevance=0.0
        document2 = make_invidx_by_OkapiBM25(documentAddress, e)
        for num in query1:
#            print("tf-idf: ")
 #           print(MRR(result, simi1[num]))
            #print(recall(result,simi1[num]))
#            document3= make_index_AIG(documentAddress,e,query1[num])
#            simi3=sum_score(document3,1000)
#            print("AIG: ")
#            print(MRR(result, simi3))
            #print(recall(result,simi3))
            simi2=sum_keyword(document2,query1[num],1000)
            print("BM25: ")
            print(MRR(result, simi2))
            #print(recall(result,simi2))
#        for num in simi1:
#            for weight1,docid in simi1[num]:
#            #print(docid)
#                for weight2,docid2 in simi2:
#                    if docid==docid2:
#                        retrieval = retrieval + 1
#                        if docid in result:
#                            relevance=relevance + 1
#    print(relevance/retrieval)
def queryExpanEva1(extend,documentAddress,queryAddress,resultAddress):
    for e in extend:
        sim4=queryExpand1(documentAddress,e,queryAddress)
        result=readFile(resultAddress)
        print("precision:")
        print(MRR(result, sim4))
      #  print("recall:")
      #  print(recall(result,sim4))
    
def queryExpanEva(extend,documentAddress,queryAddress,resultAddress):
    expandedTerm=userLogExpan(extend,documentAddress,queryAddress)
   # expandedTerm=queryExpand1(document,extend,queryAddress)
    print(expandedTerm)
    query1=calculate_query(get_query(queryAddress))
    result=readFile(resultAddress)
    for num in query1:
        for term in expandedTerm:
            query1[num][term]=query1[num].get(term,0) + 1
#print(query1)   
    for e in extend:
#        document1, length_by_docid1 = make_invidx(documentAddress, e)
#        simi1= cosine_distance(document1,query1,1000)
        document2 = make_invidx_by_OkapiBM25(documentAddress, e)
   # simi1= cosine_distance(document1,query1,50)
#    print(simi1)
        for num in query1:
#            print("tf-idf: ")
#            print(MRR(result, simi1[num]))
#            print(recall(result,simi1[num])) 
#            document3= make_index_AIG(documentAddress,e,query1[num])
 #           simi3=sum_score(document3,1000)
            simi2=sum_keyword(document2,query1[num],1000)
 #           print("AIG: ")
#            print(MRR(result, simi3))
#            print(recall(result,simi3))
            print("BM25: ")
            print(MRR(result, simi2))
#            print(recall(result,simi2))
            
#get_topK(queryAddress,documentAddress,extend)
#for e in extend:
#   queryExpand(documentAddress,e,queryAddress)
#get_k(queryAddress,documentAddress,extend)
evaluation(extend,documentAddress,queryAddress,resultAddress)
queryExpanEva(extend,documentAddress,queryAddress,resultAddress)
queryExpanEva1(extend,documentAddress,queryAddress,resultAddress)

documentAddress="C://TweetStudy//12//12//1"
evaluation(extend,documentAddress,queryAddress,resultAddress)
queryExpanEva(extend,documentAddress,queryAddress,resultAddress)
queryExpanEva1(extend,documentAddress,queryAddress,resultAddress)


