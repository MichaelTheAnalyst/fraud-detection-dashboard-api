"""
Quick API Test Script - Verify all endpoints are working
"""
import requests
import json
from datetime import datetime
import sys


BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def test_endpoint(name, url, expected_keys=None):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check expected keys if provided
            if expected_keys:
                missing_keys = [key for key in expected_keys if key not in data]
                if missing_keys:
                    print_error(f"{name} - Missing keys: {missing_keys}")
                    return False
            
            # Print sample of response
            print_success(f"{name}")
            print(f"   Status: {response.status_code}")
            print(f"   Time: {response.elapsed.total_seconds():.3f}s")
            
            # Print some key data
            if isinstance(data, dict):
                sample_keys = list(data.keys())[:3]
                for key in sample_keys:
                    value = data[key]
                    if isinstance(value, (int, float, str, bool)):
                        print(f"   {key}: {value}")
            
            return True
        else:
            print_error(f"{name} - Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"{name} - Connection failed. Is server running?")
        return False
    except Exception as e:
        print_error(f"{name} - Error: {str(e)}")
        return False


def main():
    """Main test function"""
    print_header("🧪 FRAUD DETECTION API TEST SUITE")
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Health Check
    print_header("1️⃣  System Health")
    results.append(test_endpoint(
        "Health Check",
        f"{BASE_URL}/health",
        expected_keys=["status", "timestamp", "data_loaded"]
    ))
    
    # Test 2: Executive Dashboard
    print_header("2️⃣  Executive Dashboard Endpoints")
    results.append(test_endpoint(
        "Executive Overview",
        f"{API_V1}/dashboard/executive-overview",
        expected_keys=["fraud_amount_today", "fraud_rate_24h", "alerts_pending"]
    ))
    
    results.append(test_endpoint(
        "High-Risk Transactions",
        f"{API_V1}/dashboard/high-risk-transactions?limit=5",
        expected_keys=["critical_alerts", "total_alerts"]
    ))
    
    results.append(test_endpoint(
        "Fraud Velocity Heatmap",
        f"{API_V1}/dashboard/fraud-velocity-heatmap",
        expected_keys=["hourly_rates", "peak_attack_window"]
    ))
    
    results.append(test_endpoint(
        "Fraud Type Breakdown",
        f"{API_V1}/dashboard/fraud-type-breakdown",
        expected_keys=["fraud_types", "dominant_type"]
    ))
    
    results.append(test_endpoint(
        "Behavioral Anomalies",
        f"{API_V1}/dashboard/behavioral-anomalies",
        expected_keys=["anomalies", "total_anomalies"]
    ))
    
    results.append(test_endpoint(
        "Smart Alerts",
        f"{API_V1}/dashboard/smart-alerts",
        expected_keys=["critical_alerts", "warning_alerts"]
    ))
    
    # Test 3: Analytics
    print_header("3️⃣  Analytics Endpoints")
    results.append(test_endpoint(
        "Geo-Anomaly Hotspots",
        f"{API_V1}/analytics/geo-anomaly-hotspots",
        expected_keys=["high_risk_corridors", "impossible_travel_count"]
    ))
    
    results.append(test_endpoint(
        "Predictive Risk Scores",
        f"{API_V1}/analytics/predictive-risk-scores?limit=10",
        expected_keys=["high_probability_targets", "total_at_risk"]
    ))
    
    results.append(test_endpoint(
        "Financial Impact",
        f"{API_V1}/analytics/financial-impact?period_days=30",
        expected_keys=["fraud_prevented", "net_savings", "roi_percentage"]
    ))
    
    results.append(test_endpoint(
        "Customer Experience",
        f"{API_V1}/analytics/customer-experience",
        expected_keys=["blocked_transactions", "satisfaction_score"]
    ))
    
    results.append(test_endpoint(
        "Temporal Trends",
        f"{API_V1}/analytics/temporal-trends",
        expected_keys=["historical_trend", "forecast"]
    ))
    
    results.append(test_endpoint(
        "Merchant/Channel Risk",
        f"{API_V1}/analytics/merchant-channel-risk",
        expected_keys=["risk_matrix", "highest_risk_combination"]
    ))
    
    # Test 4: Network Analysis
    print_header("4️⃣  Network Analysis Endpoints")
    results.append(test_endpoint(
        "Fraud Network Graph",
        f"{API_V1}/network/fraud-network-graph?min_fraud_prob=0.7",
        expected_keys=["nodes", "edges", "fraud_rings"]
    ))
    
    results.append(test_endpoint(
        "Mule Accounts Detection",
        f"{API_V1}/network/mule-accounts?min_senders=5"
    ))
    
    # Test 5: Model Monitoring
    print_header("5️⃣  Model Monitoring Endpoints")
    results.append(test_endpoint(
        "Model Health",
        f"{API_V1}/model/model-health",
        expected_keys=["current_metrics", "recommendation"]
    ))
    
    results.append(test_endpoint(
        "Confusion Matrix",
        f"{API_V1}/model/confusion-matrix",
        expected_keys=["true_positive", "false_positive"]
    ))
    
    results.append(test_endpoint(
        "Feature Importance",
        f"{API_V1}/model/feature-importance"
    ))
    
    # Summary
    print_header("📊 TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n  Total Tests: {total}")
    print(f"  Passed: {passed} ✅")
    print(f"  Failed: {total - passed} ❌")
    print(f"  Success Rate: {percentage:.1f}%\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! API is working perfectly!")
        print("\n🌐 Next Steps:")
        print("   • Open Swagger docs: http://localhost:8000/docs")
        print("   • View API reference: API_QUICK_REFERENCE.md")
        print("   • Start building your frontend!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\n💡 Troubleshooting:")
        print("   • Ensure server is running: python start_server.py")
        print("   • Check if dataset is loaded: curl http://localhost:8000/health")
        print("   • Review logs in the server console")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

