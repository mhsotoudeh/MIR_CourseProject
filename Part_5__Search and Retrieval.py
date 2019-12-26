import numpy as np
import Part_1__Normalization as nrm
import Part_2__Indexing as idx
import Part_3__Index_Comperssion as ic
import json
import sys
import math


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


def proximity_intersection():
    pass


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


# Load docs trie
with open('store_file', 'r') as f:
    input_dict = json.load(f)
    trie = idx.TrieNode.from_dict(input_dict)

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
            doc_term_matrix[doc_idx][term_idx] = (1 + math.log(tf, 10)) * math.log(docs_count/df, 10)

# Normalizing Document Vectors
normalized_doc_term_matrix = normalize_rows(doc_term_matrix)

# Determine search type
search_type = 'proximity' # Or 'proximity'
query = 'seek second'
window = 5

# Preprocess Query
query = np.array(nrm.normalize_english(query))
# query enhancement

# Find Query Vector
query_vector = np.zeros(terms_count)
for term_idx in range(len(dictionary)):
    postings_list = trie.get_postings_list(dictionary[term_idx])
    df = len(postings_list)
    tf = np.count_nonzero(query == dictionary[term_idx])
    if tf == 0:
        query_vector[term_idx] = 0
    else:
        query_vector[term_idx] = 1 + math.log(tf, 10)

normalized_query_vector = query_vector / np.linalg.norm(query_vector)


# Search
if search_type == 'normal':
    results, scores = normal_search(query_vector, normalized_doc_term_matrix, doc_ids)
elif search_type == 'proximity':
    proximity_query = ProximityQuery(query, window)
    results, scores = proximity_search(proximity_query, normalized_doc_term_matrix, doc_ids)

print('Search results for ' + str(query) + ':')
print(results)
print(scores)