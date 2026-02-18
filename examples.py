#!/usr/bin/env python3
"""
Example script demonstrating the SRE Automation Agent usage.
"""

from agent import SREAgent
from config import Config

def example_single_check():
    """Example: Run a single system check."""
    print("Example 1: Single System Check")
    print("-" * 50)
    
    agent = SREAgent()
    result = agent.start(continuous=False)
    
    print("\nCheck Results:")
    print(f"Overall Status: {result['summary']['overall_status']}")
    print(f"Alerts Generated: {len(result['alerts'])}")
    
    return result


def example_custom_config():
    """Example: Using custom configuration."""
    print("\nExample 2: Custom Configuration")
    print("-" * 50)
    
    # Create custom configuration
    config = Config()
    config.set('monitoring.cpu_threshold', 50)  # Lower threshold for demo
    config.set('monitoring.memory_threshold', 60)
    
    print(f"CPU Threshold: {config.get('monitoring.cpu_threshold')}%")
    print(f"Memory Threshold: {config.get('monitoring.memory_threshold')}%")
    
    # Note: To use custom config with agent, save it to a file and load it


def example_alert_history():
    """Example: View alert history."""
    print("\nExample 3: Alert History")
    print("-" * 50)
    
    agent = SREAgent()
    agent.run_check()
    
    # Get recent alerts
    recent_alerts = agent.alert_manager.get_alert_history(limit=5)
    
    if recent_alerts:
        print(f"\nRecent Alerts ({len(recent_alerts)}):")
        for alert in recent_alerts:
            print(f"  - [{alert['severity'].upper()}] {alert['message']}")
    else:
        print("\nNo alerts in history")


def example_service_monitoring():
    """Example: Monitor specific services."""
    print("\nExample 4: Service Monitoring")
    print("-" * 50)
    
    config = Config()
    
    # Add services to monitor
    config.set('services', [
        {'name': 'python'},
        {'name': 'bash'}
    ])
    
    agent = SREAgent()
    agent.config = config
    agent.service_monitor = agent.service_monitor.__class__(config)
    
    services = agent.service_monitor.check_all_services()
    
    print("\nService Status:")
    for service in services:
        print(f"  {service['service']}: {service['status']} ({service['count']} processes)")


def example_report_generation():
    """Example: Generate and save reports."""
    print("\nExample 5: Report Generation")
    print("-" * 50)
    
    agent = SREAgent()
    result = agent.run_check()
    
    # Generate text report
    text_report = agent.reporter.format_text_report(result['summary'])
    print("\nText Report Preview:")
    print(text_report[:500] + "...\n")
    
    # Save reports
    json_file = agent.reporter.save_report(result['summary'], 'example_report.json', 'json')
    text_file = agent.reporter.save_report(result['summary'], 'example_report.txt', 'text')
    
    print(f"Reports saved:")
    print(f"  - {json_file}")
    print(f"  - {text_file}")


if __name__ == '__main__':
    print("SRE Automation Agent - Examples")
    print("=" * 50)
    
    # Run examples
    try:
        example_single_check()
        example_custom_config()
        example_alert_history()
        example_service_monitoring()
        example_report_generation()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
