import plotly.graph_objs as go
def barcodePropToHtml(dataframe):
    #-------graph variable pie-------------
    values = dataframe['barcode'].value_counts().keys().tolist()
    counts = dataframe['barcode'].value_counts().tolist()
    trace2 = go.Pie(labels=values, values=counts)
    layout = go.Layout(width=400,height=500)
    fig = go.Figure(data=trace2, layout=layout)
    return fig
    
