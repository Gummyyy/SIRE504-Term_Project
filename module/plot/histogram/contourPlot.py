import plotly.graph_objects as go
from module.plot.cal.layout import create_layout
from module.plot.cal.filter import by_barcodes
def seqlenAvgscoreToHtml(dataframe):

    barcode_type = dataframe['barcode'].value_counts().keys().tolist()
    print('in progress creaete all pie ...')
    trace_list = []
    lable_list = []
    label_df = ['All', 'Pass Read']
    df_pass_len = dataframe[dataframe['seq_len'] > 200] 
    df_pass_read = df_pass_len[df_pass_len['avg_score'] > 20]
    list_df = [dataframe, df_pass_read]
    is_first = True

    for current_index, current_df in enumerate(list_df):
        count_list = current_df['barcode'].value_counts().tolist()
        title = label_df[current_index]
        seq_len = current_df.seq_len
        avg_score = current_df.avg_score
        # graph will show at first times by value of is_first
        contour=go.Histogram2dContour(
        x = avg_score,
        y = seq_len,
        colorscale = 'Blues',
        visible= is_first
)
        #pie = go.Pie(labels=barcode_type, values=count_list, visible=is_first, name=title)
        trace_list.append(contour)
        lable_list.append(title)

        # if 1st index set it to False
        if is_first:
            is_first = False

        barcode_list_df = by_barcodes(dataframe=current_df, type_barcode_list=barcode_type)
        # create graph by barcodes (first times, they does not show)
        for barcode_index, barcode_df in enumerate(barcode_list_df):
            x=barcode_df['avg_score']
            y=barcode_df['seq_len']
            title_x = title + ' - Barcode ' + str(barcode_type[barcode_index])
            histogram = go.Histogram2dContour(x=x,y=y,colorscale = 'Blues', visible=False, name=title_x)
            trace_list.append(histogram)
            lable_list.append(title_x)
    # throw graphs to create common layout
    figure = create_layout(
        title='Contour Read Length & Phred Score',
        traces=trace_list, 
        lables=lable_list, 
        xname='PHRED Score', 
        yname='Sequence Length',
    )
    figure.update_layout(yaxis_range=[0,12000])

    return figure