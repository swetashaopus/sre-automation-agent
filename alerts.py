"""
SRE Automation Agent - Alert Module

Handles alerting and notifications for incidents and issues.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime


logger = logging.getLogger(__name__)


class AlertManager:
    """Manages alerts and notifications."""
    
    def __init__(self, config):
        """
        Initialize alert manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.enabled = config.get('alerts.enabled', True)
        self.methods = config.get('alerts.methods', ['log'])
        self.alert_history = []
    
    def should_alert(self, metric_data: Dict[str, Any]) -> bool:
        """
        Determine if an alert should be triggered.
        
        Args:
            metric_data: Metric data to evaluate
            
        Returns:
            True if alert should be triggered
        """
        if not self.enabled:
            return False
        
        status = metric_data.get('status', 'healthy')
        return status in ['warning', 'critical']
    
    def create_alert(self, metric_data: Dict[str, Any], severity: str = None) -> Dict[str, Any]:
        """
        Create an alert from metric data.
        
        Args:
            metric_data: Metric data that triggered the alert
            severity: Override severity level
            
        Returns:
            Alert data
        """
        if severity is None:
            status = metric_data.get('status', 'healthy')
            severity = 'high' if status == 'critical' else 'medium'
        
        alert = {
            'id': len(self.alert_history) + 1,
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'metric': metric_data.get('metric', 'unknown'),
            'value': metric_data.get('value'),
            'threshold': metric_data.get('threshold'),
            'status': metric_data.get('status'),
            'message': self._generate_message(metric_data)
        }
        
        self.alert_history.append(alert)
        return alert
    
    def _generate_message(self, metric_data: Dict[str, Any]) -> str:
        """
        Generate alert message from metric data.
        
        Args:
            metric_data: Metric data
            
        Returns:
            Alert message string
        """
        metric = metric_data.get('metric', 'unknown')
        value = metric_data.get('value', 0)
        threshold = metric_data.get('threshold', 0)
        status = metric_data.get('status', 'unknown')
        
        if metric == 'cpu':
            return f"CPU usage is {status}: {value}% (threshold: {threshold}%)"
        elif metric == 'memory':
            return f"Memory usage is {status}: {value}% (threshold: {threshold}%)"
        elif metric == 'disk':
            mountpoint = metric_data.get('mountpoint', 'unknown')
            return f"Disk usage on {mountpoint} is {status}: {value}% (threshold: {threshold}%)"
        else:
            return f"Metric {metric} is {status}: {value}"
    
    def send_alert(self, alert: Dict[str, Any]):
        """
        Send alert using configured methods.
        
        Args:
            alert: Alert data to send
        """
        for method in self.methods:
            if method == 'log':
                self._send_log_alert(alert)
            # Additional methods can be added here (email, slack, etc.)
    
    def _send_log_alert(self, alert: Dict[str, Any]):
        """
        Send alert to log.
        
        Args:
            alert: Alert data
        """
        severity = alert.get('severity', 'medium')
        message = alert.get('message', 'Unknown alert')
        
        if severity == 'high':
            logger.error(f"ALERT [{severity.upper()}]: {message}")
        else:
            logger.warning(f"ALERT [{severity.upper()}]: {message}")
    
    def process_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process metrics and create alerts as needed.
        
        Args:
            metrics: Metrics data to process
            
        Returns:
            List of alerts created
        """
        alerts = []
        
        # Check CPU
        if 'cpu' in metrics:
            if self.should_alert(metrics['cpu']):
                alert = self.create_alert(metrics['cpu'])
                self.send_alert(alert)
                alerts.append(alert)
        
        # Check Memory
        if 'memory' in metrics:
            if self.should_alert(metrics['memory']):
                alert = self.create_alert(metrics['memory'])
                self.send_alert(alert)
                alerts.append(alert)
        
        # Check Disk
        if 'disk' in metrics:
            for disk_metric in metrics['disk']:
                if self.should_alert(disk_metric):
                    alert = self.create_alert(disk_metric)
                    self.send_alert(alert)
                    alerts.append(alert)
        
        return alerts
    
    def get_alert_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get alert history.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        if limit:
            return self.alert_history[-limit:]
        return self.alert_history
