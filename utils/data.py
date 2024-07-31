def get_unique_types_of_col(_df_col):
  return set(_df_col.map(type))

def get_all_unique_types(df):
  return {col: get_unique_types_of_col(df[col]) for col in df.columns}

def get_null_counts(_df):
  null_counts = _df.isnull().sum()
  return null_counts[null_counts != 0]
