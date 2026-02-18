"""
SRE Automation Agent - Monitoring Module

Provides system and service monitoring capabilities.
"""

import psutil
import time
import logging
from typing import Dict, Any, List
from datetime import datetime


logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitors system resources and health."""
    
    def __init__(self, config):
        """
        Initialize system monitor.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.cpu_threshold = config.get('monitoring.cpu_threshold', 80)
        self.memory_threshold = config.get('monitoring.memory_threshold', 85)
        self.disk_threshold = config.get('monitoring.disk_threshold', 90)
    
    def check_cpu(self) -> Dict[str, Any]:
        """
        Check CPU usage.
        
        Returns:
            Dict with CPU metrics and status
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        status = 'healthy'
        if cpu_percent >= self.cpu_threshold:
            status = 'critical'
        elif cpu_percent >= self.cpu_threshold * 0.8:
            status = 'warning'
        
        return {
            'metric': 'cpu',
            'value': cpu_percent,
            'unit': 'percent',
            'cpu_count': cpu_count,
            'threshold': self.cpu_threshold,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_memory(self) -> Dict[str, Any]:
        """
        Check memory usage.
        
        Returns:
            Dict with memory metrics and status
        """
        memory = psutil.virtual_memory()
        
        status = 'healthy'
        if memory.percent >= self.memory_threshold:
            status = 'critical'
        elif memory.percent >= self.memory_threshold * 0.8:
            status = 'warning'
        
        return {
            'metric': 'memory',
            'value': memory.percent,
            'unit': 'percent',
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'threshold': self.memory_threshold,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_disk(self) -> List[Dict[str, Any]]:
        """
        Check disk usage for all partitions.
        
        Returns:
            List of dicts with disk metrics and status
        """
        results = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                status = 'healthy'
                if usage.percent >= self.disk_threshold:
                    status = 'critical'
                elif usage.percent >= self.disk_threshold * 0.8:
                    status = 'warning'
                
                results.append({
                    'metric': 'disk',
                    'mountpoint': partition.mountpoint,
                    'device': partition.device,
                    'fstype': partition.fstype,
                    'value': usage.percent,
                    'unit': 'percent',
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'threshold': self.disk_threshold,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })
            except (PermissionError, OSError):
                # Skip partitions we can't access
                continue
        
        return results
    
    def check_all(self) -> Dict[str, Any]:
        """
        Run all system checks.
        
        Returns:
            Dict with all system metrics
        """
        return {
            'cpu': self.check_cpu(),
            'memory': self.check_memory(),
            'disk': self.check_disk(),
            'timestamp': datetime.now().isoformat()
        }


class ServiceMonitor:
    """Monitors services and processes."""
    
    def __init__(self, config):
        """
        Initialize service monitor.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.services = config.get('services', [])
    
    def check_process(self, process_name: str) -> Dict[str, Any]:
        """
        Check if a process is running.
        
        Args:
            process_name: Name of the process to check
            
        Returns:
            Dict with process status
        """
        running_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    running_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'status': proc.info['status'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        status = 'running' if running_processes else 'stopped'
        
        return {
            'service': process_name,
            'status': status,
            'processes': running_processes,
            'count': len(running_processes),
            'timestamp': datetime.now().isoformat()
        }
    
    def check_all_services(self) -> List[Dict[str, Any]]:
        """
        Check all configured services.
        
        Returns:
            List of dicts with service status
        """
        results = []
        
        for service in self.services:
            if isinstance(service, dict):
                service_name = service.get('name')
            else:
                service_name = service
            
            if service_name:
                results.append(self.check_process(service_name))
        
        return results
