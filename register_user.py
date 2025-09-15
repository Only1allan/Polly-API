#!/usr/bin/env python3
"""
User registration function using the requests library for the Polly-API.
"""

import requests
from typing import Dict, Any, Optional
import json


def register_user(
    username: str, 
    password: str, 
    base_url: str = "http://localhost:8000"
) -> Dict[str, Any]:
    """
    Register a new user via the /register endpoint.
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict[str, Any]: The response data containing user information or error details
    
    Raises:
        requests.exceptions.RequestException: If there's a network or HTTP error
    """
    url = f"{base_url}/register"
    
    # Prepare the request payload
    payload = {
        "username": username,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Parse the JSON response
        response_data = response.json()
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"✅ User '{username}' registered successfully!")
            print(f"User ID: {response_data.get('id')}")
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response_data
            }
        elif response.status_code == 400:
            print(f"❌ Registration failed: {response_data}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response_data
            }
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response_data
            }
            
    except requests.exceptions.ConnectionError:
        error_msg = f"❌ Could not connect to the API at {base_url}. Make sure the server is running."
        print(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
    except requests.exceptions.JSONDecodeError:
        error_msg = f"❌ Invalid JSON response from server"
        print(error_msg)
        return {
            "success": False,
            "error": error_msg
        }
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Request failed: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "error": error_msg
        }


def main():
    """
    Example usage of the register_user function.
    """
    print("=== Polly-API User Registration ===\n")
    
    # Example 1: Successful registration
    print("Example 1: Registering a new user")
    result1 = register_user("john_doe", "secure_password123")
    print(f"Result: {json.dumps(result1, indent=2)}\n")
    
    # Example 2: Trying to register the same user again (should fail)
    print("Example 2: Trying to register the same user again")
    result2 = register_user("john_doe", "secure_password123")
    print(f"Result: {json.dumps(result2, indent=2)}\n")
    
    # Example 3: Registering another user
    print("Example 3: Registering another user")
    result3 = register_user("jane_smith", "another_password456")
    print(f"Result: {json.dumps(result3, indent=2)}")


if __name__ == "__main__":
    main()