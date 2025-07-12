import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

class DataProcessor:
    def __init__(self):
        self.processed_data = None
        
    def process_flight_data(self, raw_data):
        """
        Process and clean raw flight data
        """
        if not raw_data:
            return pd.DataFrame()
            
        # Convert to DataFrame
        df = pd.DataFrame(raw_data)
        
        # Clean and process the data
        df = self._clean_data(df)
        df = self._add_features(df)
        df = self._calculate_metrics(df)
        
        self.processed_data = df
        return df
    
    def _clean_data(self, df):
        """Clean the raw data"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Convert date columns to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        if 'departure_time' in df.columns:
            df['departure_time'] = pd.to_datetime(df['departure_time'])
            
        if 'arrival_time' in df.columns:
            df['arrival_time'] = pd.to_datetime(df['arrival_time'])
        
        # Handle missing values
        df['price'] = df['price'].fillna(df['price'].median())
        df['airline'] = df['airline'].fillna('Unknown')
        
        # Remove outliers (prices outside 3 standard deviations)
        price_mean = df['price'].mean()
        price_std = df['price'].std()
        df = df[(df['price'] >= price_mean - 3*price_std) & 
                (df['price'] <= price_mean + 3*price_std)]
        
        return df
    
    def _add_features(self, df):
        """Add derived features to the data"""
        # Add day of week if not present
        if 'day_of_week' not in df.columns and 'date' in df.columns:
            df['day_of_week'] = df['date'].dt.day_name()
        
        # Add hour of day if not present
        if 'hour' not in df.columns and 'departure_time' in df.columns:
            df['hour'] = df['departure_time'].dt.hour
        
        # Add month and season
        if 'date' in df.columns:
            df['month'] = df['date'].dt.month
            df['season'] = df['date'].dt.month.map({
                12: 'Summer', 1: 'Summer', 2: 'Summer',
                3: 'Autumn', 4: 'Autumn', 5: 'Autumn',
                6: 'Winter', 7: 'Winter', 8: 'Winter',
                9: 'Spring', 10: 'Spring', 11: 'Spring'
            })
        
        # Add price categories
        df['price_category'] = pd.cut(df['price'], 
                                    bins=[0, 200, 400, 600, 1000], 
                                    labels=['Budget', 'Economy', 'Premium', 'Luxury'])
        
        # Add demand level based on available seats
        if 'available_seats' in df.columns and 'total_seats' in df.columns:
            df['occupancy_rate'] = (df['total_seats'] - df['available_seats']) / df['total_seats']
            df['demand_level'] = pd.cut(df['occupancy_rate'], 
                                      bins=[0, 0.5, 0.7, 0.9, 1.0], 
                                      labels=['Low', 'Medium', 'High', 'Very High'])
        
        # Add route distance (simplified)
        df['route_distance'] = df['route'].map(self._get_route_distances())
        
        return df
    
    def _calculate_metrics(self, df):
        """Calculate additional metrics"""
        # Calculate price per km
        if 'route_distance' in df.columns:
            df['price_per_km'] = df['price'] / df['route_distance']
        
        # Calculate time-based demand patterns
        if 'hour' in df.columns:
            df['peak_hour'] = df['hour'].apply(lambda x: 
                'Peak' if (7 <= x <= 9) or (17 <= x <= 19) else 'Off-Peak')
        
        # Calculate weekend vs weekday
        if 'day_of_week' in df.columns:
            df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
        
        return df
    
    def _get_route_distances(self):
        """Get route distances for Australian airports"""
        return {
            'SYD-MEL': 713, 'MEL-SYD': 713,
            'SYD-BNE': 732, 'BNE-SYD': 732,
            'SYD-PER': 3291, 'PER-SYD': 3291,
            'SYD-ADL': 1165, 'ADL-SYD': 1165,
            'SYD-CBR': 244, 'CBR-SYD': 244,
            'MEL-BNE': 1370, 'BNE-MEL': 1370,
            'MEL-PER': 2708, 'PER-MEL': 2708,
            'MEL-ADL': 640, 'ADL-MEL': 640,
            'BNE-PER': 3605, 'PER-BNE': 3605,
            'BNE-ADL': 1600, 'ADL-BNE': 1600,
            'PER-ADL': 2125, 'ADL-PER': 2125
        }
    
    def get_sample_data(self):
        """Get sample data for demonstration"""
        if self.processed_data is not None and len(self.processed_data) > 0:
            return self.processed_data
        
        # Generate sample data if none exists
        return self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate sample processed data"""
        # Generate dates for the next 30 days
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        
        sample_data = []
        
        for date in dates:
            # Generate 5-10 flights per day
            num_flights = random.randint(5, 10)
            
            for i in range(num_flights):
                # Random departure time
                hour = random.randint(6, 22)
                minute = random.choice([0, 15, 30, 45])
                departure_time = date.replace(hour=hour, minute=minute)
                
                # Random route
                routes = ['SYD-MEL', 'MEL-SYD', 'SYD-BNE', 'BNE-SYD', 'MEL-BNE', 'BNE-MEL']
                route = random.choice(routes)
                origin, destination = route.split('-')
                
                # Price based on route
                base_prices = {'SYD-MEL': 300, 'MEL-SYD': 300, 'SYD-BNE': 350, 
                              'BNE-SYD': 350, 'MEL-BNE': 400, 'BNE-MEL': 400}
                base_price = base_prices[route]
                price = base_price + random.randint(-50, 100)
                
                # Airline
                airlines = ['Qantas', 'Virgin Australia', 'Jetstar', 'Rex']
                airline = random.choice(airlines)
                
                # Flight details
                duration_hours = random.randint(1, 4)
                arrival_time = departure_time + timedelta(hours=duration_hours)
                
                # Seat availability
                total_seats = random.randint(150, 300)
                available_seats = random.randint(10, total_seats)
                occupancy_rate = (total_seats - available_seats) / total_seats
                
                # Demand score
                weekend_multiplier = 1.3 if date.weekday() >= 5 else 1.0
                peak_multiplier = 1.4 if (7 <= hour <= 9) or (17 <= hour <= 19) else 1.0
                demand_score = weekend_multiplier * peak_multiplier * (1 - price/1000)
                
                flight_record = {
                    'flight_number': f"{airline[:2].upper()}{random.randint(100, 9999)}",
                    'airline': airline,
                    'origin': origin,
                    'destination': destination,
                    'route': route,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'duration': f"{duration_hours}h",
                    'price': price,
                    'date': date,
                    'day_of_week': date.strftime('%A'),
                    'hour': hour,
                    'month': date.month,
                    'season': ['Summer', 'Autumn', 'Winter', 'Spring'][(date.month % 12) // 3],
                    'total_seats': total_seats,
                    'available_seats': available_seats,
                    'occupancy_rate': occupancy_rate,
                    'demand_level': 'High' if occupancy_rate > 0.7 else 'Medium' if occupancy_rate > 0.5 else 'Low',
                    'peak_hour': 'Peak' if (7 <= hour <= 9) or (17 <= hour <= 19) else 'Off-Peak',
                    'is_weekend': date.weekday() >= 5,
                    'demand_score': round(demand_score, 2),
                    'price_category': 'Economy' if price < 400 else 'Premium' if price < 600 else 'Luxury'
                }
                
                sample_data.append(flight_record)
        
        return pd.DataFrame(sample_data)
    
    def get_price_analysis(self, df):
        """Analyze price trends and patterns"""
        if df.empty:
            return {}
        
        analysis = {
            'price_statistics': {
                'mean': float(round(df['price'].mean(), 2)),
                'median': float(round(df['price'].median(), 2)),
                'min': float(round(df['price'].min(), 2)),
                'max': float(round(df['price'].max(), 2)),
                'std': float(round(df['price'].std(), 2))
            },
            'price_by_airline': {str(k): {'mean': float(v['mean']), 'count': int(v['count'])} for k, v in df.groupby('airline')['price'].agg(['mean', 'count']).round(2).to_dict('index').items()},
            'price_by_route': {str(k): float(v) for k, v in df.groupby('route')['price'].mean().round(2).to_dict().items()},
            'price_by_day': {str(k): float(v) for k, v in df.groupby('day_of_week')['price'].mean().round(2).to_dict().items()},
            'price_by_hour': {int(k): float(v) for k, v in df.groupby('hour')['price'].mean().round(2).to_dict().items()}
        }
        
        return analysis
    
    def get_demand_analysis(self, df):
        """Analyze demand patterns"""
        if df.empty:
            return {}
        
        analysis = {
            'demand_by_day': {str(k): int(v) for k, v in df['day_of_week'].value_counts().to_dict().items()},
            'demand_by_hour': {int(k): int(v) for k, v in df['hour'].value_counts().sort_index().to_dict().items()},
            'demand_by_airline': {str(k): int(v) for k, v in df['airline'].value_counts().to_dict().items()},
            'demand_by_route': {str(k): int(v) for k, v in df['route'].value_counts().to_dict().items()},
            'weekend_vs_weekday': {
                'weekend': int(len(df[df['is_weekend'] == True])),
                'weekday': int(len(df[df['is_weekend'] == False]))
            }
        }
        
        if 'demand_level' in df.columns:
            analysis['demand_levels'] = {str(k): int(v) for k, v in df['demand_level'].value_counts().to_dict().items()}
        
        return analysis
    
    def get_route_analysis(self, df):
        """Analyze route-specific patterns"""
        if df.empty:
            return {}
        
        route_analysis = {}
        
        for route in df['route'].unique():
            route_data = df[df['route'] == route]
            route_analysis[str(route)] = {
                'total_flights': int(len(route_data)),
                'avg_price': float(round(route_data['price'].mean(), 2)),
                'popular_airlines': {str(k): int(v) for k, v in route_data['airline'].value_counts().head(3).to_dict().items()},
                'peak_hours': {int(k): int(v) for k, v in route_data['hour'].value_counts().head(3).to_dict().items()},
                'weekend_ratio': float(round(len(route_data[route_data['is_weekend']]) / len(route_data), 2))
            }
        
        return route_analysis
    
    def get_trends_analysis(self, df):
        """Analyze trends over time"""
        if df.empty or 'date' not in df.columns:
            return {}
        
        # Daily trends
        daily_trends = df.groupby('date').agg({
            'price': ['mean', 'count'],
            'demand_score': 'mean'
        }).round(2)
        
        # Weekly trends
        df['week'] = df['date'].dt.isocalendar().week
        weekly_trends = df.groupby('week').agg({
            'price': 'mean',
            'demand_score': 'mean'
        }).round(2)
        
        return {
            'daily_trends': daily_trends.to_dict(),
            'weekly_trends': weekly_trends.to_dict()
        } 