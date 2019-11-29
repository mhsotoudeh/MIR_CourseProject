import numpy as np


class DocVector:
    def __init__(self, dim):
        vector = []


def normalize_rows(matrix):
    return matrix / np.linalg.norm(matrix, ord=2, axis=1, keepdims=True)


# doc = ['akbar', 'be', 'lazy', 'go', 'swim', 'july']

query = 'akbar is bad'
proximity_query = 'akbar is bad', 5

terms_count = 100
docs_count = 10

dictionary = np.zeros(shape=(1, terms_count))
doc_id_list = np.zeros(shape=(1, docs_count))

doc_term_matrix = np.zeros(shape=(docs_count, terms_count))

# Filling the Matrix


# Normalizing Document Vectors
normalized_doc_term_matrix = normalize_rows(doc_term_matrix)


# Preprocess Query


# Find Query Vector
query_vector = np.zeros(shape=(1, terms_count))

# Scoring
scores = []
for i in range(len(normalized_doc_term_matrix)):
    score = np.dot(normalized_doc_term_matrix[i], query_vector)
    scores.append(score)

# Sort and Give Results
zipped_pairs = zip(scores, docs_list)
search_result = [x for _, x in sorted(zipped_pairs)]
search_result.reverse()


# For Test
# test = np.array([ [1, 1, 0], [3, 3, 3], [5, 0, 5] ])
# print(normalize_rows(test))
