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


def proximity_search(tokenized_query, query, window):
    # Find Docs with All Words Present
    query_terms = np.array([])
    for term in tokenized_query:
        np.append(query_terms, np.where(dictionary == term))

    eligible_documents = []
    eligible_document_ids = []
    for i in range(normalized_doc_term_matrix):
        row = normalized_doc_term_matrix[i]
        eligible = True
        for term in query_terms:
            if row[term] == 0.0:
                eligible = False
        if eligible is True:
            eligible_documents.append(row)
            eligible_document_ids.append(i)

    # Find Docs with Words Inside the Window
    valid_documents = []
    valid_document_ids = []
    # Proximity Intersection

    # Search Between Valid Documents and Return Results and Scores
    results, scores = normal_search(query, valid_documents, valid_document_ids)
    return results, scores


# Determine search type
search_type = 'normal' # Or 'proximity'
query = 'seek'
proximity_query = ProximityQuery('akbar is bad', 5)

# Load docs trie
with open('store_file', 'r') as f:
    input_dict = json.load(f)
    trie = idx.TrieNode.from_dict(input_dict)

dictionary, docs = trie.WORDS, list(trie.DOCS.keys())
terms_count, docs_count = len(dictionary), len(docs)

doc_term_matrix = np.zeros(shape=(docs_count, terms_count))
# Filling the Matrix
for term_idx in range(len(dictionary)):
    postings_list = trie.get_postings_list(dictionary[term_idx])
    df = len(postings_list)

    for doc in postings_list:
        doc_idx = docs.index(doc)
        tf = len(postings_list[doc])
        if tf == 0:
            doc_term_matrix[doc_idx][term_idx] = 0
        else:
            doc_term_matrix[doc_idx][term_idx] = (1 + math.log(tf, 10)) * math.log(docs_count/df, 10)

# Normalizing Document Vectors
normalized_doc_term_matrix = normalize_rows(doc_term_matrix)


# Preprocess Query
if search_type == 'normal':
    query = nrm.normalize_english(query)
    # query enhancement
elif search_type == 'proximity':
    proximity_query.query = nrm.normalize_english(proximity_query.query)
    # query enhancement

# Find Query Vector
query_vector = np.zeros(terms_count)
for term_idx in range(len(dictionary)):
    postings_list = trie.get_postings_list(dictionary[term_idx])
    df = len(postings_list)
    tf = query.count(dictionary[term_idx])
    if tf == 0:
        query_vector[term_idx] = 0
    else:
        query_vector[term_idx] = 1 + math.log(tf, 10)

normalized_query_vector = query_vector / np.linalg.norm(query_vector)


# Search
if search_type == 'normal':
    results, scores = normal_search(query_vector, normalized_doc_term_matrix, docs)
elif search_type == 'proximity':
    results, scores = proximity_search(proximity_query.query, query_vector, proximity_query.window_size)

print('Search results for ' + str(query) + ':')
print(results)
print(scores)