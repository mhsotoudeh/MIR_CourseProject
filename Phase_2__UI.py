import shlex
import Phase_2__KNN as knn
import Phase_2__Naive_Bayes as nvb
import Phase_2__Random_Forest as rfs
import Phase_2__SVM as svc

if __name__ == "__main__":
    while True:
        cmd = input('Enter your command.\n').lower()
        cmd = shlex.split(cmd)

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'knn':
            knn.knn_classification()

        elif cmd[0] == 'nvb':
            nvb.naive_bayes_classification()

        elif cmd[0] == 'rfs':
            rfs.random_forest_classification()

        elif cmd[0] == 'svm':
            svc.svm_classification()