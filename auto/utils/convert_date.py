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
        print("指定需要转换成时间格式的字段:",col)
        try:
            df[col] =df[col].astype('datetime64[ns]')
        except Exception as e:
            # 处理可能发生的错误
            print(f"数据转换失败11111：{e}")
    print('修改后DataFrame数据类型')
    print(df.dtypes)
    return df