import os
import pandas as pd
import calendar
import gzip
import time
from xml.etree import ElementTree


def translate(translations_xml: str) -> dict:
    """Takes in the path of the translations gzip file and returns a dict in
    the form {Asset: {Variable: Name}}."""
    return {a.attrib['name']: {t.find('src').text: t.find('dest').text
                               for t in a.findall('translation')}
            for a in
            ElementTree.parse(gzip.open(translations_xml)).findall('asset')}


def mapper(x: pd.Series) -> tuple:
    """Maps the value series for each variable in a tuple (sum, count)."""
    return x.sum(), x.count()


def reducer(x: pd.Series) -> float:
    """Reduces the (sum, count) tuple series to get the mean of each
    variable."""
    try:
        y = list(map(sum, zip(*x)))
        return round(y[0] / y[1], 5)
    except TypeError:
        if x.notnull().any():
            y = list(map(sum, zip(*x.dropna())))
            return round(y[0] / y[1], 5)


def timer(x: str) -> int:
    """Gets the unix timestamp assuming that the datetime is on UTC."""
    return 600 * (int(calendar.timegm(
        time.strptime(x + '0', '%Y-%m-%d%H:%M'))) // 600 + 1)


def horizontalize(dataset: str, translations: dict) -> pd.DataFrame:
    """Takes in the dataset and translations dict and returns horizontalized 
    data calculating 10 minute averages for each variable and asset."""
    df = pd.DataFrame()
    for df_chunk in pd.read_csv(dataset, chunksize=10 ** 6,
                                compression='gzip'):
        df_chunk['time'] = [x[:4] for x in df_chunk['time']]
        df_chunk['variable'] = [translations[x[0]][x[1]] for x in
                                zip(df_chunk['asset'], df_chunk['variable'])]
        df = df.append(df_chunk.pivot_table(index=['asset', 'date', 'time'],
                                            columns='variable',
                                            values='value',
                                            aggfunc=mapper).reset_index())
    df['unixtime'] = list(map(timer, df['date'] + df['time']))
    df.drop(['date', 'time'], axis=1, inplace=True)
    return df.groupby(['asset', 'unixtime']).agg(reducer)


def process(input_folder: str, output_folder: str, translations_xml: str):
    for dataset in os.listdir(input_folder):
        if '.csv.gz' in dataset:
            t0 = time.time()
            print(f"PROCESSING {dataset} ...")
            processed = horizontalize(dataset=input_folder + dataset,
                                      translations=translate(translations_xml))
            processed.to_csv(output_folder + dataset, compression='gzip')
            print(f"TIME! {round(time.time() - t0, 3)}(s)")


process(input_folder='raw/',
        output_folder='processed/',
        translations_xml='translations.xml.gz')
