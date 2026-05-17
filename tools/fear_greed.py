#!/usr/bin/env python3
"""
Fear & Greed Index Fetcher
Fetch current and historical Fear & Greed Index data from Alternative.me API
"""

import requests
import json
from datetime import datetime, timedelta

def fetch_fear_greed(limit=8):
    """Fetch Fear & Greed Index data"""
    try:
        url = "https://api.alternative.me/fng/"
        params = {"limit": limit, "format": "json"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def parse_data(data):
    """Parse and format Fear & Greed data"""
    if "error" in data:
        return {"status": "error", "message": data.get("error")}
    
    if not data.get("data"):
        return {"status": "error", "message": "No data available"}
    
    records = data["data"]
    
    # Current value (most recent)
    current = records[0]
    current_value = int(current["value"])
    current_class = current["value_classification"]
    current_ts = int(current["timestamp"])
    current_date = datetime.fromtimestamp(current_ts).strftime("%Y-%m-%d")
    
    # Yesterday (if available)
    yesterday = None
    if len(records) > 1:
        yesterday = records[1]
        yesterday_value = int(yesterday["value"])
    else:
        yesterday_value = None
    
    # Week ago (if available)
    week_ago = None
    if len(records) >= 7:
        week_ago = records[6]
        week_ago_value = int(week_ago["value"])
    else:
        week_ago_value = None
    
    # Calculate trend
    trend = "stable"
    if yesterday_value:
        if current_value > yesterday_value + 5:
            trend = "↑ improving"
        elif current_value < yesterday_value - 5:
            trend = "↓ declining"
    
    return {
        "status": "success",
        "current": {
            "value": current_value,
            "classification": current_class,
            "date": current_date
        },
        "comparison": {
            "yesterday": yesterday_value,
            "week_ago": week_ago_value,
            "trend": trend
        },
        "raw_data": records
    }

def forecast_sentiment(data):
    """Simple 1-week sentiment forecast based on trend"""
    if data["status"] != "success":
        return "Unable to forecast"
    
    current = data["current"]["value"]
    trend = data["comparison"]["trend"]
    
    # Simple forecast logic
    if "improving" in trend:
        forecast = "Sentiment likely to improve or stabilize. Watch for resistance at 50+ (Greed zone)."
    elif "declining" in trend:
        forecast = "Sentiment may continue declining. Support at 20-30 (Extreme Fear zone)."
    else:
        forecast = "Sentiment likely to remain in current zone. Monitor for breakout signals."
    
    return forecast

if __name__ == "__main__":
    print("Fetching Fear & Greed Index...")
    raw_data = fetch_fear_greed(limit=8)
    parsed = parse_data(raw_data)
    
    if parsed["status"] == "success":
        print(json.dumps(parsed, indent=2))
    else:
        print(json.dumps(parsed, indent=2))
