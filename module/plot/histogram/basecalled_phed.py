import plotly.graph_objects as go 
from module.plot.cal.layout import create_layout
from module.plot.cal.filter import by_barcodes
from module.plot.cal.calculation import create_qauntile

def create_phedquality(dataframe):
    barcode_type = dataframe['barcode'].value_counts().keys().tolist()
    print('in phred historgram progress ...')
    trace_list = []
    lable_list = []
    qauntile_list = []
    percents = [0.1, 0.25, 0.5, 0.75, 0.9]
    label_df = ['Merge', 'Pass Read']
    df_phedq = dataframe
    df_pass_phedq = df_phedq[df_phedq['seq_len'] > 200]
    list_df = [df_phedq, df_pass_phedq]
    is_first = True

    print('create graph ...')
    for current_index, current_df in enumerate(list_df):
        # create initial show (first times) graph dependence on 1st index
        x = current_df['avg_score']
        title = label_df[current_index]
        title_x = title + ' - All'
       
        # set graph show at first times by value of is_first
        histogram = go.Histogram(x=x, visible=is_first, name=title_x)
        qauntile = create_qauntile(series=x, percents=percents)

        qauntile_list.append(qauntile)
        trace_list.append(histogram)
        lable_list.append(title_x)

        # if 1st index set it to False
        if is_first:
            is_first = False

        barcode_list_df = by_barcodes(dataframe=current_df, type_barcode_list=barcode_type)

        # create graph by barcodes (first times, they does not show)
        for barcode_index, barcode_df in enumerate(barcode_list_df):
            x=barcode_df['avg_score']
            title_x = title + ' - Barcode ' + str(barcode_type[barcode_index])
            histogram = go.Histogram(x=x, visible=False, name=title_x)
            qauntile = create_qauntile(series=x, percents=percents)

            qauntile_list.append(qauntile)
            trace_list.append(histogram)
            lable_list.append(title_x)
    
    # throw graphs to create common layout
    figure = create_layout(
        title='Graph Phred Score',
        traces=trace_list, 
        lables=lable_list, 
        xname='PHRED Score', 
        yname='Density',
        qauntiles=qauntile_list,
        percents=percents
    )

    return figure