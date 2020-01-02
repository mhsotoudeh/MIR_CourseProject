import Phase_2__Utility_Functions as uf
import numpy as np


def get_tag(word_list):
    probs = []
    for i in range(1, 5):
        probs.append(tag_sums[i] / sum(tag_sums))
    for word in word_list:
        if word not in probabilities:
            continue
        for tag in range(4):
            probs[tag] *= probabilities[word][tag]
    return probs.index(max(probs)) + 1


def naive_bayes_classification():
    normalized_doc_term_matrix, dictionary, tags, tag_sums, _ = uf.get_tf_idf_vector_space('data/raw/phase2_train.csv')

    probabilities = dict()
    for term_idx in range(len(dictionary)):
        le_word = dictionary[term_idx]
        probabilities[le_word] = []
        for tag in [1, 2, 3, 4]:
            probabilities[le_word].append(
                np.sum(normalized_doc_term_matrix[tags[tag], term_idx]) / tag_sums[tag]
            )

    uf.print_stats_nb(get_tag, 'data/raw/phase2_test.csv')
