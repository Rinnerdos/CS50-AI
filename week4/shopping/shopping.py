import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence_raw = list()
    labels_raw = list()
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'Administrative':
                continue
            
            evidence_raw.append(row[0:17])
            labels_raw.append(row[17])

    # Now loop over the raw evidence and raw labels
    # as to clean them up

    evidence = evidence_raw.copy()
    labels = labels_raw.copy()

    for i in range(len(evidence_raw)):
        for j in range(len(evidence_raw[i])):
            if j == 10:
                if evidence_raw[i][j] == "Jan":
                    evidence[i][j] = 0
                elif evidence_raw[i][j] == "Feb":
                    evidence[i][j] = 1
                elif evidence_raw[i][j] == "Mar":
                    evidence[i][j] = 2
                elif evidence_raw[i][j] == "Apr":
                    evidence[i][j] = 3
                elif evidence_raw[i][j] == "May":
                    evidence[i][j] = 4
                elif evidence_raw[i][j] == "June":
                    evidence[i][j] = 5
                elif evidence_raw[i][j] == "Jul":
                    evidence[i][j] = 6
                elif evidence_raw[i][j] == "Aug":
                    evidence[i][j] = 7
                elif evidence_raw[i][j] == "Sep":
                    evidence[i][j] = 8
                elif evidence_raw[i][j] == "Oct":
                    evidence[i][j] = 9
                elif evidence_raw[i][j] == "Nov":
                    evidence[i][j] = 10
                elif evidence_raw[i][j] == "Dec":
                    evidence[i][j] = 11
            
            if j == 15:
                if evidence_raw[i][j] == "Returning_Visitor":
                    evidence[i][j] = 1
                else:
                    evidence[i][j] = 0
            if j == 16:
                if evidence_raw[i][j] == "TRUE":
                    evidence[i][j] = 1
                else:
                    evidence[i][j] = 0

            int_list = [0, 2, 4, 11, 12, 13, 14]
            float_list = [1, 3, 5, 6, 7, 8, 9]

            if j in int_list:
                evidence[i][j] = int(evidence[i][j])
            elif j in float_list:
                evidence[i][j] = float(evidence[i][j])


    for i in range(len(labels_raw)):
        if labels_raw[i] == 'TRUE':
            labels[i] = int(1)
        else:
            labels[i] = int(0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors= 1)

    return model.fit(evidence, labels)
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_correct = 0
    negative_correct = 0
    positive_false = 0
    negative_false = 0

    for actual, predicted in zip(labels, predictions):
        if (actual == predicted) and (actual == 0):
            negative_correct += 1
        elif (actual == predicted) and (actual == 1):
            positive_correct += 1
        elif actual != predicted and (actual == 0):
            negative_false += 1
        elif actual != predicted and (actual == 1):
            positive_false += 1

    sensitivity = positive_correct  / (positive_correct + positive_false)
    specificity = negative_correct / (negative_correct + negative_false)

    return (sensitivity, specificity)
        

if __name__ == "__main__":
    main()
