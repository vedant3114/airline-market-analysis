import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    AVIATION_STACK_API_KEY = os.environ.get('AVIATION_STACK_API_KEY')
    
    # Application settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Data settings
    SAMPLE_DATA_ENABLED = True
    API_TIMEOUT = 30  # seconds
    
    # Chart settings
    CHART_HEIGHT = 400
    CHART_WIDTH = None  # Auto-width
    
    # Australian airports
    AUSTRALIAN_AIRPORTS = {
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
    AIRLINES = ['Qantas', 'Virgin Australia', 'Jetstar', 'Rex', 'Tigerair']
    
    # Route distances (km) for price calculation
    ROUTE_DISTANCES = {
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
    
    # Price categories
    PRICE_CATEGORIES = {
        'budget': (0, 200),
        'economy': (200, 400),
        'premium': (400, 600),
        'luxury': (600, 1000)
    }
    
    # Demand levels
    DEMAND_LEVELS = {
        'low': (0, 0.5),
        'medium': (0.5, 0.7),
        'high': (0.7, 0.9),
        'very_high': (0.9, 1.0)
    }
    
    # Peak hours
    PEAK_HOURS = {
        'morning': (7, 9),
        'evening': (17, 19)
    }
    
    # Seasons
    SEASONS = {
        12: 'Summer', 1: 'Summer', 2: 'Summer',
        3: 'Autumn', 4: 'Autumn', 5: 'Autumn',
        6: 'Winter', 7: 'Winter', 8: 'Winter',
        9: 'Spring', 10: 'Spring', 11: 'Spring'
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SAMPLE_DATA_ENABLED = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SAMPLE_DATA_ENABLED = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SAMPLE_DATA_ENABLED = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 