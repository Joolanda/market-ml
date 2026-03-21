class BaseModel:
    def train(self, X_train, y_train):
        """Train the model on training data."""
        raise NotImplementedError("train() must be implemented by subclasses")

    def predict(self, X):
        """Predict labels for input data."""
        raise NotImplementedError("predict() must be implemented by subclasses")

    def evaluate(self, X_test, y_test):
        """Return accuracy score or other metrics."""
        preds = self.predict(X_test)
        return (preds == y_test).mean()

