class ModelLoadError(Exception):
    """Exception raised when a model fails to load."""
    pass

class PredictionError(Exception):
    """Exception raised when a prediction fails."""
    pass

class InvalidInputError(Exception):
    """Exception raised for invalid input features."""
    pass

class TypeError(Exception):
    """Exception raised for invalid input types."""
    pass