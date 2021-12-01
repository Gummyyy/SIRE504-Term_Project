def create_qauntile(series = [], percents = []):
    qauntiles = []

    for percent in percents:
        qauntile = series.quantile(percent)
        qauntiles.append(qauntile)

    return qauntiles