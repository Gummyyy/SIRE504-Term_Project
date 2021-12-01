from __future__ import division
import pandas as pd
import os.path
from Bio import SeqIO
import re
from tqdm import tqdm
import sys
def readFastQ(path):
    
    filename = os.path.splitext(path)[0]
    id=[]
    runid = []
    sampleid = []
    read =[]
    ch =[]
    start_time = []
    barcode = []
    seq = []
    list_score = []
    sum_score =[]
    seq_len=[]
    avg_score = []
    num_read = (sum(1 for _ in open(path)))/4
    chunk_size = round(num_read/100)-1
    count = 0
    with tqdm(total=num_read,unit="read",file=sys.stdout,desc="Reading FastQ file") as pbar:
        for record in SeqIO.parse(path,'fastq'):
            if count%chunk_size==0:
                pbar.update(chunk_size)
                pbar.refresh()
            count = count + 1
            detail = re.match(r'(.*) runid=(.*) sampleid=(.*) read=(.*) ch=(.*) start_time=(.*) barcode=barcode(.*)',record.description)
            id.append(detail.group(1))
            runid.append(detail.group(2))
            sampleid.append(detail.group(3))
            read.append(detail.group(4))
            ch.append(detail.group(5))
            start_time.append(detail.group(6))
            barcode.append(detail.group(7))
            seq.append(str(record.seq))
            seq_len.append(len(str(record.seq)))
            list_score.append(record.letter_annotations['phred_quality'])
            sum_score.append(sum(record.letter_annotations['phred_quality']))
            avg_score.append(sum(record.letter_annotations['phred_quality'])/len(str(record.seq)))
    data = {"id":id,"runid":runid,"sample":id,"read":read,"ch":ch,"start_time":start_time,"barcode":barcode,"seq":seq,"seq_len":seq_len,"list_score":list_score,"sum_score":sum_score,"avg_score": avg_score}
    dataframe = pd.DataFrame(data)
    #-------------------save dataframe to external file----------
    dataframe.to_pickle("./pickle_store/"+filename+".pkl")
    return dataframe

def readPickle(filename):
    dataframe = pd.read_pickle("./pickle_store/"+filename+".pkl")
    return dataframe