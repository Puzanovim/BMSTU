from sklearn import metrics
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPClassifier


digits = load_digits()

print(digits.data.shape)

for i, layers in enumerate(((),)):
    for test_size in range(1, 10):
        x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=test_size / 10)
        print(x_train.shape)
        print(x_test.shape)
        print(y_train.shape)
        print(y_test.shape)
        clf = MLPClassifier(solver='lbfgs', activation='relu', hidden_layer_sizes=layers, max_iter=5000)
        clf.fit(x_train, y_train)
        train_predicted = clf.predict(x_train)
        test_predicted = clf.predict(x_test)

        print(f'---------- Training for {test_size / 10} with {layers} shapes {x_train.shape[0]} {x_test.shape[0]} -------- ')
        print('Accuracy')
        print('For train: ', metrics.accuracy_score(y_train, train_predicted))
        print('For test: ', metrics.accuracy_score(y_test, test_predicted))
        print('Precision')
        print('For train: ', metrics.precision_score(y_train, train_predicted, average='micro'))
        print('For test: ', metrics.precision_score(y_test, test_predicted, average='micro'))
        print('Recall')
        print('For train: ', metrics.recall_score(y_train, train_predicted, average='micro'))
        print('For test: ', metrics.recall_score(y_test, test_predicted, average='micro'))
        print()
