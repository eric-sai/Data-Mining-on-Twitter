import math
from index import make_invidx_by_OkapiBM25
from index import make_invidx_by_OkapiBM25s
def TSV(tf,df,N,simi):
    termSelectedValue={}
    rt={}
    for docid in tf:
        for weight,docid1 in simi:
            if docid ==docid1:
                for term in tf[docid]:
                    rt[term]= rt.get(term,0) + 1
    for term1 in rt:
        termSelectedValue[term1]=math.pow((df[term1]/N),rt[term1])
    return termSelectedValue    
    
