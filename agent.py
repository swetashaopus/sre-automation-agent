#!/usr/bin/env python3
"""
SRE Automation Agent - Main Agent Module

The main automation agent that orchestrates monitoring, alerting, and reporting.
"""

import time
import logging
import argparse
import signal
import sys
from datetime import datetime

from config import Config
from monitor import SystemMonitor, ServiceMonitor
from alerts import AlertManager
from report import Reporter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sre_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SREAgent:
    """Main SRE automation agent."""
    
    def __init__(self, config_file: str = None):
        """
        Initialize SRE agent.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = Config(config_file)
        self.system_monitor = SystemMonitor(self.config)
        self.service_monitor = ServiceMonitor(self.config)
        self.alert_manager = AlertManager(self.config)
        self.reporter = Reporter(self.config)
        
        self.running = False
        self.interval = self.config.get('monitoring.interval_seconds', 60)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("SRE Automation Agent initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def run_check(self) -> dict:
        """
        Run a single monitoring check.
        
        Returns:
            Dict with check results
        """
        logger.info("Running system checks...")
        
        # Collect system metrics
        metrics = self.system_monitor.check_all()
        
        # Check services if configured
        services = self.service_monitor.check_all_services()
        if services:
            metrics['services'] = services
        
        # Process metrics and generate alerts
        alerts = self.alert_manager.process_metrics(metrics)
        
        # Generate summary report
        summary = self.reporter.generate_summary(metrics, alerts)
        
        return {
            'metrics': metrics,
            'alerts': alerts,
            'summary': summary
        }
    
    def start(self, continuous: bool = True):
        """
        Start the SRE agent.
        
        Args:
            continuous: If True, run continuously. If False, run once.
        """
        self.running = True
        logger.info("SRE Automation Agent started")
        
        if continuous:
            logger.info(f"Running in continuous mode with {self.interval}s interval")
            
            while self.running:
                try:
                    result = self.run_check()
                    
                    # Log summary
                    summary = result['summary']
                    logger.info(f"Check completed - Overall Status: {summary['overall_status']}")
                    
                    if result['alerts']:
                        logger.warning(f"Generated {len(result['alerts'])} alert(s)")
                    
                    # Wait for next interval
                    if self.running:
                        time.sleep(self.interval)
                        
                except Exception as e:
                    logger.error(f"Error during monitoring check: {e}", exc_info=True)
                    if self.running:
                        time.sleep(self.interval)
        else:
            # Run once
            result = self.run_check()
            
            # Print summary
            print("\n" + self.reporter.format_text_report(result['summary']))
            
            # Save report
            report_file = self.reporter.save_report(result['summary'])
            logger.info(f"Report saved to {report_file}")
            
            return result
    
    def stop(self):
        """Stop the SRE agent."""
        self.running = False
        logger.info("SRE Automation Agent stopped")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='SRE Automation Agent')
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file',
        default=None
    )
    parser.add_argument(
        '-o', '--once',
        action='store_true',
        help='Run checks once and exit'
    )
    parser.add_argument(
        '-r', '--report',
        action='store_true',
        help='Generate and save report'
    )
    
    args = parser.parse_args()
    
    # Create and run agent
    agent = SREAgent(config_file=args.config)
    
    if args.once or args.report:
        result = agent.start(continuous=False)
        
        if args.report:
            # Save both text and JSON reports
            agent.reporter.save_report(result['summary'], format='text')
            agent.reporter.save_report(result['summary'], format='json')
            print(f"\nReports saved")
    else:
        agent.start(continuous=True)


if __name__ == '__main__':
    main()
