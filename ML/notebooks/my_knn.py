import numpy as np
from collections import Counter

class MyKNNClassifier:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def _euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def predict(self, X):
        X = np.array(X)
        predictions = [self._predict_one(x) for x in X]
        return np.array(predictions)

    def _predict_one(self, x):
        # 1. Расчет расстояний до всех точек
        distances = [self._euclidean_distance(x, x_train) for x_train in self.X_train]
        
        # 2. Получение индексов k ближайших соседей
        k_indices = np.argsort(distances)[:self.k]
        
        # 3. Получение меток этих соседей
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        
        # 4. Голосование (самый частый класс)
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]