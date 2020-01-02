import Part_1__Normalization as nrm
import Part_2__Indexing as idx
import pandas as pd
import numpy as np
import math


def get_tf_idf_vector_space(docs_address):
    train_docs = pd.read_csv(docs_address)
    tags = {1: [], 2: [], 3: [], 4: []}
    tag_list = []
    tag_sums = {1: 0, 2: 0, 3: 0, 4: 0}

    idx.TrieNode.WORDS = list()
    idx.TrieNode.DOCS = dict()
    trie = idx.TrieNode()

    cnt = 0
    new_ind = 0
    for ind, doc in train_docs.iterrows():
        cnt += 1
        if cnt % 3 != 0:
            continue
        s_text = nrm.normalize_english(doc["Text"])
        tags[doc["Tag"]].append(new_ind)
        tag_list.append(doc["Tag"])
        new_ind += 1
        for pos in range(len(s_text)):
            trie.add_word(s_text[pos], new_ind, pos)

    dictionary, doc_ids = np.array(trie.WORDS), np.array(list(trie.DOCS.keys()))
    terms_count, docs_count = len(dictionary), len(doc_ids)

    doc_term_matrix = np.zeros(shape=(docs_count, terms_count))

    for term_idx in range(len(dictionary)):
        postings_list = trie.get_postings_list(dictionary[term_idx])

        df = len(postings_list)

        for doc_id in postings_list:
            doc_idx = np.argwhere(doc_ids == doc_id)[0][0]
            tf = len(postings_list[doc_id])
            if tf == 0:
                doc_term_matrix[doc_idx][term_idx] = 0
            else:
                doc_term_matrix[doc_idx][term_idx] = (1 + math.log(tf, 10)) * math.log(docs_count / df, 10)

    normalized_doc_term_matrix = doc_term_matrix / np.linalg.norm(doc_term_matrix, ord=2, axis=1, keepdims=True)
    tag_sums[1] = np.sum(normalized_doc_term_matrix[tags[1], :])
    tag_sums[2] = np.sum(normalized_doc_term_matrix[tags[2], :])
    tag_sums[3] = np.sum(normalized_doc_term_matrix[tags[3], :])
    tag_sums[4] = np.sum(normalized_doc_term_matrix[tags[4], :])

    return normalized_doc_term_matrix, dictionary, tags, tag_sums, tag_list


def tf_idf_from_dict(docs_address, dictionary):
    docs = pd.read_csv(docs_address)
    tags = []

    idx.TrieNode.WORDS = list()
    idx.TrieNode.DOCS = dict()
    trie = idx.TrieNode()

    cnt = 0
    new_ind = 0
    for ind, doc in docs.iterrows():
        cnt += 1
        if cnt % 3 != 0:
            continue
        s_text = nrm.normalize_english(doc["Text"])
        tags.append(doc["Tag"])
        new_ind += 1
        for pos in range(len(s_text)):
            trie.add_word(s_text[pos], new_ind, pos)

    doc_ids = np.array(list(trie.DOCS.keys()))
    terms_count, docs_count = len(dictionary), len(doc_ids)

    doc_term_matrix = np.zeros(shape=(docs_count, terms_count))

    for term_idx in range(len(dictionary)):
        postings_list = trie.get_postings_list(dictionary[term_idx])
        if postings_list is None:
            continue
        df = len(postings_list)

        for doc_id in postings_list:
            doc_idx = np.argwhere(doc_ids == doc_id)[0][0]
            tf = len(postings_list[doc_id])
            if tf == 0:
                doc_term_matrix[doc_idx][term_idx] = 0
            else:
                doc_term_matrix[doc_idx][term_idx] = (1 + math.log(tf, 10)) * math.log(docs_count / df, 10)

    normalized_doc_term_matrix = doc_term_matrix / np.linalg.norm(doc_term_matrix, ord=2, axis=1, keepdims=True)

    return normalized_doc_term_matrix, tags


def print_stats_nb(classifier_func, test_doc_address):
    test_docs = pd.read_csv(test_doc_address)
    count = [0, 0, 0, 0]
    pred = [0, 0, 0, 0]
    true_pred = [0, 0, 0, 0]
    for ind, doc in test_docs.iterrows():
        s_text = nrm.normalize_english(doc["Text"])
        pred_tag = classifier_func(s_text)

        count[doc["Tag"] - 1] += 1
        pred[pred_tag - 1] += 1
        if doc["Tag"] == pred_tag:
            true_pred[doc["Tag"] - 1] += 1

    print('*** Naive Bayes ***')
    print('Accuracy =', sum(true_pred) / sum(count))
    print()
    for tag in range(4):
        print('class', tag + 1, 'precision and recall')
        print('precision =', true_pred[tag] / pred[tag])
        print('recall =', true_pred[tag] / count[tag])
        print('f1 = ', 2 * (true_pred[tag] / pred[tag]) * (true_pred[tag] / count[tag]) / (
                (true_pred[tag] / pred[tag]) + (true_pred[tag] / count[tag])))
        print()
