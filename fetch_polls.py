#!/usr/bin/env python3
"""
Fetch paginated poll data from the Polly-API /polls endpoint.
"""

import requests
from typing import Dict, Any, List, Optional
import json
from datetime import datetime


def fetch_polls(
    skip: int = 0,
    limit: int = 10,
    base_url: str = "http://localhost:8000"
) -> Dict[str, Any]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict[str, Any]: The response data containing polls list or error details
        
        Success response structure:
        {
            "success": True,
            "status_code": 200,
            "data": [
                {
                    "id": int,
                    "question": str,
                    "created_at": str (ISO datetime),
                    "owner_id": int,
                    "options": [
                        {
                            "id": int,
                            "text": str,
                            "poll_id": int
                        }
                    ]
                }
            ],
            "pagination": {
                "skip": int,
                "limit": int,
                "returned_count": int
            }
        }
    
    Raises:
        requests.exceptions.RequestException: If there's a network or HTTP error
    """
    url = f"{base_url}/polls"
    
    # Prepare query parameters
    params = {
        "skip": skip,
        "limit": limit
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params, headers=headers)
        
        # Parse the JSON response
        response_data = response.json()
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"✅ Successfully fetched {len(response_data)} polls")
            print(f"📄 Pagination: skip={skip}, limit={limit}")
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response_data,
                "pagination": {
                    "skip": skip,
                    "limit": limit,
                    "returned_count": len(response_data)
                }
            }
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
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


def fetch_all_polls(
    base_url: str = "http://localhost:8000",
    page_size: int = 10,
    max_polls: Optional[int] = None
) -> Dict[str, Any]:
    """
    Fetch all polls using pagination, automatically handling multiple requests.
    
    Args:
        base_url (str): The base URL of the API
        page_size (int): Number of polls to fetch per request (default: 10)
        max_polls (Optional[int]): Maximum number of polls to fetch (None for all)
    
    Returns:
        Dict[str, Any]: Combined response with all polls
    """
    all_polls = []
    skip = 0
    total_fetched = 0
    
    print(f"🔄 Starting to fetch all polls (page size: {page_size})")
    
    while True:
        # Calculate limit for this request
        if max_polls is not None:
            remaining = max_polls - total_fetched
            if remaining <= 0:
                break
            current_limit = min(page_size, remaining)
        else:
            current_limit = page_size
        
        # Fetch current page
        result = fetch_polls(skip=skip, limit=current_limit, base_url=base_url)
        
        if not result.get("success"):
            return result
        
        current_polls = result["data"]
        
        # If no polls returned, we've reached the end
        if not current_polls:
            break
        
        all_polls.extend(current_polls)
        total_fetched += len(current_polls)
        skip += len(current_polls)
        
        print(f"📊 Fetched {len(current_polls)} polls, total so far: {total_fetched}")
        
        # If we got fewer polls than requested, we've reached the end
        if len(current_polls) < current_limit:
            break
    
    print(f"✅ Completed! Total polls fetched: {total_fetched}")
    
    return {
        "success": True,
        "data": all_polls,
        "total_count": total_fetched,
        "pagination_info": {
            "page_size": page_size,
            "total_requests": (skip // page_size) + (1 if skip % page_size > 0 else 0)
        }
    }


def display_polls(polls_data: List[Dict[str, Any]]) -> None:
    """
    Display polls in a formatted way.
    
    Args:
        polls_data: List of poll dictionaries from the API response
    """
    if not polls_data:
        print("📭 No polls to display")
        return
    
    print(f"\n📊 Displaying {len(polls_data)} polls:")
    print("=" * 60)
    
    for poll in polls_data:
        # Parse and format the created_at timestamp
        try:
            created_at = datetime.fromisoformat(poll["created_at"].replace("Z", "+00:00"))
            formatted_date = created_at.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, KeyError):
            formatted_date = poll.get("created_at", "Unknown")
        
        print(f"\n🗳️  Poll ID: {poll.get('id', 'N/A')}")
        print(f"❓ Question: {poll.get('question', 'N/A')}")
        print(f"👤 Owner ID: {poll.get('owner_id', 'N/A')}")
        print(f"📅 Created: {formatted_date}")
        
        # Display options
        options = poll.get("options", [])
        if options:
            print("📝 Options:")
            for i, option in enumerate(options, 1):
                print(f"   {i}. {option.get('text', 'N/A')} (ID: {option.get('id', 'N/A')})")
        else:
            print("📝 Options: None")
        
        print("-" * 40)


def main():
    """
    Example usage of the fetch_polls functions.
    """
    print("=== Polly-API Poll Fetcher ===\n")
    
    # Example 1: Fetch first page of polls
    print("Example 1: Fetch first 5 polls")
    result1 = fetch_polls(skip=0, limit=5)
    if result1.get("success"):
        display_polls(result1["data"])
    else:
        print(f"Error: {result1.get('error')}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 2: Fetch next page
    print("Example 2: Fetch next 5 polls (skip=5)")
    result2 = fetch_polls(skip=5, limit=5)
    if result2.get("success"):
        display_polls(result2["data"])
    else:
        print(f"Error: {result2.get('error')}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 3: Fetch all polls (limited to 20 for demo)
    print("Example 3: Fetch all polls (max 20)")
    result3 = fetch_all_polls(max_polls=20, page_size=10)
    if result3.get("success"):
        print(f"\n📊 Summary: Fetched {result3['total_count']} polls total")
        print(f"🔄 Made {result3['pagination_info']['total_requests']} API requests")
        # Display first few polls as preview
        if result3["data"]:
            print("\n🔍 Preview of first few polls:")
            display_polls(result3["data"][:3])  # Show first 3 polls
    else:
        print(f"Error: {result3.get('error')}")


if __name__ == "__main__":
    main()