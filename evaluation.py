#read result 
def readFile(resultAddress):
    file=open(resultAddress)
    lines=file.readlines()
    file.close()
    result={}
    for line in lines:
        l=line[:-1]
        result[l]=l
         #   print(result[resultList[0]])
    return result

def precision(result, simi):
    precisionList={}
    relevance=0
    retrieval=0
    for weight,docid in simi:
        retrieval=retrieval + 1
        if docid in result:
                relevance=relevance + 1
                 #   print(relevance)
    print(relevance)
    print(retrieval)
    if retrieval != 0:
        precisionList=float (relevance)/retrieval
    else:
        precisionList=0.0
    return precisionList

def recall(result, simi):
    recallList={}
    count=len(result)
    relevance=0
    for weight,docid in simi:
        if docid in result:
            relevance=relevance + 1            
    recallList=float(relevance)/count
    return recallList                
def MRR(result,simi):
    rank = 0.0
    recall=0.0
    rate=0.0
    for weight,docid in sorted(simi):
        rank=rank+1
        if docid in result:
            return rank
#            recall = recall +1
#            rate=recall/rank+rate
#        if recall == 2:
#            return rate/2.0
#    while recall < 2.0:
#        rank=rank+1
#        recall=recall+1
#        rate = recall/rank+rate
    return rank
#    return rate
def printEva(eva):
    for num in sorted(eva.keys()):
        print(num,eva[num])
#resultAddress="C:\\Users\\ASUS\\Desktop\\blogs\\qrels.february"
#result=readFile(resultAddress)
#print(result)
def MAP(Avep,queryNum):
    re=0
    for num in Avep:
      #  print(Avep[num])
        re=Avep[num]+re
    return re/queryNum
def Avp(result,simi,k):
    avp={}
    d ={}
    for num in result:
        avp[num]=0
       # d[num]= 0
    for num in result:
        relevance=0
        retrieval=0
        for weight,docid in sorted(simi[num])[:k]:
            retrieval=retrieval + 1
            if docid in result[num]:
                if result[num][docid]!='0':
                    relevance=relevance + 1
                    avp[num]=avp[num] + (relevance/retrieval)
                    #print(relevance)
        if relevance !=0:
            avp[num]=avp[num]/relevance
    return avp
    
