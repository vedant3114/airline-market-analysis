from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
import os
from datetime import datetime, timedelta
import requests
from data_scraper import AirlineDataScraper
from data_processor import DataProcessor
from insights_generator import InsightsGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize components
scraper = AirlineDataScraper()
processor = DataProcessor()
insights_gen = InsightsGenerator()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/fetch-data', methods=['POST'])
def fetch_data():
    """API endpoint to fetch airline data"""
    try:
        data = request.get_json()
        origin = data.get('origin', 'SYD')
        destination = data.get('destination', 'MEL')
        date_from = data.get('date_from', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
        date_to = data.get('date_to', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
        
        print(f"Fetching flight data from {origin} to {destination} from {date_from} to {date_to}")
        
        # Fetch data from scraper
        airline_data = scraper.fetch_flight_data(origin, destination, date_from, date_to)
        
        if airline_data:
            print(f"Successfully fetched {len(airline_data)} records from scraper")
            
            # Process the data
            processed_data = processor.process_flight_data(airline_data)
            print(f"Processed data shape: {processed_data.shape}")
            
            # Generate insights
            insights = insights_gen.generate_insights(processed_data)
            
            # Add heatmap-specific insights
            heatmap_insights = insights_gen.generate_heatmap_insights(processed_data)
            insights['heatmap_insights'] = heatmap_insights
            
            print(f"Generated insights keys: {list(insights.keys())}")
            print(f"AI analysis keys: {list(insights.get('ai_analysis', {}).keys())}")
            print(f"Heatmap insights keys: {list(heatmap_insights.keys())}")
            
            # Convert DataFrame to records and handle numpy types
            records = processed_data.to_dict('records')
            for record in records:
                for key, value in record.items():
                    if hasattr(value, 'item'):  # numpy type
                        record[key] = value.item()
                    elif isinstance(value, (np.integer, np.floating)):
                        record[key] = value.item()
                    # Handle NaN values
                    if isinstance(value, float) and np.isnan(value):
                        record[key] = None
                    elif hasattr(value, 'item') and np.isnan(value.item()):
                        record[key] = None
            
            # Convert insights to native Python types
            def convert_numpy_types(obj):
                if isinstance(obj, dict):
                    return {str(k): convert_numpy_types(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy_types(item) for item in obj]
                elif hasattr(obj, 'item'):  # numpy type
                    value = obj.item()
                    # Handle NaN values
                    if isinstance(value, float) and np.isnan(value):
                        return None
                    return value
                elif isinstance(obj, (np.integer, np.floating)):
                    value = obj.item()
                    # Handle NaN values
                    if isinstance(value, float) and np.isnan(value):
                        return None
                    return value
                elif isinstance(obj, float) and np.isnan(obj):
                    return None
                else:
                    return obj
            
            # Convert insights to native Python types
            insights = convert_numpy_types(insights)
            
            response_data = {
                'success': True,
                'data': records,
                'insights': insights,
                'summary': {
                    'total_flights': int(len(processed_data)),
                    'avg_price': float(processed_data['price'].mean()),
                    'price_range': f"${processed_data['price'].min():.0f} - ${processed_data['price'].max():.0f}",
                    'popular_airlines': {str(k): int(v) for k, v in processed_data['airline'].value_counts().head(3).to_dict().items()}
                }
            }
            
            print(f"Response data keys: {list(response_data.keys())}")
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': 'No data available'})
            
    except Exception as e:
        print(f"Error in fetch_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/test-insights')
def test_insights():
    """Test endpoint to verify insights generation"""
    try:
        # Get sample data
        sample_data = processor.get_sample_data()
        print(f"Sample data shape: {sample_data.shape}")
        
        # Generate insights
        insights = insights_gen.generate_insights(sample_data)
        print(f"Test insights keys: {list(insights.keys())}")
        
        # Check AI analysis specifically
        ai_analysis = insights.get('ai_analysis', {})
        print(f"AI analysis keys: {list(ai_analysis.keys())}")
        print(f"AI analysis trends: {ai_analysis.get('trends', {})}")
        print(f"AI analysis recommendations: {ai_analysis.get('recommendations', [])}")
        
        # Convert insights to native Python types
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {str(k): convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif hasattr(obj, 'item'):  # numpy type
                value = obj.item()
                # Handle NaN values
                if isinstance(value, float) and np.isnan(value):
                    return None
                return value
            elif isinstance(obj, (np.integer, np.floating)):
                value = obj.item()
                # Handle NaN values
                if isinstance(value, float) and np.isnan(value):
                    return None
                return value
            elif isinstance(obj, float) and np.isnan(obj):
                return None
            else:
                return obj
        
        insights = convert_numpy_types(insights)
        
        return jsonify({
            'success': True,
            'insights': insights,
            'data_shape': sample_data.shape,
            'ai_analysis_present': 'ai_analysis' in insights,
            'ai_analysis_keys': list(ai_analysis.keys()) if ai_analysis else []
        })
    except Exception as e:
        print(f"Error in test_insights: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/charts', methods=['POST'])
def generate_charts():
    """API endpoint to generate charts"""
    try:
        data = request.get_json()
        chart_type = data.get('chart_type', 'price_trend')
        heatmap_view = data.get('heatmap_view', 'default')
        
        # Get sample data for demonstration
        sample_data = processor.get_sample_data()
        
        if chart_type == 'price_trend':
            chart = create_price_trend_chart(sample_data)
        elif chart_type == 'airline_distribution':
            chart = create_airline_distribution_chart(sample_data)
        elif chart_type == 'route_popularity':
            chart = create_route_popularity_chart(sample_data)
        elif chart_type == 'demand_heatmap':
            heatmap_data = create_demand_heatmap(sample_data)
            if isinstance(heatmap_data, dict) and 'options' in heatmap_data:
                # Return the specific view or default
                if heatmap_view in heatmap_data['options']:
                    chart = heatmap_data['options'][heatmap_view]
                else:
                    chart = heatmap_data['default']
                # Also return available views for the frontend
                return jsonify({
                    'success': True,
                    'chart': chart,
                    'heatmap_views': heatmap_data.get('available_views', []),
                    'current_view': heatmap_view
                })
            else:
                chart = heatmap_data.get('default', '{}')
        else:
            chart = create_price_trend_chart(sample_data)
        
        return jsonify({
            'success': True,
            'chart': chart
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def create_price_trend_chart(data):
    """Create price trend chart"""
    fig = px.line(data, x='date', y='price', color='airline',
                  title='Flight Price Trends Over Time',
                  labels={'price': 'Price (AUD)', 'date': 'Date', 'airline': 'Airline'})
    fig.update_layout(height=400)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_airline_distribution_chart(data):
    """Create airline distribution chart"""
    airline_counts = data['airline'].value_counts()
    fig = px.pie(values=airline_counts.values, names=airline_counts.index,
                 title='Flight Distribution by Airline')
    fig.update_layout(height=400)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_route_popularity_chart(data):
    """Create route popularity chart"""
    route_counts = data.groupby('route').size().reset_index(name='count')
    fig = px.bar(route_counts, x='route', y='count',
                 title='Route Popularity',
                 labels={'count': 'Number of Flights', 'route': 'Route'})
    fig.update_layout(height=400)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_demand_heatmap(data):
    """Create enhanced demand heatmap with multiple views"""
    try:
        # Create multiple heatmap views
        heatmaps = {}
        
        # 1. Flight Count Heatmap by Day and Hour
        if 'date' in data.columns and 'hour' in data.columns:
            # Create pivot table for flight count
            pivot_data = data.pivot_table(
                values='price', 
                index=data['date'].dt.day_name(), 
                columns=data['date'].dt.hour,
                aggfunc='count'
            ).fillna(0)
            
            # Reorder days to start with Monday
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            pivot_data = pivot_data.reindex([day for day in day_order if day in pivot_data.index])
            
            # Ensure no NaN values
            pivot_data = pivot_data.fillna(0)
            
            fig1 = px.imshow(
                pivot_data, 
                title='Flight Demand Heatmap by Day and Hour',
                labels=dict(x="Hour of Day", y="Day of Week", color="Number of Flights"),
                color_continuous_scale='Viridis',
                aspect='auto'
            )
            fig1.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50))
            heatmaps['flight_count'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 2. Average Price Heatmap by Day and Hour
        if 'date' in data.columns and 'hour' in data.columns:
            price_pivot = data.pivot_table(
                values='price', 
                index=data['date'].dt.day_name(), 
                columns=data['date'].dt.hour,
                aggfunc='mean'
            ).fillna(0)
            
            # Reorder days
            price_pivot = price_pivot.reindex([day for day in day_order if day in price_pivot.index])
            
            # Ensure no NaN values
            price_pivot = price_pivot.fillna(0)
            
            fig2 = px.imshow(
                price_pivot, 
                title='Average Price Heatmap by Day and Hour',
                labels=dict(x="Hour of Day", y="Day of Week", color="Average Price (AUD)"),
                color_continuous_scale='Reds',
                aspect='auto'
            )
            fig2.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50))
            heatmaps['price_heatmap'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 3. Demand Score Heatmap by Day and Hour
        if 'date' in data.columns and 'hour' in data.columns and 'demand_score' in data.columns:
            demand_pivot = data.pivot_table(
                values='demand_score', 
                index=data['date'].dt.day_name(), 
                columns=data['date'].dt.hour,
                aggfunc='mean'
            ).fillna(0)
            
            # Reorder days
            demand_pivot = demand_pivot.reindex([day for day in day_order if day in demand_pivot.index])
            
            # Ensure no NaN values
            demand_pivot = demand_pivot.fillna(0)
            
            fig3 = px.imshow(
                demand_pivot, 
                title='Demand Score Heatmap by Day and Hour',
                labels=dict(x="Hour of Day", y="Day of Week", color="Demand Score"),
                color_continuous_scale='Blues',
                aspect='auto'
            )
            fig3.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50))
            heatmaps['demand_score'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 4. Route Popularity Heatmap
        if 'route' in data.columns and 'airline' in data.columns:
            route_airline_pivot = data.pivot_table(
                values='price',
                index='route',
                columns='airline',
                aggfunc='count'
            ).fillna(0)
            
            # Ensure no NaN values
            route_airline_pivot = route_airline_pivot.fillna(0)
            
            fig4 = px.imshow(
                route_airline_pivot,
                title='Flight Distribution by Route and Airline',
                labels=dict(x="Airline", y="Route", color="Number of Flights"),
                color_continuous_scale='Greens',
                aspect='auto'
            )
            fig4.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50))
            heatmaps['route_airline'] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 5. Price Range Heatmap by Route and Day
        if 'route' in data.columns and 'date' in data.columns:
            price_range_pivot = data.pivot_table(
                values='price',
                index='route',
                columns=data['date'].dt.day_name(),
                aggfunc='mean'
            ).fillna(0)
            
            # Reorder days
            price_range_pivot = price_range_pivot.reindex(columns=[day for day in day_order if day in price_range_pivot.columns])
            
            # Ensure no NaN values
            price_range_pivot = price_range_pivot.fillna(0)
            
            fig5 = px.imshow(
                price_range_pivot,
                title='Average Price by Route and Day of Week',
                labels=dict(x="Day of Week", y="Route", color="Average Price (AUD)"),
                color_continuous_scale='Oranges',
                aspect='auto'
            )
            fig5.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50))
            heatmaps['route_day_price'] = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 6. Weekend vs Weekday Analysis
        if 'is_weekend' in data.columns and 'hour' in data.columns:
            weekend_pivot = data.pivot_table(
                values='price',
                index='is_weekend',
                columns='hour',
                aggfunc='count'
            ).fillna(0)
            
            # Rename index for better labels
            weekend_pivot.index = ['Weekday', 'Weekend']
            
            # Ensure no NaN values
            weekend_pivot = weekend_pivot.fillna(0)
            
            fig6 = px.imshow(
                weekend_pivot,
                title='Flight Distribution: Weekend vs Weekday by Hour',
                labels=dict(x="Hour of Day", y="Day Type", color="Number of Flights"),
                color_continuous_scale='Purples',
                aspect='auto'
            )
            fig6.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50))
            heatmaps['weekend_analysis'] = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Return the first heatmap as default, but include all options
        default_heatmap = heatmaps.get('flight_count', heatmaps.get('price_heatmap', '{}'))
        
        return {
            'default': default_heatmap,
            'options': heatmaps,
            'available_views': list(heatmaps.keys())
        }
        
    except Exception as e:
        print(f"Error creating heatmap: {str(e)}")
        # Fallback to simple heatmap
        try:
            pivot_data = data.pivot_table(
                values='price', 
                index=data['date'].dt.day_name(), 
                columns=data['date'].dt.hour,
                aggfunc='count'
            ).fillna(0)
            
            fig = px.imshow(pivot_data, 
                           title='Demand Heatmap by Day and Hour',
                           labels=dict(x="Hour of Day", y="Day of Week", color="Number of Flights"))
            fig.update_layout(height=400)
            return {'default': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)}
        except:
            return {'default': '{}'}

@app.route('/api/market-analysis')
def market_analysis():
    """API endpoint for market analysis insights"""
    try:
        # Get comprehensive market analysis
        analysis = insights_gen.get_market_analysis()
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/heatmap-insights')
def get_heatmap_insights():
    """API endpoint for heatmap-specific insights"""
    try:
        # Get sample data
        sample_data = processor.get_sample_data()
        
        # Generate heatmap insights
        heatmap_insights = insights_gen.generate_heatmap_insights(sample_data)
        
        # Convert to native Python types
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {str(k): convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif hasattr(obj, 'item'):  # numpy type
                value = obj.item()
                # Handle NaN values
                if isinstance(value, float) and np.isnan(value):
                    return None
                return value
            elif isinstance(obj, (np.integer, np.floating)):
                value = obj.item()
                # Handle NaN values
                if isinstance(value, float) and np.isnan(value):
                    return None
                return value
            elif isinstance(obj, float) and np.isnan(obj):
                return None
            else:
                return obj
        
        heatmap_insights = convert_numpy_types(heatmap_insights)
        
        return jsonify({
            'success': True,
            'heatmap_insights': heatmap_insights
        })
    except Exception as e:
        print(f"Error in heatmap insights: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 