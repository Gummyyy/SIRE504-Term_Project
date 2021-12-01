import plotly.graph_objects as go 
from .filter import by_barcodes

def create_lines(x_list = [], ymax = 3000):
    lines = []

    for x in x_list:
        line = dict(
            type='line',
            line=dict(dash='dash', color='red'),
            xref='x',
            yref='y',
            x0=x,
            x1=x,
            y0=0,
            y1=ymax
        )
        lines.append(line)

    return lines

def create_annotations(x_list = [], ymax = 3000, percents = []):
    annotations = []

    for index, x in enumerate(x_list):
        percent = percents[index] * 100
        annotation_qantile = dict(
            text=str(percent) + '%',
            xref='x',
            yref='y',
            x=x,
            y=ymax,
            showarrow=False
        )
        annotation_value = dict(
            text=float('{:.2f}'.format(x)),
            xref='x',
            yref='y',
            x=x,
            y=ymax,
            showarrow=True
        )
        annotations.append(annotation_qantile)
        annotations.append(annotation_value)

    return annotations

def create_layout(traces=[], lables=[], qauntiles=[], ymin=0, xname='label x', yname='label y', title='Graph', percents=[]):
    print('in create layout progress ...')
    dropdown_buttons = []
    lines = []
    annotations = []
    n_trace = len(traces)
    n_qauntile = len(qauntiles)

    # check if there is qauntile value (prevent out of index error)
    if n_trace == n_qauntile:
        lines = create_lines(x_list=qauntiles[0])
        annotations = create_annotations(x_list=qauntiles[0], percents=percents)

    figure = go.Figure(data=traces, layout=dict(shapes=lines, annotations=annotations, title=title + ', ' + lables[0]))

    # create button dependence on how many graph
    for index, trace in enumerate(traces):
        visible_list = [False] * n_trace
        visible_list[index] = True
        label = lables[index]

        # check if there is qauntile value (prevent out of index error)
        if n_qauntile == n_trace:
            lines = create_lines(qauntiles[index])
            annotations = create_annotations(x_list=qauntiles[index], percents=percents)

        # if click button, will change graph, qauntile line and qauntile text
        button = dict(
            args=[
                dict(visible=visible_list,), 
                dict(shapes=lines, annotations=annotations, title=title + ', ' + label)
            ],
            method='update',
            label=label
        )
        dropdown_buttons.append(button)

    print('update layout')
    updatemenus = [
        dict(
            pad={'r': 10, 't': 10},
            buttons=dropdown_buttons,
            direction='down',
            showactive=True,
            type='dropdown',
        )
    ]

    # set layout dependence on design
    figure.update_layout(
        width=1200,
        height=500,
        updatemenus=updatemenus,
        #yaxis_range=[ymin, ymax],
        xaxis=dict(),
        xaxis_title_text=xname,
        yaxis_title_text=yname,
    )
    if(title == 'Contour Read Length & Phred Score'):
        figure.update_layout(
        width=1200,
        height=500,
        updatemenus=updatemenus,
        #yaxis_range=[ymin, ymax],
        xaxis=dict(),
        xaxis_title_text=xname,
        yaxis_title_text=yname,
    )

    return figure
