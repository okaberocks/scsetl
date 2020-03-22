from beautifuldict.baseconfig import Baseconfig

from pkg_resources import resource_filename

params = {
    'input': {
        'path': resource_filename(__name__, 'data/input/')
    },
    'output': {
        'path': resource_filename(__name__, 'data/output/'),
        'file': 'positivos-codigo-postal.json-stat'
    },
    'fillna': {
        'Sexo': 'No consta',
        'EDAD': 'No consta',
        'Estado': 'No consta',
        'F inicio': 'No consta',
        'F cura': 'No consta',
        'HOSPITALIZADO_HOSP_CENSO': 'No consta',
        'RESIDENCIA': 'No consta',
        'localidad': 'No consta',
        'codpostal': '39000',
        'codcentro': 'No consta',
        'nombre centro': 'No consta',
        'tipo centro': 'No consta',
        'codigo zona': 'No consta',
        'nombre zona': 'No consta',
        'codarea': 'No consta',
        'nombre area': 'No consta'
    },
    'replace': {
        'codpostal': {
            'old': '0',
            'new': '39000'
        }
}
}
cfg = Baseconfig(params)
