#!/usr/bin/env python3
"""
Simple test script to demonstrate the register_user function
Run this script to test the user registration functionality
"""

from register_user import register_user
import time

def test_registration():
    """Test the user registration function with various scenarios"""
    
    print("🧪 Testing User Registration Function")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Valid Registration #1",
            "username": "alice_test",
            "password": "test_password_123",
            "expected_success": True
        },
        {
            "name": "Valid Registration #2", 
            "username": "bob_test",
            "password": "another_test_pass",
            "expected_success": True
        },
        {
            "name": "Duplicate Username",
            "username": "alice_test",  # Same as first test
            "password": "different_password",
            "expected_success": False
        },
        {
            "name": "Short Username",
            "username": "a",
            "password": "test_password",
            "expected_success": True  # Assuming API allows short usernames
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   Username: {test_case['username']}")
        print(f"   Password: {'*' * len(test_case['password'])}")
        
        result = register_user(
            username=test_case['username'],
            password=test_case['password']
        )
        
        # Check if result matches expectation
        if result.get('success') == test_case['expected_success']:
            print(f"   ✅ Test passed!")
        else:
            print(f"   ❌ Test failed! Expected success={test_case['expected_success']}, got success={result.get('success')}")
        
        # Small delay between requests
        time.sleep(0.5)
    
    print(f"\n{'=' * 50}")
    print("🏁 Testing completed!")
    print("\n💡 To run individual tests, import the register_user function:")
    print("   from register_user import register_user")
    print("   result = register_user('your_username', 'your_password')")

if __name__ == "__main__":
    test_registration()