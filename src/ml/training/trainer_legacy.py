from sklearn.model_selection import train_test_split

def train_model(model, X, y, test_size=0.2, random_state=42):
    """
    Generic trainer for any model implementing BaseModel.
    Splits data, trains the model, returns predictions and true labels.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=False
    )

    model.train(X_train, y_train)
    preds = model.predict(X_test)

    return preds, y_test
