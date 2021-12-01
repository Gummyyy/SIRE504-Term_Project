import plotly.graph_objs as go
def avgReadToHtml(dataframe):
    #-------graph variable histogram-------------
    avg_score = dataframe.avg_score
    trace1 = go.Histogram(x=avg_score)   
    layout = go.Layout(width=1000,height=500)
    fig = go.Figure(data=trace1, layout=layout)
    return fig