import pandas as pd

df = pd.concat(
    map(pd.read_csv, ['articlesfrommagyarnemzetorban 1-122.csv', 'articlesfrommagyarnemzetorban 124-135ig.csv',
    'articlesfrommagyarnemzetorban 136-181ig.csv', 'articlesfrommagyarnemzetorban elvilegjo440-600.csv']), ignore_index=True)

df.to_csv('kulfoldkategoria-magyarnemzet-2022es.csv', index=False, encoding='utf-8-sig')