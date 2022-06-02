from multiprocessing import Process, Pool
import os
import pandas as pd
from razdel import tokenize
from pymorphy2 import MorphAnalyzer

m = MorphAnalyzer()


def make_dirs(names):
    try:
        os.mkdir('C:/Users/liana/PycharmProjects/ColingPython-p2/seminar_1/news'+f'/{names}')
    except:
        print('already existing directory')


def preprocess(text):
    tokens = list(tokenize(text))
    tokens_list = [_.text for _ in tokens]
    lemma_list = []
    for i in tokens_list:
        if i.isalpha():
            p = m.parse(i)[0]
            p = p.normal_form
            lemma_list.append(p)
    lem_text = ' '.join(lemma_list)
    return lem_text


def save(text, topic, url):
    with open(os.path.abspath(os.getcwd())+r'\news'+rf'\{topic}'+rf'\{url}'+'.txt',
              "w", encoding='utf-8') as news:
        news.write(text)


def process(row):
    text = row[1]['text']
    save(preprocess(text), row[1]['topics'], row[1]['url'].split('/')[-1].split('.')[0])


def main():
    df = pd.read_csv('ria.csv', encoding='utf-8')
    topics = ['В мире', 'Происшествия', 'Общество', 'Экономика', 'РИА Наука', 'Политика', 'Россия', 'Безопасность']
    rslt_df = df.loc[df['topics'].isin(topics)]
    try:
        os.mkdir('C:/Users/liana/PycharmProjects/ColingPython-p2/seminar_1/news')
    except:
        print('already existing directory')
    for i in topics:
        make_dirs(i)
    with Pool(4) as pool:
        pool.map(process, rslt_df.iterrows())
    for i in topics:
        print(i)
        for j in os.listdir(os.getcwd()+r'\news'+rf'\{i}'):
            print(f'\t{j}')


if __name__ == '__main__':
    main()
