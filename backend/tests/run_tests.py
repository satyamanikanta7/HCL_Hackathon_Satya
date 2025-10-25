import subprocess
import sys
import os

def run_tests():
    """Run all tests in the tests directory."""
    print("Running simple tests for Fraud Detection System...")
    print("=" * 50)
    
    # Change to the backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(backend_dir)
    
    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n All tests completed successfully!")
    else:
        print("\n Some tests failed (this may be expected)")
    
    sys.exit(0 if success else 1)
