from etlstat.extractor import extractor
from cfg import cfg
from pyjstat import pyjstat
import pandas as pd

cases = extractor.xlsx(cfg.input.path)
municipios = extractor.csv(cfg.input.path, sep=',')
cases_df = cases['cruce qlik.xlsx']['cruce_qlik']
municipios_df = municipios['municipios.csv']

cases_df.fillna(value=cfg.fillna, inplace=True)
cases_df.replace(
    to_replace=cfg.replace.codpostal.old,
    value=cfg.replace.codpostal.new,
    inplace=True
)
cases_df['codpostal'] = cases_df['codpostal'].astype(int)
cases_df['codpostal'] = cases_df['codpostal'].astype(object)

# TODO: extract constants to config - maybe a dict
cases_df['localidad'].replace('SANTANDER - P', 'SANTANDER (SANTANDER)', inplace=True)
cases_df['localidad'].replace('ENTRAMBASAGUAS - P', 'ENTRAMBASAGUAS (ENTRAMBASAGUAS)', inplace=True)
cases_df['localidad'].replace('SANTIURDE DE TORANZO - P', 'SANTIURDE DE TORANZO (SANTIURDE DE TORANZO)', inplace=True)
cases_df['localidad'].replace('BARCENA DE CICERO - P', 'BARCENA DE CICERO (BARCENA DE CICERO)', inplace=True)
cases_df['localidad'].replace('LAREDO - P', 'LAREDO (LAREDO)', inplace=True)
cases_df['localidad'].replace('PENAGOS - P', 'PENAGOS (PENAGOS)', inplace=True)
cases_df.replace({'localidad': {'ASTILLERO (EL) (ASTILLERO (EL))': 'ASTILLERO, EL (ASTILLERO, EL)'}}, inplace=True)
cases_df.replace({'localidad': {'CORRALES (LOS) (CORRALES DE BUELNA (LOS))': 'CORRALES, LOS (CORRALES DE BUELNA, LOS)'}}, inplace=True)
cases_df['localidad'].replace('HAYUELA (LA) (UDIAS)', 'HAYUELA, LA (UDIAS)', inplace=True)
cases_df['localidad'].replace('COSTANA (LA) (CAMPOO DE YUSO)', 'COSTANA, LA (CAMPOO DE YUSO)', inplace=True)
cases_df['localidad'].replace('PESQUERA (LA) (LAREDO)', 'PESQUERA, LA (LAREDO)', inplace=True)

cases_df = cases_df[cases_df.localidad != 'No consta']
cases_df = cases_df[cases_df.localidad != 'LOCALIDAD DESCONOCIDA']

cases_df[['localidad_only',
          'municipio']] = cases_df.localidad.str.split("(", 1, expand=True) 
cases_df['municipio'] = cases_df['municipio'].str.slice(0, -1)

# WARNING: merge wont show unmatched results. Pay attention to the 
# number of expected results
cases_mun_df = pd.merge(cases_df, municipios_df, on='municipio')
# print(cases_df.at[2, 'localidad'])

cases_mun_df.to_csv('./prueba.csv')

results_mun = cases_mun_df.groupby(['codigo_ine']).count()
results = cases_df.groupby(['codpostal']).count()

results_mun = pd.DataFrame({'codigo_ine': results_mun.index,
                            'value': results_mun['ID']})
results = pd.DataFrame({'codpostal': results.index, 'value': results['ID']})

results_mun = results_mun.melt(
    id_vars=['codigo_ine'],
    value_vars=['value'],
    var_name='Variables'
)
results_mun = results_mun.sort_values(by=['codigo_ine', 'Variables'])
results = results.melt(
    id_vars=['codpostal'],
    value_vars=['value'],
    var_name='Variables'
)
results = results.sort_values(by=['codpostal', 'Variables'])

results_dataset = pyjstat.Dataset.read(results)
results_mun_dataset = pyjstat.Dataset.read(results_mun)


print(results_dataset.write())
print(results_mun_dataset.write())