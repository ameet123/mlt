import math
import logging
import os
from collections import namedtuple

import pandas as pd

MASTER_LEVEL = logging.INFO
LOGGER = logging.getLogger("tfidf")
unwantedChars = ['\'', '"', ',', ';', ':', '-', '.', ')', '(']
Term = namedtuple('Term', 'term count')


def set_logging():
    LOGGER.setLevel(MASTER_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(MASTER_LEVEL)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%m-%d %I:%M:%S')
    ch.setFormatter(formatter)
    LOGGER.addHandler(ch)


def cleanseLine(chars, oneLine):
    for ch in chars:
        oneLine = oneLine.replace(ch, '')
    return oneLine.lower()


def get_doc_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def __ingest_words(word_file):
    termDict = {}
    with open(word_file, "r") as f:
        for line in f:
            line = cleanseLine(unwantedChars, line)
            for w in line.split():
                if w in termDict:
                    term = termDict[w]
                    count = term.count + 1
                else:
                    count = 1
                termDict[w] = Term(w, count)
                LOGGER.debug("%s", termDict[w])
    return termDict


def compute_tf(path, document):
    '''
    convert dictionary to DataFrame and calculate term frequency
    :param path:
    :return:
    '''
    termDict = __ingest_words(path)
    termDF = pd.DataFrame.from_dict(termDict, orient='index')
    termDF.reset_index(level=0, inplace=True)
    termDF.drop('index', 1, inplace=True)
    maxCnt = termDF['count'].max()
    LOGGER.info("[%s] Max word count:%d", document, maxCnt)
    termDF[document + '_tf'] = termDF.apply(lambda row: row['count'] / float(maxCnt), axis=1)
    termDF.drop('count', 1, inplace=True)
    # termDF.rename(columns={'count': document + "_count"}, inplace=True)
    LOGGER.debug("\n%s", termDF.to_string())
    return termDF


def computeTfIdf(my_dir):
    df_list = {}
    for f in os.listdir(my_dir):
        LOGGER.info(">>Working on file:%s", f)
        abs_path = my_dir + "/" + f
        document = get_doc_name(abs_path)
        docDF = compute_tf(abs_path, document)
        df_list[document] = docDF
    LOGGER.info(">>Total dataframes in the list:%s", len(df_list))
    # Merge the dataframes
    dfs = df_list.values()
    all_df = reduce(lambda left, right: pd.merge(left, right, how='outer'), dfs)
    LOGGER.info(">>Final DF rows:[%d]", all_df.shape[0])
    # number of docs : minus the term
    N = len(all_df.columns) - 1
    # Add non-NaN column count
    # all_df['doc_count'] = all_df.count(axis=1) - 1

    all_df['idf'] = math.log((float(N)/(all_df.count(axis=1) - 1)).astype(float))
    LOGGER.info("\n%s", all_df.to_string())


def main():
    my_dir = "Ballmer"
    set_logging()
    path = "Ballmer/ballmer02.txt"
    computeTfIdf(my_dir)


if __name__ == '__main__':
    main()
