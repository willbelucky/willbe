# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 21.
"""
from __future__ import print_function
from functools import reduce
import re
import tarfile

import numpy as np

from keras.utils.data_utils import get_file
from keras.layers.embeddings import Embedding
from keras.layers import Input, Dropout, RepeatVector, Dense, add
from keras.layers.recurrent import LSTM as RNN
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences

from util.machine_learning_supporter import SupervisedData

SENTENCE = 0
QUERY = 1


def tokenize(sent):
    """Return the tokens of a sentence including punctuation.
    >>> tokenize('Bob dropped the apple. Where is the apple?')
    ['Bob', 'dropped', 'the', 'apple', '.', 'Where', 'is', 'the', 'apple', '?']
    """
    return [x.strip() for x in re.split('(\W+)?', sent) if x.strip()]


def parse_stories(lines, only_supporting=False):
    """Parse stories provided in the bAbi tasks format
    If only_supporting is true,
    only the sentences that support the answer are kept.
    """
    data = []
    story = []
    for line in lines:
        line = line.decode('utf-8').strip()
        nid, line = line.split(' ', 1)
        nid = int(nid)
        if nid == 1:
            story = []
        if '\t' in line:
            q, a, supporting = line.split('\t')
            q = tokenize(q)
            if only_supporting:
                # Only select the related sub_story
                supporting = map(int, supporting.split())
                sub_story = [story[i - 1] for i in supporting]
            else:
                # Provide all the sub_stories
                sub_story = [x for x in story if x]
            data.append((sub_story, q, a))
            story.append('')
        else:
            sent = tokenize(line)
            story.append(sent)
    return data


def get_stories(f, only_supporting=False, max_length=None):
    """Given a file name, read the file, retrieve the stories,
    and then convert the sentences into a single story.
    If max_length is supplied,
    any stories longer than max_length tokens will be discarded.
    """
    data = parse_stories(f.readlines(), only_supporting=only_supporting)
    flatten = lambda data: reduce(lambda x, y: x + y, data)
    data = [(flatten(story), q, answer) for story, q, answer in data if
            not max_length or len(flatten(story)) < max_length]
    return data


def vectorize_stories(data, word_idx, sentence_maxlen, query_maxlen):
    xs = []
    xqs = []
    ys = []
    for story, query, answer in data:
        x = [word_idx[w] for w in story]
        xq = [word_idx[w] for w in query]
        # let's not forget that index 0 is reserved
        y = np.zeros(len(word_idx) + 1)
        y[word_idx[answer]] = 1
        xs.append(x)
        xqs.append(xq)
        ys.append(y)
    return pad_sequences(xs, maxlen=sentence_maxlen), pad_sequences(xqs, maxlen=query_maxlen), np.array(ys)


def get_data(job_name):
    try:
        path = get_file('babi-tasks-v1-2.tar.gz',
                        origin='https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz')
    except:
        print('Error downloading dataset, please download it manually:\n'
              '$ wget http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz\n'
              '$ mv tasks_1-20_v1-2.tar.gz ~/.keras/datasets/babi-tasks-v1-2.tar.gz')
        raise
    tar = tarfile.open(path)
    # Default QA1 with 1000 samples
    # challenge = 'tasks_1-20_v1-2/en/qa1_single-supporting-fact_{}.txt'
    # QA1 with 10,000 samples
    # challenge = 'tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_{}.txt'
    # QA2 with 1000 samples
    challenge = 'tasks_1-20_v1-2/en/qa2_two-supporting-facts_{}.txt'
    # QA2 with 10,000 samples
    # challenge = 'tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_{}.txt'
    train = get_stories(tar.extractfile(challenge.format('train')))
    test = get_stories(tar.extractfile(challenge.format('test')))

    vocab = set()
    for story, q, answer in train + test:
        vocab |= set(story + q + [answer])
    vocab = sorted(vocab)

    # Reserve 0 for masking via pad_sequences
    vocab_size = len(vocab) + 1
    word_idx = dict((c, i + 1) for i, c in enumerate(vocab))
    sentence_maxlen = max(map(len, (x for x, _, _ in train + test)))
    query_maxlen = max(map(len, (x for _, x, _ in train + test)))

    train_sentences, train_queries, train_answers = vectorize_stories(train, word_idx, sentence_maxlen, query_maxlen)
    test_sentences, test_queries, test_answers = vectorize_stories(test, word_idx, sentence_maxlen, query_maxlen)

    print('vocab = {}'.format(vocab))
    print('train_sentences.shape = {}'.format(train_sentences.shape))
    print('train_queries.shape = {}'.format(train_queries.shape))
    print('train_answers.shape = {}'.format(train_answers.shape))
    print('sentence_maxlen, query_maxlen = {}, {}'.format(sentence_maxlen, query_maxlen))

    return SupervisedData(job_name,
                          x_train=[train_sentences, train_queries],
                          y_train=train_answers,
                          x_test=[test_sentences, test_queries],
                          y_test=test_answers,
                          input_shape={SENTENCE: (sentence_maxlen,), QUERY: (query_maxlen,)},
                          vocab_size=vocab_size,
                          sentence_maxlen=sentence_maxlen,
                          query_maxlen=query_maxlen)


def get_model(data: SupervisedData, embed_hidden_size):
    sentence = Input(shape=data.input_shape[SENTENCE], dtype='int32')
    # noinspection PyUnresolvedReferences
    encoded_sentence = Embedding(data.vocab_size, embed_hidden_size)(sentence)
    encoded_sentence = Dropout(0.3)(encoded_sentence)

    question = Input(shape=data.input_shape[QUERY], dtype='int32')
    # noinspection PyUnresolvedReferences
    encoded_question = Embedding(data.vocab_size, embed_hidden_size)(question)
    encoded_question = Dropout(0.3)(encoded_question)
    encoded_question = RNN(embed_hidden_size)(encoded_question)
    # noinspection PyUnresolvedReferences
    encoded_question = RepeatVector(data.sentence_maxlen)(encoded_question)

    merged = add([encoded_sentence, encoded_question])
    merged = RNN(embed_hidden_size)(merged)
    merged = Dropout(0.3)(merged)
    # noinspection PyUnresolvedReferences
    preds = Dense(data.vocab_size, activation='softmax')(merged)

    model = Model([sentence, question], preds)
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    return model


if __name__ == '__main__':
    job_name = 'babi_rnn'

    EMBED_HIDDEN_SIZE = 50
    BATCH_SIZE = 32
    EPOCHS = 40

    data = get_data(job_name)

    model = get_model(data, EMBED_HIDDEN_SIZE)

    data.evaluate_model(model, BATCH_SIZE, EPOCHS)
