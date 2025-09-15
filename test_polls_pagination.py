#!/usr/bin/env python3
"""
Test script for the fetch_polls function
Run this script to test the polls fetching functionality
"""

from fetch_polls import fetch_polls, fetch_all_polls, display_polls
import time
import json

def test_polls_pagination():
    """Test the fetch_polls function with various pagination scenarios"""
    
    print("🧪 Testing Polls Pagination Function")
    print("=" * 60)
    
    # Test cases for pagination
    test_cases = [
        {
            "name": "Default pagination (first 10)",
            "skip": 0,
            "limit": 10,
            "description": "Test default pagination behavior"
        },
        {
            "name": "Small page size",
            "skip": 0,
            "limit": 3,
            "description": "Test with smaller page size"
        },
        {
            "name": "Second page",
            "skip": 3,
            "limit": 3,
            "description": "Test fetching the second page"
        },
        {
            "name": "Large page size",
            "skip": 0,
            "limit": 50,
            "description": "Test with larger page size"
        },
        {
            "name": "High skip value",
            "skip": 1000,
            "limit": 10,
            "description": "Test with high skip value (likely empty result)"
        },
        {
            "name": "Minimal request",
            "skip": 0,
            "limit": 1,
            "description": "Test fetching just one poll"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        print(f"   Parameters: skip={test_case['skip']}, limit={test_case['limit']}")
        
        result = fetch_polls(
            skip=test_case['skip'],
            limit=test_case['limit']
        )
        
        if result.get('success'):
            polls_count = len(result['data'])
            print(f"   ✅ Success! Retrieved {polls_count} polls")
            
            # Show summary of first poll if any exist
            if polls_count > 0:
                first_poll = result['data'][0]
                print(f"   📄 First poll: \"{first_poll.get('question', 'N/A')[:50]}...\"")
            
            # Show pagination info
            pagination = result.get('pagination', {})
            print(f"   📊 Pagination: skip={pagination.get('skip')}, limit={pagination.get('limit')}, returned={pagination.get('returned_count')}")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Small delay between requests to be gentle on the API
        time.sleep(0.5)
    
    print(f"\n{'=' * 60}")
    print("🏁 Pagination testing completed!")


def test_fetch_all_polls():
    """Test the fetch_all_polls function"""
    
    print(f"\n{'=' * 60}")
    print("🧪 Testing Fetch All Polls Function")
    print("=" * 60)
    
    print("\n📋 Test: Fetch all polls (limited to 15 for demo)")
    result = fetch_all_polls(max_polls=15, page_size=5)
    
    if result.get('success'):
        total_polls = result.get('total_count', 0)
        total_requests = result.get('pagination_info', {}).get('total_requests', 0)
        
        print(f"✅ Success! Retrieved {total_polls} polls total")
        print(f"🔄 Made {total_requests} API requests")
        
        # Display first few polls as sample
        if result['data']:
            print(f"\n🔍 Sample of retrieved polls:")
            display_polls(result['data'][:2])  # Show first 2 polls
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")


def test_display_function():
    """Test the display_polls function with sample data"""
    
    print(f"\n{'=' * 60}")
    print("🧪 Testing Display Function with Sample Data")
    print("=" * 60)
    
    # Sample poll data matching the API schema
    sample_polls = [
        {
            "id": 1,
            "question": "What's your favorite programming language?",
            "created_at": "2024-01-15T10:30:00Z",
            "owner_id": 101,
            "options": [
                {"id": 1, "text": "Python", "poll_id": 1},
                {"id": 2, "text": "JavaScript", "poll_id": 1},
                {"id": 3, "text": "Go", "poll_id": 1}
            ]
        },
        {
            "id": 2,
            "question": "Best time for daily standup?",
            "created_at": "2024-01-16T09:00:00Z",
            "owner_id": 102,
            "options": [
                {"id": 4, "text": "9:00 AM", "poll_id": 2},
                {"id": 5, "text": "10:00 AM", "poll_id": 2},
                {"id": 6, "text": "11:00 AM", "poll_id": 2}
            ]
        }
    ]
    
    print("📄 Displaying sample polls:")
    display_polls(sample_polls)


def main():
    """Run all tests"""
    print("=== Polly-API Polls Fetcher Test Suite ===\n")
    
    try:
        # Test basic pagination
        test_polls_pagination()
        
        # Test fetch all polls
        test_fetch_all_polls()
        
        # Test display function
        test_display_function()
        
        print(f"\n{'=' * 60}")
        print("🎉 All tests completed!")
        print("\n💡 To use the functions in your code:")
        print("   from fetch_polls import fetch_polls, fetch_all_polls")
        print("   result = fetch_polls(skip=0, limit=10)")
        print("   all_polls = fetch_all_polls(max_polls=100, page_size=20)")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during testing: {str(e)}")


if __name__ == "__main__":
    main()