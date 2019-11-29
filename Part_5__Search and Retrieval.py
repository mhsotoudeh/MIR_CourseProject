import numpy as np
import Part_1__Normalization as nrm


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


# doc = ['akbar', 'be', 'lazy', 'go', 'swim', 'july']

search_type = 'normal' # Or 'proximity'
query = 'akbar is bad'
proximity_query = ProximityQuery('akbar is bad', 5)

terms_count = 100
docs_count = 10

dictionary = np.zeros(shape=(1, terms_count))
doc_id_list = np.zeros(shape=(1, docs_count))

doc_term_matrix = np.zeros(shape=(docs_count, terms_count))

# Filling the Matrix


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
query_vector = np.zeros(shape=(1, terms_count))

# Search
if search_type == 'normal':
    results, scores = normal_search(query_vector, normalized_doc_term_matrix, doc_id_list)
elif search_type == 'proximity':
    results, scores = proximity_search(proximity_query.query, query_vector, proximity_query.window_size)


# For Test
# test = np.array([ [1, 1, 0], [3, 3, 3], [5, 0, 5] ])
# print(normalize_rows(test))
