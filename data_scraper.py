import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import random
from bs4 import BeautifulSoup
import re

class AirlineDataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Australian airports
        self.australian_airports = {
            'SYD': 'Sydney',
            'MEL': 'Melbourne', 
            'BNE': 'Brisbane',
            'PER': 'Perth',
            'ADL': 'Adelaide',
            'CBR': 'Canberra',
            'DRW': 'Darwin',
            'HBA': 'Hobart',
            'CNS': 'Cairns',
            'TSV': 'Townsville'
        }
        
        # Major airlines
        self.airlines = ['Qantas', 'Virgin Australia', 'Jetstar', 'Rex', 'Tigerair']

    def fetch_flight_data(self, origin='SYD', destination='MEL', date_from=None, date_to=None):
        """
        Fetch flight data from multiple sources
        """
        if not date_from:
            date_from = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
        print(f"Fetching flight data from {origin} to {destination} from {date_from} to {date_to}")
        
        # Try multiple data sources
        data_sources = [
            self._fetch_from_aviation_stack,
            self._fetch_from_sample_api,
            self._generate_sample_data
        ]
        
        for source_func in data_sources:
            try:
                data = source_func(origin, destination, date_from, date_to)
                if data and len(data) > 0:
                    print(f"Successfully fetched {len(data)} records from {source_func.__name__}")
                    return data
            except Exception as e:
                print(f"Error fetching from {source_func.__name__}: {str(e)}")
                continue
        
        # Fallback to sample data
        return self._generate_sample_data(origin, destination, date_from, date_to)

    def _fetch_from_aviation_stack(self, origin, destination, date_from, date_to):
        """
        Fetch data from Aviation Stack API (free tier)
        """
        try:
            # Aviation Stack API endpoint
            url = "http://api.aviationstack.com/v1/flights"
            
            params = {
                'access_key': 'your_api_key_here',  # Would need actual API key
                'dep_iata': origin,
                'arr_iata': destination,
                'date': date_from
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_aviation_stack_data(data)
            else:
                print(f"Aviation Stack API returned status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error with Aviation Stack API: {str(e)}")
            return None

    def _fetch_from_sample_api(self, origin, destination, date_from, date_to):
        """
        Fetch data from a sample flight API
        """
        try:
            # Using a mock API endpoint
            url = "https://api.mockaroo.com/flight_data"
            
            params = {
                'key': 'mock_key',
                'count': 50,
                'origin': origin,
                'destination': destination
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error with sample API: {str(e)}")
            return None

    def _generate_sample_data(self, origin, destination, date_from, date_to):
        """
        Generate realistic sample flight data for demonstration
        """
        print("Generating sample flight data...")
        
        # Convert dates to datetime objects
        start_date = datetime.strptime(date_from, '%Y-%m-%d')
        end_date = datetime.strptime(date_to, '%Y-%m-%d')
        
        # Generate dates between start and end
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        flight_data = []
        
        # Generate multiple flights per day
        for date in date_range:
            # Generate 3-8 flights per day
            num_flights = random.randint(3, 8)
            
            for i in range(num_flights):
                # Random departure time
                hour = random.randint(6, 22)
                minute = random.choice([0, 15, 30, 45])
                departure_time = date.replace(hour=hour, minute=minute)
                
                # Flight duration (1-4 hours for domestic flights)
                duration_hours = random.randint(1, 4)
                duration_minutes = random.randint(0, 59)
                arrival_time = departure_time + timedelta(hours=duration_hours, minutes=duration_minutes)
                
                # Price based on distance and demand
                base_price = self._calculate_base_price(origin, destination)
                price_variation = random.uniform(0.7, 1.5)
                price = round(base_price * price_variation, 2)
                
                # Airline selection with weights
                airline = random.choices(
                    self.airlines,
                    weights=[0.4, 0.3, 0.2, 0.08, 0.02]  # Qantas most popular, Tigerair least
                )[0]
                
                # Flight number
                flight_number = self._generate_flight_number(airline)
                
                # Aircraft type
                aircraft_types = ['Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A330']
                aircraft = random.choice(aircraft_types)
                
                # Seat availability
                total_seats = random.randint(150, 300)
                available_seats = random.randint(10, total_seats)
                
                flight_record = {
                    'flight_number': flight_number,
                    'airline': airline,
                    'origin': origin,
                    'destination': destination,
                    'route': f"{origin}-{destination}",
                    'departure_time': departure_time.isoformat(),
                    'arrival_time': arrival_time.isoformat(),
                    'duration': f"{duration_hours}h {duration_minutes}m",
                    'price': price,
                    'aircraft': aircraft,
                    'total_seats': total_seats,
                    'available_seats': available_seats,
                    'date': date.strftime('%Y-%m-%d'),
                    'day_of_week': date.strftime('%A'),
                    'hour': hour,
                    'demand_score': self._calculate_demand_score(date, hour, price)
                }
                
                flight_data.append(flight_record)
        
        return flight_data

    def _calculate_base_price(self, origin, destination):
        """Calculate base price based on route distance"""
        # Simplified distance calculation for Australian routes
        route_distances = {
            'SYD-MEL': 713, 'MEL-SYD': 713,
            'SYD-BNE': 732, 'BNE-SYD': 732,
            'SYD-PER': 3291, 'PER-SYD': 3291,
            'MEL-BNE': 1370, 'BNE-MEL': 1370,
            'MEL-PER': 2708, 'PER-MEL': 2708,
            'BNE-PER': 3605, 'PER-BNE': 3605
        }
        
        route = f"{origin}-{destination}"
        distance = route_distances.get(route, 1000)  # Default 1000km
        
        # Base price: $0.15 per km
        return distance * 0.15

    def _generate_flight_number(self, airline):
        """Generate realistic flight number based on airline"""
        airline_codes = {
            'Qantas': 'QF',
            'Virgin Australia': 'VA',
            'Jetstar': 'JQ',
            'Rex': 'ZL',
            'Tigerair': 'TT'
        }
        
        code = airline_codes.get(airline, 'XX')
        number = random.randint(100, 9999)
        return f"{code}{number}"

    def _calculate_demand_score(self, date, hour, price):
        """Calculate demand score based on date, time, and price"""
        # Weekend flights are more popular
        weekend_multiplier = 1.3 if date.weekday() >= 5 else 1.0
        
        # Peak hours (morning and evening) are more popular
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            time_multiplier = 1.4
        elif 10 <= hour <= 16:
            time_multiplier = 1.1
        else:
            time_multiplier = 0.8
        
        # Price sensitivity (lower prices = higher demand)
        price_factor = max(0.5, 1.0 - (price - 200) / 1000)
        
        return round(weekend_multiplier * time_multiplier * price_factor, 2)

    def _parse_aviation_stack_data(self, data):
        """Parse data from Aviation Stack API"""
        if 'data' not in data:
            return None
            
        parsed_data = []
        for flight in data['data']:
            try:
                parsed_flight = {
                    'flight_number': flight.get('flight', {}).get('iata', ''),
                    'airline': flight.get('airline', {}).get('name', ''),
                    'origin': flight.get('departure', {}).get('iata', ''),
                    'destination': flight.get('arrival', {}).get('iata', ''),
                    'departure_time': flight.get('departure', {}).get('scheduled', ''),
                    'arrival_time': flight.get('arrival', {}).get('scheduled', ''),
                    'price': random.randint(150, 800),  # Mock price
                    'date': flight.get('departure', {}).get('scheduled', '')[:10]
                }
                parsed_data.append(parsed_flight)
            except Exception as e:
                print(f"Error parsing flight data: {e}")
                continue
                
        return parsed_data

    def get_available_routes(self):
        """Get list of available routes"""
        routes = []
        airports = list(self.australian_airports.keys())
        
        for i, origin in enumerate(airports):
            for destination in airports[i+1:]:
                routes.append({
                    'origin': origin,
                    'destination': destination,
                    'route': f"{origin}-{destination}"
                })
        
        return routes

    def get_airport_info(self, airport_code):
        """Get airport information"""
        return {
            'code': airport_code,
            'name': self.australian_airports.get(airport_code, 'Unknown'),
            'country': 'Australia'
        } 