import os

import pandas as pd


def append_to_csv(_data, _columns, _filename):
  if not _data or len(_data) == 0:
    return
  new_row = pd.DataFrame(_data)
  if os.path.exists(_filename):
    df = pd.read_csv(_filename)
  else:
    df = pd.DataFrame(columns=_columns)
  df = pd.concat([df, new_row], ignore_index=True)
  df.to_csv(_filename, index=False)