#code finished, need testing
#Probabilistic Query Expansion Using Query Logs
import math
#read user feedback data
def userFeedback(file):
    session={}
    f=open(file,'r')
    for line in f:
        l=line.split(" ")
        session[l[0]]=l[1:]
    return session
# calculate log-based query expansion enter a query and evaluate by historical query text
def coWeight(session,query,document,tf,atid):
    fWD={}
    fW={}
    w={}
    maxW=0
    pDW={}
    for text in session:
        for docid in session[text]:
            if docid in tf:
                pDW[docid]={}
    re={}
    pWD={}
    pWW={}
    count=0.0
    rtNum=1.0
    #get fWD,fW, w and maxW
    for word in query:
            for text in session:
                if word in text:
                    fW[word]=fW.get(word,0)+1
                    fWD[word]=f={}
                    for docid in session[text]:
                        if docid in tf:
                            f[docid]=f.get(docid,0)+1
                    for docid in session[text]:
                        if docid in tf:
                            pDW[docid][word]=fWD[word][docid]/fW[word]
                            
    
    for docid in pDW:
        for term in tf[docid]:
            pWD[term]={}
    
    for docid in pDW:
        maxW = sorted(tf[docid].values())[0]
     #   for term  in tf[docid]:
     #       if term in query and  docid in atid :
     #           count=count+1
           # if term=='rt':
           #     rtNum=rtNum+1
        for term in tf[docid]:
           # if "rt" in tf[docid]:
            pWD[term][docid]=tf[docid][term]/maxW
           # pWD[term][docid]=tf[docid][term]*(1+count*float(tf[docid][term])/len(tf[docid]))/maxW
        count=0.0
        rtNum=1.0    
    for term in pWD:
        pWW[term]=t={}
        for docid in pWD[term]:
            for word in pDW[docid]:
                t[word]=t.get(word,0)+pDW[docid][word]*pWD[term][docid]
#    print(pWW)
    for term in pWW:
        for word in pWW[term]:
            if term in re:
                re[term]=re[term]*(pWW[term][word]+1)
            else:
                re[term]=pWW[term][word]+1
    for term in re:
        re[term]=math.log(re[term])

    return re

# select top-k term according to its value
def selectTopTerm(re,k):
    res={}
    topTerm={}
    for term in re:
        res[re[term]]=term
    for weight in sorted(res)[:k]:
        topTerm[res[weight]]=1
    return topTerm

