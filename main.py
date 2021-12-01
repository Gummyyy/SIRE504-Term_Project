from __future__ import division
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import plotly
import pandas as pd
import os.path
from datetime import datetime, timedelta
from module.file.fileManager import readFastQ, readPickle
from module.file.html import createHtmlReport
def argparserLocal():
    from argparse import ArgumentParser
    parser = ArgumentParser(prog='FastReport', description='FastQ Report Genetator' )
    subparsers = parser.add_subparsers(title='commands',description= 'Please Choose the Command below', dest='command')
    subparsers.required = True
    qhtml_command = subparsers.add_parser('QuickHTML',help= 'Generate statistic report from FastQ file in HTML format')
    qhtml_command.add_argument('-f','--file',type=str,default=None, help= "Provide file path") 
    return parser
def main():
    start = datetime.now().time()
    parser = argparserLocal()
    args = parser.parse_args()
    if(args.command == "QuickHTML"):
        if args.file == None:
            print("---------------\nError: You did not provide file path\n------------\n")
            exit(parser.parse_args(['QuickHTML','-h']))
        
        filename = filename = os.path.splitext(args.file)[0]
        if not os.path.isfile("./pickle_store/"+filename+".pkl"):
    #--------------FastQ reader --------------------
            dataframe = readFastQ(args.file)
        else:
            dataframe = readPickle(filename)
    #-------------------html gen--------------------------
        createHtmlReport(dataframe,filename)
    #-------graph variable histogram-------------
        # avg_score = dataframe.avg_score
        # trace1 = go.Histogram(x=avg_score)   
        # layout = go.Layout(width=1000,height=500)
        # fig = go.Figure(data=trace1, layout=layout)
        # data1 = fig
    
    
        end = datetime.now().time()
        t1 = timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
        t2 = timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)  
        duration = t2 - t1
        print("Runtime: "+str(duration))

if __name__ == "__main__":
    main()