import joblib 
from app.utils.logger import get_logger
from app.utils.exception import ModelLoadError, PredictionError, InvalidInputError, TypeError

logger = get_logger()
MODEL__PATH = "/models/iris_model.pkl"

def load_model():
    """
    Load the pre-trained model from the specified path.

    Returns:
        model: The loaded machine learning model.
    """

    try: 
        model = joblib.load(MODEL__PATH)
        logger.info(f"Model loaded successfully from {MODEL__PATH}.")
        return model
    except FileNotFoundError:
        raise ModelLoadError("Failed to load the model {e}.")

class_names = ['setosa', 'versicolor', 'virginica']
def predict(features): 
    """
    Predict the class of the iris flower based on input features.

    Args:
        features (list): A list of features [sepal_length, sepal_width, petal_length, petal_width].

    Returns:
        int: Predicted class label (0, 1, or 2).
    """
    if len(features) != 4:
        raise InvalidInputError("Expected 4 features for prediction.")

    if not all(isinstance(value, (int, float)) for value in features):
        raise TypeError("All features must be numeric.")
    
    prediction = load_model().predict([features])
    class_id = int(prediction[0])  # Convert the prediction to an integer class label

    return {
        "prediction": class_names[class_id],
        "class_id": class_id,
        "confidence":0.9
    }