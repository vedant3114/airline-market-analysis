#!/usr/bin/env python3
"""
Test script to verify insights generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import DataProcessor
from insights_generator import InsightsGenerator

def test_insights_generation():
    """Test the insights generation with sample data"""
    print("Testing insights generation...")
    
    # Initialize components
    processor = DataProcessor()
    insights_gen = InsightsGenerator()
    
    # Get sample data
    print("Getting sample data...")
    sample_data = processor.get_sample_data()
    print(f"Sample data shape: {sample_data.shape}")
    print(f"Sample data columns: {list(sample_data.columns)}")
    
    # Generate insights
    print("Generating insights...")
    insights = insights_gen.generate_insights(sample_data)
    
    # Check insights structure
    print(f"Insights keys: {list(insights.keys())}")
    
    # Check each section
    for key, value in insights.items():
        print(f"\n{key.upper()}:")
        if isinstance(value, dict):
            print(f"  Keys: {list(value.keys())}")
            if key == 'ai_analysis':
                print(f"  AI Analysis sections: {list(value.keys())}")
                if 'trends' in value:
                    print(f"  Trends: {list(value['trends'].keys())}")
                if 'recommendations' in value:
                    print(f"  Recommendations count: {len(value['recommendations'])}")
        elif isinstance(value, list):
            print(f"  List length: {len(value)}")
        else:
            print(f"  Type: {type(value)}")
    
    # Test AI analysis specifically
    ai_analysis = insights.get('ai_analysis', {})
    print(f"\nAI ANALYSIS DETAILS:")
    print(f"  Present: {'ai_analysis' in insights}")
    print(f"  Keys: {list(ai_analysis.keys())}")
    
    if 'trends' in ai_analysis:
        print(f"  Trends: {ai_analysis['trends']}")
    
    if 'recommendations' in ai_analysis:
        print(f"  Recommendations: {ai_analysis['recommendations'][:3]}")  # First 3
    
    if 'risks' in ai_analysis:
        print(f"  Risks: {ai_analysis['risks'][:3]}")  # First 3
    
    print("\nTest completed successfully!")
    return insights

if __name__ == "__main__":
    test_insights_generation() 