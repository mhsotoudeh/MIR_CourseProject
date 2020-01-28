import Phase_2__Utility_Functions as uf
from scipy import stats
import numpy as np


def get_tag(target_row, k):
    neighbors = []
    for i in range(len(normalized_doc_term_matrix)):
        dist = np.linalg.norm(target_row - normalized_doc_term_matrix[i])
        neighbors.append((i, dist))
        neighbors.sort(key=lambda x: x[1])
        if len(neighbors) > k:
            neighbors.pop(-1)

    results = []
    for neighbor in neighbors:
        results.append(tag_list[neighbor[0]])
    return stats.mode(results, axis=None)[0][0]


def knn_classification():
    global normalized_doc_term_matrix, tag_list
    normalized_doc_term_matrix, dictionary, _, _, tag_list = uf.get_tf_idf_vector_space('data/raw/phase2_train.csv')
    ks = [1, 5, 9]
    k = 9

    test_doc_term_matrix, test_tags = uf.tf_idf_from_dict('data/raw/phase2_test.csv', dictionary)
    assert len(test_doc_term_matrix) == len(test_tags)
    count = [0, 0, 0, 0]
    pred = [0, 0, 0, 0]
    true_pred = [0, 0, 0, 0]

    for i in range(len(test_tags)):
        pred_tag = get_tag(test_doc_term_matrix[i], k)
        count[test_tags[i] - 1] += 1
        pred[pred_tag - 1] += 1
        if test_tags[i] == pred_tag:
            true_pred[test_tags[i] - 1] += 1
    print('*** K-NN ***')
    print('Accuracy =', sum(true_pred) / sum(count))
    print()
    for tag in range(4):
        print('class', tag + 1, 'precision and recall')
        print('precision =', true_pred[tag] / pred[tag])
        print('recall =', true_pred[tag] / count[tag])
        print('f1 = ', 2 * (true_pred[tag] / pred[tag]) * (true_pred[tag] / count[tag]) / (
                (true_pred[tag] / pred[tag]) + (true_pred[tag] / count[tag])))
        print()

    test_doc_term_matrix, test_tags = normalized_doc_term_matrix, tag_list
    assert len(test_doc_term_matrix) == len(test_tags)
    count = [0, 0, 0, 0]
    pred = [0, 0, 0, 0]
    true_pred = [0, 0, 0, 0]

    for i in range(len(test_tags)):
        pred_tag = get_tag(test_doc_term_matrix[i], k)
        count[test_tags[i] - 1] += 1
        pred[pred_tag - 1] += 1
        if test_tags[i] == pred_tag:
            true_pred[test_tags[i] - 1] += 1
    print('*** K-NN ***')
    print('Accuracy =', sum(true_pred) / sum(count))
    print()
    for tag in range(4):
        print('class', tag + 1, 'precision and recall')
        print('precision =', true_pred[tag] / pred[tag])
        print('recall =', true_pred[tag] / count[tag])
        print('f1 = ', 2 * (true_pred[tag] / pred[tag]) * (true_pred[tag] / count[tag]) / (
                (true_pred[tag] / pred[tag]) + (true_pred[tag] / count[tag])))
        print()
