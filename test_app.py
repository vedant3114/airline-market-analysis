#!/usr/bin/env python3
"""
Test script for the Airline Market Analysis application
"""

import requests
import json
from datetime import datetime, timedelta

def test_app():
    """Test the application endpoints"""
    base_url = "http://localhost:5000"
    
    print("🚀 Testing Airline Market Analysis Application")
    print("=" * 50)
    
    # Test 1: Check if the app is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Main page is accessible")
        else:
            print(f"❌ Main page returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to application: {e}")
        return
    
    # Test 2: Test data fetching
    print("\n📊 Testing Data Fetching...")
    test_data = {
        "origin": "SYD",
        "destination": "MEL",
        "date_from": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
        "date_to": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/fetch-data",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Data fetching successful")
                print(f"   - Total flights: {data['summary']['total_flights']}")
                print(f"   - Average price: ${data['summary']['avg_price']}")
                print(f"   - Price range: {data['summary']['price_range']}")
            else:
                print(f"❌ Data fetching failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Data fetching returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Data fetching error: {e}")
    
    # Test 3: Test chart generation
    print("\n📈 Testing Chart Generation...")
    chart_types = ['price_trend', 'airline_distribution', 'route_popularity', 'demand_heatmap']
    
    for chart_type in chart_types:
        try:
            response = requests.post(
                f"{base_url}/api/charts",
                json={"chart_type": chart_type},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ {chart_type} chart generated successfully")
                else:
                    print(f"❌ {chart_type} chart failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ {chart_type} chart returned status {response.status_code}")
        except Exception as e:
            print(f"❌ {chart_type} chart error: {e}")
    
    # Test 4: Test market analysis
    print("\n🔍 Testing Market Analysis...")
    try:
        response = requests.get(f"{base_url}/api/market-analysis")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Market analysis successful")
                analysis = data['analysis']
                print(f"   - Market size: {analysis['market_overview']['total_market_size']}")
                print(f"   - Major players: {len(analysis['competitive_landscape']['full_service'])} full-service airlines")
            else:
                print(f"❌ Market analysis failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Market analysis returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Market analysis error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print(f"🌐 Application is running at: {base_url}")
    print("📖 Open the URL in your browser to see the dashboard")

if __name__ == "__main__":
    test_app() 