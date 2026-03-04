import numpy as np

def calculate_confusion_matrix(y_true, y_pred):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    for i in range(len(y_true)):
        if y_true[i] == 1 and y_pred[i] == 1:
            TP += 1
        elif y_true[i] == 0 and y_pred[i] == 0:
            TN += 1
        elif y_true[i] == 0 and y_pred[i] == 1:
            FP += 1
        elif y_true[i] == 1 and y_pred[i] == 0:
            FN += 1
            
    return [[TN, FP], [FN, TP]]

def accuracy(y_true, y_pred):
    cm = calculate_confusion_matrix(y_true, y_pred)
    TN, FP = cm[0]
    FN, TP = cm[1]
    return (TP + TN) / (TP + TN + FP + FN)

def precision(y_true, y_pred):
    cm = calculate_confusion_matrix(y_true, y_pred)
    TN, FP = cm[0]
    FN, TP = cm[1]
    if (TP + FP) == 0: return 0
    return TP / (TP + FP)

def recall(y_true, y_pred):
    cm = calculate_confusion_matrix(y_true, y_pred)
    TN, FP = cm[0]
    FN, TP = cm[1]
    if (TP + FN) == 0: return 0
    return TP / (TP + FN)

def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    if (p + r) == 0: return 0
    return 2 * (p * r) / (p + r)