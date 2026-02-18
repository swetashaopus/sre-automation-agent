"""
SRE Automation Agent - Reporting Module

Generates reports and summaries of monitoring data.
"""

import json
from typing import Dict, Any, List
from datetime import datetime


class Reporter:
    """Generates monitoring reports."""
    
    def __init__(self, config):
        """
        Initialize reporter.
        
        Args:
            config: Configuration object
        """
        self.config = config
    
    def generate_summary(self, metrics: Dict[str, Any], alerts: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a summary report of metrics.
        
        Args:
            metrics: Metrics data
            alerts: List of alerts
            
        Returns:
            Summary report
        """
        summary = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': self._determine_overall_status(metrics),
            'metrics_summary': {}
        }
        
        # CPU Summary
        if 'cpu' in metrics:
            summary['metrics_summary']['cpu'] = {
                'usage': metrics['cpu'].get('value'),
                'status': metrics['cpu'].get('status'),
                'threshold': metrics['cpu'].get('threshold')
            }
        
        # Memory Summary
        if 'memory' in metrics:
            summary['metrics_summary']['memory'] = {
                'usage': metrics['memory'].get('value'),
                'status': metrics['memory'].get('status'),
                'threshold': metrics['memory'].get('threshold')
            }
        
        # Disk Summary
        if 'disk' in metrics:
            disk_summary = []
            for disk in metrics['disk']:
                disk_summary.append({
                    'mountpoint': disk.get('mountpoint'),
                    'usage': disk.get('value'),
                    'status': disk.get('status'),
                    'threshold': disk.get('threshold')
                })
            summary['metrics_summary']['disk'] = disk_summary
        
        # Alert Summary
        if alerts:
            summary['alerts'] = {
                'count': len(alerts),
                'high_severity': len([a for a in alerts if a.get('severity') == 'high']),
                'medium_severity': len([a for a in alerts if a.get('severity') == 'medium']),
                'recent': alerts[-5:] if len(alerts) > 5 else alerts
            }
        
        return summary
    
    def _determine_overall_status(self, metrics: Dict[str, Any]) -> str:
        """
        Determine overall system status.
        
        Args:
            metrics: Metrics data
            
        Returns:
            Overall status string
        """
        statuses = []
        
        if 'cpu' in metrics:
            statuses.append(metrics['cpu'].get('status', 'healthy'))
        
        if 'memory' in metrics:
            statuses.append(metrics['memory'].get('status', 'healthy'))
        
        if 'disk' in metrics:
            for disk in metrics['disk']:
                statuses.append(disk.get('status', 'healthy'))
        
        if 'critical' in statuses:
            return 'critical'
        elif 'warning' in statuses:
            return 'warning'
        else:
            return 'healthy'
    
    def format_text_report(self, summary: Dict[str, Any]) -> str:
        """
        Format summary as text report.
        
        Args:
            summary: Summary data
            
        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 50)
        lines.append("SRE Automation Agent - System Report")
        lines.append("=" * 50)
        lines.append(f"Timestamp: {summary.get('timestamp')}")
        lines.append(f"Overall Status: {summary.get('overall_status').upper()}")
        lines.append("")
        
        metrics = summary.get('metrics_summary', {})
        
        if 'cpu' in metrics:
            lines.append("CPU:")
            lines.append(f"  Usage: {metrics['cpu']['usage']:.2f}%")
            lines.append(f"  Status: {metrics['cpu']['status']}")
            lines.append(f"  Threshold: {metrics['cpu']['threshold']}%")
            lines.append("")
        
        if 'memory' in metrics:
            lines.append("Memory:")
            lines.append(f"  Usage: {metrics['memory']['usage']:.2f}%")
            lines.append(f"  Status: {metrics['memory']['status']}")
            lines.append(f"  Threshold: {metrics['memory']['threshold']}%")
            lines.append("")
        
        if 'disk' in metrics:
            lines.append("Disk:")
            for disk in metrics['disk']:
                lines.append(f"  {disk['mountpoint']}:")
                lines.append(f"    Usage: {disk['usage']:.2f}%")
                lines.append(f"    Status: {disk['status']}")
                lines.append(f"    Threshold: {disk['threshold']}%")
            lines.append("")
        
        if 'alerts' in summary:
            alerts = summary['alerts']
            lines.append("Alerts:")
            lines.append(f"  Total: {alerts['count']}")
            lines.append(f"  High Severity: {alerts['high_severity']}")
            lines.append(f"  Medium Severity: {alerts['medium_severity']}")
            lines.append("")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def save_report(self, summary: Dict[str, Any], filename: str = None, format: str = 'json'):
        """
        Save report to file.
        
        Args:
            summary: Summary data
            filename: Output filename
            format: Output format ('json' or 'text')
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sre_report_{timestamp}.{format}"
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2)
        elif format == 'text':
            with open(filename, 'w') as f:
                f.write(self.format_text_report(summary))
        
        return filename
