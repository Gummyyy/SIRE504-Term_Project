import plotly.graph_objects as go 
from module.plot.cal.layout import create_layout

def create_all_pie(dataframe):
    barcode_type = dataframe['barcode'].value_counts().keys().tolist()
    print('in progress creaete all pie ...')
    trace_list = []
    label_list = []
    label_df = ['All', 'Pass Read']
    df_pass_len = dataframe[dataframe['seq_len'] > 200] 
    df_pass_read = df_pass_len[df_pass_len['avg_score'] > 20]
    list_df = [dataframe, df_pass_read]
    is_first = True

    print('create graph ...')
    # create graph by barcodes (first times, they does not show)
    for current_index, current_df in enumerate(list_df):
        count_list = current_df['barcode'].value_counts().tolist()
        title = label_df[current_index]
        # graph will show at first times by value of is_first
        pie = go.Pie(labels=barcode_type, values=count_list, visible=is_first, name=title)
        trace_list.append(pie)
        label_list.append(title)

        # if 1st index set it to False
        if is_first:
            is_first = False
    # throw graphs to create common layout
    figure = create_layout(traces=trace_list, lables=label_list, title='Graph by Barcodes',)

    return figure