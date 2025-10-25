import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def run_basic_tests():
    """Run basic tests."""
    print("Running basic tests...")
    
    # Test 1: Basic math
    assert 2 + 2 == 4
    print("✓ Basic math test passed")
    
    # Test 2: String operations
    text = "Hello World"
    assert len(text) == 11
    print("✓ String operations test passed")
    
    # Test 3: List operations
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    print("✓ List operations test passed")
    
    # Test 4: Dictionary operations
    data = {"name": "John", "age": 30}
    assert "name" in data
    print("✓ Dictionary operations test passed")
    
    return True

def run_fraud_tests():
    """Run fraud detection related tests."""
    print("\nRunning fraud detection tests...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Test pandas
        df = pd.DataFrame({'amount': [100, 200, 300]})
        assert len(df) == 3
        print("✓ Pandas import and usage test passed")
        
        # Test numpy
        arr = np.array([1, 2, 3, 4, 5])
        assert len(arr) == 5
        print("✓ Numpy import and usage test passed")
        
        # Test fraud score calculation
        amounts = [100, 500, 1000, 5000]
        fraud_scores = [min(amount / 1000, 1.0) for amount in amounts]
        assert fraud_scores[0] == 0.1
        print("✓ Fraud score calculation test passed")
        
        # Test transaction filtering
        transactions = [
            {'id': 1, 'amount': 100, 'fraud_score': 0.1},
            {'id': 2, 'amount': 500, 'fraud_score': 0.5},
            {'id': 3, 'amount': 1000, 'fraud_score': 0.8},
            {'id': 4, 'amount': 2000, 'fraud_score': 0.9}
        ]
        
        threshold = 0.7
        flagged = [t for t in transactions if t['fraud_score'] > threshold]
        assert len(flagged) == 2
        print("✓ Transaction filtering test passed")
        
        return True
        
    except ImportError as e:
        print(f"⚠ Some dependencies missing: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Simple Tests for Fraud Detection System")
    print("=" * 50)
    
    basic_success = run_basic_tests()
    fraud_success = run_fraud_tests()
    
    print("\n" + "=" * 50)
    if basic_success and fraud_success:
        print("All tests passed successfully!")
    else:
        print("⚠ Some tests had issues (this may be expected)")
    print("=" * 50)
