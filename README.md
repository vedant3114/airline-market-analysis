# Airline Market Analysis Dashboard

A comprehensive web application for analyzing airline booking market demand trends and generating business insights for hostel businesses in Australia.

## Features

### 🚀 Enhanced AI-Powered Analysis
- **Comprehensive Market Trends**: Analysis of market growth, seasonal patterns, and competition intensity
- **Strategic Recommendations**: 8 actionable business recommendations for pricing, capacity, and route optimization
- **Risk Assessment**: Detailed analysis of 8 key risk factors affecting the airline market
- **Market Opportunities**: Identification of growth opportunities and competitive advantages
- **Financial Insights**: Revenue drivers, cost optimization strategies, and profitability metrics
- **Competitive Analysis**: Market leader analysis and competitive landscape insights

### 📊 Data Visualization
- **Price Trend Charts**: Dynamic pricing patterns over time
- **Airline Distribution**: Market share analysis by carrier
- **Route Popularity**: Demand patterns across different routes
- **Demand Heatmap**: Visual representation of demand by day and hour

### 🔍 Market Insights
- **Price Analysis**: Expensive vs. cheapest days, airline pricing strategies
- **Demand Patterns**: Peak hours, weekend ratios, popular routes
- **Route-Specific Insights**: Detailed analysis for each route
- **Trend Analysis**: Price and demand trends over time

### 🛠 Technical Features
- **Real-time Data Processing**: Live data fetching and analysis
- **Responsive Design**: Modern Bootstrap-based UI
- **Interactive Charts**: Plotly-powered visualizations
- **Debug Tools**: Built-in testing and debugging capabilities

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   AVIATION_STACK_API_KEY=your_aviation_stack_key_here
   ```

## Usage

### Starting the Application
```bash
python app.py
```

The application will be available at:
- **Local**: http://127.0.0.1:5000
- **Network**: http://192.168.0.102:5000 (accessible from other devices on your network)

### Using the Dashboard

1. **Search Flight Data**:
   - Select origin and destination airports
   - Choose date range
   - Click "Analyze Market Data"

2. **View Results**:
   - **Summary Statistics**: Total flights, average prices, price ranges
   - **Interactive Charts**: Price trends, airline distribution, route popularity, demand heatmap
   - **Market Insights**: Price and demand analysis with actionable recommendations
   - **AI Analysis**: Comprehensive business intelligence and strategic insights

3. **Debug and Test**:
   - Click "Test Insights" button to verify AI analysis generation
   - Check browser console for detailed debug information
   - Use the debug info panel to verify data structure

### AI Analysis Sections

The enhanced AI analysis provides:

#### 📈 Market Trends
- Market growth patterns and recovery indicators
- Seasonal demand variations and peak periods
- Price volatility analysis and dynamic pricing patterns
- Competition intensity and market dynamics

#### 💰 Pricing Analysis
- Average ticket prices and price ranges
- Dynamic pricing strategies and factors
- Cost structure breakdown (fuel, labor, aircraft, other costs)
- Price sensitivity and elasticity analysis

#### 👥 Demand Analysis
- Peak travel periods and demand patterns
- Popular routes and market concentration
- Weekend vs. weekday demand ratios
- Business vs. leisure travel breakdown

#### 💡 Strategic Recommendations
1. **Strategic Pricing**: Dynamic pricing models based on demand patterns
2. **Capacity Management**: Optimized flight scheduling for demand peaks
3. **Route Optimization**: Focus on high-demand routes and underserved markets
4. **Customer Segmentation**: Targeted marketing for different traveler types
5. **Technology Investment**: AI-powered forecasting and optimization tools
6. **Partnership Opportunities**: Codeshare agreements and strategic alliances
7. **Sustainability Focus**: Fuel efficiency and carbon offset programs
8. **Digital Transformation**: Enhanced booking platforms and mobile apps

#### ⚠️ Risk Factors
- Economic downturn impacts on travel spending
- Fuel price volatility and profitability effects
- Regulatory changes and compliance costs
- Competitive pressure from new market entrants
- Technology disruption from emerging solutions
- Climate change and weather-related impacts
- Labor relations and operational disruptions
- Cybersecurity threats and data protection

#### 🚀 Market Opportunities
- Regional route expansion potential
- Premium service demand growth
- Cargo operations during off-peak periods
- Enhanced loyalty program development
- Ancillary service revenue streams
- Corporate partnership opportunities
- International connection leveraging
- Digital service innovation

## API Endpoints

### `/api/fetch-data` (POST)
Fetches and analyzes flight data for specified route and date range.

**Request Body**:
```json
{
  "origin": "SYD",
  "destination": "MEL", 
  "date_from": "2025-07-19",
  "date_to": "2025-08-11"
}
```

### `/api/charts` (POST)
Generates interactive charts for data visualization.

**Request Body**:
```json
{
  "chart_type": "price_trend"
}
```

### `/api/market-analysis` (GET)
Returns comprehensive market analysis insights.

### `/api/test-insights` (GET)
Test endpoint for verifying insights generation (debug tool).

## Troubleshooting

### Empty Insights Sections
If you see empty market recommendations, insights, or AI analysis:

1. **Check the "Test Insights" button** to verify data generation
2. **Open browser console** (F12) to see debug logs
3. **Verify API responses** in the Network tab
4. **Check backend logs** for any errors

### Common Issues

**ModuleNotFoundError: No module named 'flask'**
```bash
pip install flask
```

**Pandas installation issues**
```bash
pip install pandas==1.5.3
```

**Charts not loading**
- Check if Plotly is installed: `pip install plotly`
- Verify internet connection for CDN resources

### Debug Information
The application includes comprehensive debugging:
- Console logs for data flow tracking
- Debug info panel showing data structure
- Backend logging for API calls
- Test endpoints for verification

## Data Sources

- **Aviation Stack API**: Real flight data (requires API key)
- **Sample Data Generation**: Robust mock data for testing and demonstration
- **OpenAI API**: AI-powered insights (optional, falls back to enhanced mock analysis)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and business analysis purposes.

---

**Note**: The application uses mock data generation when external APIs are not available, ensuring you always get comprehensive insights for testing and demonstration purposes. 