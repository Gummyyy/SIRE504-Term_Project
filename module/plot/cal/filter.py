def by_barcodes(dataframe, type_barcode_list=[]):
    filter_barcodes = []

    for barcode in type_barcode_list:
        df_barcode = dataframe[dataframe['barcode'] == barcode]
        filter_barcodes.append(df_barcode)
    
    return filter_barcodes