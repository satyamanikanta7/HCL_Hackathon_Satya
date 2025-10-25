def test_basic_math():
    """Test basic math operations."""
    assert 2 + 2 == 4
    assert 3 * 3 == 9

def test_string_operations():
    """Test basic string operations."""
    text = "Hello World"
    assert len(text) == 11
    assert "Hello" in text

def test_list_operations():
    """Test basic list operations."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert max(numbers) == 5
    assert min(numbers) == 1

def test_dictionary_operations():
    """Test basic dictionary operations."""
    data = {"name": "John", "age": 30}
    assert "name" in data
    assert data["age"] == 30
