import plotly.graph_objs as go
import numpy as np
def plotSummaryTable(dataframe):
    Table_pass_read = dataframe[dataframe.avg_score > 20]
    Table_pass_read_bar = Table_pass_read.groupby('barcode')
    group_bar = dataframe.groupby('barcode')
    barNumList = list(group_bar.groups.keys())
    fig = go.Figure()
    
    fig.add_trace(go.Table(header=dict(values=['Status', 'Number of Reads', 'Number of Bases', 'Median Read Length', 'Median PHRED score']),
                 cells=dict(values=[['All reads', 'Pass reads'], [len(dataframe), len(Table_pass_read)], [sum(dataframe.seq_len), sum(Table_pass_read.seq_len)], 
                 ['{:.2f}'.format(dataframe.seq_len.median()), '{:.2f}'.format(Table_pass_read.seq_len.median())], ['{:.2f}'.format(dataframe.avg_score.median()), '{:.2f}'.format(Table_pass_read.avg_score.median())]])))
    for i in range(len(barNumList)):
        fig.add_trace(go.Table(header=dict(values=['Status', 'Number of Reads', 'Number of Bases', 'Median Read Length', 'Median PHRED score']),
                    cells=dict(values=[['All reads', 'Pass reads'], [group_bar.size()[i], Table_pass_read_bar.size()[i]], [group_bar.seq_len.sum()[i], Table_pass_read_bar.seq_len.sum()[i]], 
                    ['{:.2f}'.format(group_bar.seq_len.median()[i]), '{:.2f}'.format(Table_pass_read_bar.seq_len.median()[i])], ['{:.2f}'.format(group_bar.avg_score.median()[i]), '{:.2f}'.format(Table_pass_read_bar.avg_score.median()[i])]])))
# -----------------------------------------
    barcode = dataframe['barcode'].value_counts().keys().tolist()
    visible = np.identity(len(barcode)+1)
    visible = visible.astype(np.bool)
    test_list = []
    test_list.append(dict(label="Total",
                     method="update",
                     args=[{"visible": visible[0]},
                           {"title": "Total reads summary",
                            "annotations": []}]))
    
    for i in range(len(barcode)):
        test_list.append(dict(label='Bar: '+str(barcode[i]),
                     method="update",
                     args=[{"visible": visible[i+1]},
                           {"title": 'Barcode '+str(barcode[i])+' reads summary',
                            "annotations": []}]))
        
    fig.update_layout(
        width=1000,
        height=390,
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.57,
            y=1.2,
            buttons=list(test_list),
        )
    ])
    return fig