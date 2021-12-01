import plotly.graph_objects as go 
from module.plot.cal.filter import by_barcodes
from module.plot.cal.layout import create_layout
from module.plot.cal.calculation import create_qauntile

def create_all_histogram(dataframe):
    barcode_type = dataframe['barcode'].value_counts().keys().tolist()
    print('in creaete all historgram progress ...')
    trace_list = []
    lable_list = []
    qauntile_list = []
    percents = [0.1, 0.25, 0.5, 0.75, 0.9]
    label_df = ['Merge', 'Pass Read']
    df_pass_len = dataframe[dataframe['seq_len'] > 200] 
    df_pass_read = df_pass_len[df_pass_len['avg_score'] > 20]
    list_df = [df_pass_len, df_pass_read]
    is_first = True

    print('create graph ...')
    for current_index, current_df in enumerate(list_df):
        # create initial show (first times) graph dependence on 1st index
        x = current_df['seq_len']
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
            x=barcode_df['seq_len']
            title_x = title + ' - Barcode ' + str(barcode_type[barcode_index])
            histogram = go.Histogram(x=x, visible=False, name=title_x)
            qauntile = create_qauntile(series=x, percents=percents)

            qauntile_list.append(qauntile)
            trace_list.append(histogram)
            lable_list.append(title_x)
    
    # throw graphs to create common layout
    figure = create_layout(
        title='Graph All Pass',
        traces=trace_list, 
        lables=lable_list, 
        xname='Sequence length', 
        yname='Density',
        qauntiles=qauntile_list,
        percents=percents
    )

    return figure