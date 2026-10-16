import pytest 
from app.services.model_service import predict


@pytest.mark.unit
def test_prediction_returns_valid_structure():
    features = [5.2,1.4,3.2,4.0]
    
    result = predict(features)
    
    assert isinstance(result, dict)
    assert "prediction" in result 
    assert "class_id" in result 
    assert 0.0 <= result["confidence"] <= 1.0
    
    assert result["prediction"] in ["setosa", 'virginica', 'versicolor']
    
    assert result["class_id"] in [0,1,2]
    
# @pytest.mark.unit
# def test_basic_calculation():
#     result = 2+3
    
#     assert result ==5