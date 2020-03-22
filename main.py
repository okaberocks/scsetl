from etlstat.extractor import extractor
from cfg import cfg
from pyjstat import pyjstat
import pandas as pd

cases = extractor.xlsx(cfg.input.path)

cases_df = cases['cruce qlik.xlsx']['cruce_qlik']

cases_df.fillna(value=cfg.fillna, inplace=True)
cases_df.replace(
    to_replace=cfg.replace.codpostal.old,
    value=cfg.replace.codpostal.new,
    inplace=True
)
cases_df['codpostal'] = cases_df['codpostal'].astype(int)
cases_df['codpostal'] = cases_df['codpostal'].astype(object)

results = cases_df.groupby(['codpostal']).count()
print(type(results))
print(results)

results_dataset = pyjstat.Dataset.read(pd.DataFrame({'codpostal': results.index, 'ID': results['ID']}), value='ID') 
print(results_dataset)
print(results_dataset.write())