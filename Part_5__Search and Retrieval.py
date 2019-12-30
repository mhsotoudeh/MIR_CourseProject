import numpy as np
import Part_1__Normalization as nrm
import Part_2__Indexing as idx
import json
import sys
import math
import shlex


class ProximityQuery:
    def __init__(self, query, window_size):
        self.query = query
        self.window_size = window_size


def normalize_rows(matrix):
    return matrix / np.linalg.norm(matrix, ord=2, axis=1, keepdims=True)


def normal_search(query, docs, doc_ids):
    scores = []
    for i in range(len(docs)):
        score = np.dot(docs[i], query)
        scores.append(score)

    # Sort and Give Results
    zipped_pairs = zip(scores, doc_ids)
    search_result = [x for _, x in sorted(zipped_pairs)]
    search_result.reverse()
    sorted_scores = scores.copy()
    sorted_scores.sort(reverse=True)

    return search_result, sorted_scores


def proximity_search(proximity_query, docs, doc_ids):
    # Find Docs with All Words Present
    query_term_indices = np.array([])
    for term in proximity_query.query:
        index = np.argwhere(dictionary == term)
        if len(index) != 0:
            query_term_indices = np.append(query_term_indices, index)
    query_term_indices = query_term_indices.astype(int)

    if len(query_term_indices) < len(proximity_query.query):
        return [], []

    eligible_documents = np.array([])
    eligible_document_ids = np.array([])
    for i in range(len(docs)):
        row = docs[i]
        eligible = True
        for idx in query_term_indices:
            if row[idx] == 0:
                eligible = False

        # Find Docs with Words Inside the Window

        if eligible is True:
            eligible_documents = np.append(eligible_documents, row)
            eligible_document_ids = np.append(eligible_document_ids, doc_ids[i])

    # Search Between Eligible Documents and Return Results and Scores
    results, scores = normal_search(query, eligible_documents, eligible_document_ids)
    return results, scores


def get_weight(tf, df, type):
    if type == 'ln':
        return 1 + math.log(tf, 10)
    elif type == 'lt':
        return (1 + math.log(tf, 10)) * math.log(docs_count / df, 10)
    elif type == 'nt':
        return tf * math.log(docs_count / df, 10)


def get_doc_term_matrix(trie, type):
    dictionary, doc_ids = np.array(trie.WORDS), np.array(list(trie.DOCS.keys()))
    terms_count, docs_count = len(dictionary), len(doc_ids)

    doc_term_matrix = np.zeros(shape=(docs_count, terms_count))
    # Filling the Matrix
    for term_idx in range(len(dictionary)):
        postings_list = trie.get_postings_list(dictionary[term_idx])
        df = len(postings_list)

        for doc_id in postings_list:
            doc_idx = np.argwhere(doc_ids == doc_id)[0][0]
            tf = len(postings_list[doc_id])
            if tf == 0:
                doc_term_matrix[doc_idx][term_idx] = 0
            else:
                doc_term_matrix[doc_idx][term_idx] = get_weight(tf, df, type[:2])

    if type[2] == 'c':  # Normalizing Document Vectors
        doc_term_matrix = normalize_rows(doc_term_matrix)

    return doc_term_matrix


def get_query_vector(query, type):
    query_vector = np.zeros(terms_count)
    for term_idx in range(len(dictionary)):
        postings_list = trie.get_postings_list(dictionary[term_idx])
        df = len(postings_list)
        tf = np.count_nonzero(query == dictionary[term_idx])
        if tf == 0:
            query_vector[term_idx] = 0
        else:
            query_vector[term_idx] = get_weight(tf, df, type[:2])

    if type[2] == 'c':  # Normalizing Query Vector
        query_vector = query_vector / np.linalg.norm(query_vector)

    return query_vector


if __name__ == "__main__":
    doc_vector_type = 'ltc'
    query_vector_type = 'lnc'

    while True:
        cmd = input('Enter your command.\n').lower()
        cmd = shlex.split(cmd)

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'addtrie':  # Example: addtrie store_file
            dir = cmd[1]
            with open(dir, 'r') as f:
                input_dict = json.load(f)
                trie = idx.TrieNode.from_dict(input_dict)

        elif cmd[0] == 'wgscheme':  # Example: wgscheme ltc lnc
            doc_vector_type = cmd[1]  # Default: ltc
            query_vector_type = cmd[2]  # Default: lnc

        elif cmd[0] == 'vecspc':  # Example: vecspc
            dictionary, doc_ids = np.array(trie.WORDS), np.array(list(trie.DOCS.keys()))
            terms_count, docs_count = len(dictionary), len(doc_ids)
            doc_term_matrix = get_doc_term_matrix(trie, doc_vector_type)

        elif cmd[0] == 'save':
            np.savetxt('vecspc.txt', doc_term_matrix)

        elif cmd[0] == 'search':  # Example: search normal "seek system" OR search proximity "seek system" 5
            search_type = cmd[1]  # normal or proximity
            query = cmd[2]
            window = math.inf
            if search_type == 'proximity':
                window = cmd[3]

            # Preprocess Query
            query = np.array(nrm.normalize_english(query))
            # query enhancement

            # Get Query Vector
            query_vector = get_query_vector(query, query_vector_type)

            # Search
            results, scores = [], []
            if search_type == 'normal':
                results, scores = normal_search(query_vector, doc_term_matrix, doc_ids)
            elif search_type == 'proximity':
                proximity_query = ProximityQuery(query, window)
                results, scores = proximity_search(proximity_query, doc_term_matrix, doc_ids)

            print('Search results for ' + str(query) + ':')
            print(results)
            print(scores)
