import requests
import json
import time

def test_complete_system():
    """Test all system components"""
    print("🚀 COMPLETE SYSTEM TEST - MATH ROUTING AGENT")
    print("=" * 70)
    
    base_url = "http://localhost:8000"
    
    # Test scenarios
    test_cases = [
        {
            "question": "Solve x^2 - 5x + 6 = 0",
            "type": "KB_MATCH",
            "description": "Knowledge Base hit - quadratic equation"
        },
        {
            "question": "Find derivative of x^3 * sin(x)",
            "type": "WEB_SEARCH", 
            "description": "Web search required - complex calculus"
        },
    ]