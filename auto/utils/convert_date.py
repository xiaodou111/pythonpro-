import pandas as pd
def convert_date_columns(df, *date_columns):
    """
    转换DataFrame中指定列的日期格式。

    参数:
    df (DataFrame): 需要转换日期格式的DataFrame。
    *date_columns (str): 需要转换的日期列名。

    返回:
    DataFrame: 日期格式转换后的DataFrame。
    """
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    return df