from sklearn.metrics import precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
import utility_functions as uf

normalized_doc_term_matrix, dictionary, _, _, tag_list = uf.get_tf_idf_vector_space('data/raw/phase2_train.csv')
clf = RandomForestClassifier(random_state=0)
clf.fit(normalized_doc_term_matrix, tag_list)

test_doc_term_matrix, test_tags = uf.tf_idf_from_dict('data/raw/phase2_test.csv', dictionary)
print('*** Random Forest ***')
print('Accuracy =', clf.score(test_doc_term_matrix, test_tags))
print()
pred_tags = clf.predict(test_doc_term_matrix)
precision = precision_score(test_tags, pred_tags, average=None)
recall = recall_score(test_tags, pred_tags, average=None)
for tag in range(4):
    print('class', tag + 1, 'precision and recall')
    print('precision = ', precision[tag])
    print('recall =', recall[tag])
    print('f1 = ', 2 * precision[tag] * recall[tag] / (precision[tag] + recall[tag]))
    print()
