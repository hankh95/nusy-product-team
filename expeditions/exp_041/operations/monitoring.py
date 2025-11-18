# DGX Operations & Monitoring (Sub-EXP-041E)
# Production monitoring, alerting, and operational runbooks

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import psutil
import GPUtil
from prometheus_client import start_http_server, Gauge, Counter, Histogram
import yaml

# Configuration
NUSY_ROOT = Path("/opt/nusy")
MONITORING_PORT = 9090
ALERT_THRESHOLDS = {
    "cpu_usage": 80.0,  # Percent
    "memory_usage": 85.0,  # Percent
    "gpu_memory_usage": 90.0,  # Percent
    "disk_usage": 90.0,  # Percent
    "agent_response_time": 5.0,  # Seconds
    "model_inference_time": 10.0  # Seconds
}

class DGXMonitor:
    """Comprehensive monitoring for the DGX Manolin Cluster"""

    def __init__(self):
        self.cluster = None
        self.is_monitoring = False

        # Prometheus metrics
        self.cpu_usage = Gauge('dgx_cpu_usage_percent', 'CPU usage percentage')
        self.memory_usage = Gauge('dgx_memory_usage_percent', 'Memory usage percentage')
        self.gpu_memory_usage = Gauge('dgx_gpu_memory_usage_percent', 'GPU memory usage percentage')
        self.disk_usage = Gauge('dgx_disk_usage_percent', 'Disk usage percentage')

        self.agent_count = Gauge('dgx_agent_count', 'Number of active agents')
        self.session_count = Gauge('dgx_session_count', 'Number of active sessions')
        self.request_count = Counter('dgx_requests_total', 'Total requests processed')
        self.error_count = Counter('dgx_errors_total', 'Total errors encountered')

        self.agent_response_time = Histogram('dgx_agent_response_time_seconds',
                                           'Agent response time in seconds')
        self.model_inference_time = Histogram('dgx_model_inference_time_seconds',
                                            'Model inference time in seconds')

        # Alert tracking
        self.alerts = []
        self.alert_history = []

        # Setup logging
        self.logger = logging.getLogger("dgx-monitor")
        handler = logging.FileHandler(NUSY_ROOT / "logs" / "dgx_monitor.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def start_monitoring(self, cluster):
        """Start comprehensive monitoring"""
        self.cluster = cluster
        self.is_monitoring = True

        # Start Prometheus metrics server
        start_http_server(MONITORING_PORT)
        self.logger.info(f"Prometheus metrics server started on port {MONITORING_PORT}")

        # Start monitoring tasks
        asyncio.create_task(self._system_metrics_collector())
        asyncio.create_task(self._cluster_metrics_collector())
        asyncio.create_task(self._alert_checker())
        asyncio.create_task(self._health_checker())

        self.logger.info("DGX monitoring started")

    async def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        self.logger.info("DGX monitoring stopped")

    async def _system_metrics_collector(self):
        """Collect system-level metrics"""
        while self.is_monitoring:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_usage.set(cpu_percent)

                # Memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                self.memory_usage.set(memory_percent)

                # GPU usage (if available)
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu_memory_percent = gpus[0].memoryUtil * 100
                        self.gpu_memory_usage.set(gpu_memory_percent)
                except:
                    pass  # GPU monitoring may not be available

                # Disk usage
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                self.disk_usage.set(disk_percent)

                await asyncio.sleep(10)  # Collect every 10 seconds

            except Exception as e:
                self.logger.error(f"System metrics collection error: {e}")
                await asyncio.sleep(30)

    async def _cluster_metrics_collector(self):
        """Collect cluster-level metrics"""
        while self.is_monitoring:
            try:
                if self.cluster:
                    status = await self.cluster.get_status()

                    # Agent and session counts
                    self.agent_count.set(status["agent_count"])
                    self.session_count.set(status.get("metrics", {}).get("active_sessions", 0))

                    # Update request and error metrics from cluster
                    metrics = status.get("metrics", {})
                    # Note: In a real implementation, these would be cumulative counters

                await asyncio.sleep(30)  # Collect every 30 seconds

            except Exception as e:
                self.logger.error(f"Cluster metrics collection error: {e}")
                await asyncio.sleep(60)

    async def _alert_checker(self):
        """Check for alert conditions"""
        while self.is_monitoring:
            try:
                alerts = []

                # Check CPU usage
                cpu_percent = psutil.cpu_percent()
                if cpu_percent > ALERT_THRESHOLDS["cpu_usage"]:
                    alerts.append({
                        "type": "cpu_high",
                        "severity": "warning",
                        "message": f"CPU usage is {cpu_percent:.1f}% (threshold: {ALERT_THRESHOLDS['cpu_usage']}%)",
                        "value": cpu_percent
                    })

                # Check memory usage
                memory = psutil.virtual_memory()
                if memory.percent > ALERT_THRESHOLDS["memory_usage"]:
                    alerts.append({
                        "type": "memory_high",
                        "severity": "critical",
                        "message": f"Memory usage is {memory.percent:.1f}% (threshold: {ALERT_THRESHOLDS['memory_usage']}%)",
                        "value": memory.percent
                    })

                # Check disk usage
                disk = psutil.disk_usage('/')
                if disk.percent > ALERT_THRESHOLDS["disk_usage"]:
                    alerts.append({
                        "type": "disk_high",
                        "severity": "warning",
                        "message": f"Disk usage is {disk.percent:.1f}% (threshold: {ALERT_THRESHOLDS['disk_usage']}%)",
                        "value": disk.percent
                    })

                # Update active alerts
                self.alerts = alerts

                # Log new alerts
                for alert in alerts:
                    if alert not in self.alert_history:
                        self.logger.warning(f"ALERT: {alert['message']}")
                        self.alert_history.append(alert)

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                self.logger.error(f"Alert checking error: {e}")
                await asyncio.sleep(120)

    async def _health_checker(self):
        """Perform periodic health checks"""
        while self.is_monitoring:
            try:
                health_status = await self.perform_health_check()

                if not health_status["healthy"]:
                    self.logger.error(f"Health check failed: {health_status}")
                    # Could trigger alerts or recovery actions here

                await asyncio.sleep(300)  # Health check every 5 minutes

            except Exception as e:
                self.logger.error(f"Health check error: {e}")
                await asyncio.sleep(300)

    async def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        health_status = {
            "healthy": True,
            "checks": {},
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Check cluster status
            if self.cluster:
                cluster_status = await self.cluster.get_status()
                health_status["checks"]["cluster"] = {
                    "status": "healthy" if cluster_status["is_running"] else "unhealthy",
                    "agents": cluster_status["agent_count"],
                    "model_runtime": cluster_status.get("model_runtime_status", "unknown")
                }

                if not cluster_status["is_running"]:
                    health_status["healthy"] = False
            else:
                health_status["checks"]["cluster"] = {"status": "no_cluster"}
                health_status["healthy"] = False

            # Check system resources
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()

            health_status["checks"]["system"] = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": psutil.disk_usage('/').percent
            }

            # Critical thresholds
            if cpu_percent > 95 or memory.percent > 95:
                health_status["healthy"] = False
                health_status["checks"]["system"]["status"] = "critical"
            elif cpu_percent > ALERT_THRESHOLDS["cpu_usage"] or memory.percent > ALERT_THRESHOLDS["memory_usage"]:
                health_status["checks"]["system"]["status"] = "warning"

            # Check model files
            model_registry = NUSY_ROOT / "models" / "model_registry.json"
            if model_registry.exists():
                health_status["checks"]["models"] = {"status": "present"}
            else:
                health_status["checks"]["models"] = {"status": "missing"}
                health_status["healthy"] = False

        except Exception as e:
            health_status["healthy"] = False
            health_status["error"] = str(e)

        return health_status

    def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            "is_monitoring": self.is_monitoring,
            "active_alerts": self.alerts,
            "recent_alerts": self.alert_history[-10:],  # Last 10 alerts
            "metrics_port": MONITORING_PORT,
            "uptime": time.time() - psutil.boot_time()
        }

class DGXOperations:
    """Operational runbooks and management"""

    def __init__(self):
        self.runbooks = self._load_runbooks()

    def _load_runbooks(self) -> Dict[str, Any]:
        """Load operational runbooks"""
        return {
            "startup": {
                "title": "DGX System Startup",
                "steps": [
                    "Power on DGX Spark and storage enclosure",
                    "Wait for system POST and OS boot",
                    "Verify network connectivity",
                    "Start NVIDIA services: sudo systemctl start nvidia-persistenced",
                    "Start NuSy services: cd /opt/nusy && source nusy-env/bin/activate && python -m manolin_cluster",
                    "Verify monitoring: curl http://localhost:9090/metrics",
                    "Check cluster status: curl http://localhost:8000/status"
                ]
            },
            "shutdown": {
                "title": "DGX System Shutdown",
                "steps": [
                    "Stop NuSy services gracefully",
                    "Save any in-memory state to disk",
                    "Stop monitoring services",
                    "Shutdown OS: sudo shutdown -h now",
                    "Power off storage enclosure",
                    "Power off DGX Spark"
                ]
            },
            "backup": {
                "title": "System Backup Procedure",
                "steps": [
                    "Stop active workloads",
                    "Create workspace backup: tar -czf workspace_backup.tar.gz /opt/nusy/workspace",
                    "Backup model registry: cp /opt/nusy/models/model_registry.json /opt/nusy/backups/",
                    "Backup configuration files",
                    "Verify backup integrity",
                    "Resume workloads"
                ]
            },
            "recovery": {
                "title": "System Recovery Procedure",
                "steps": [
                    "Assess damage and determine recovery scope",
                    "Restore from latest backup if available",
                    "Reinstall missing components using provisioning scripts",
                    "Validate system integrity with integration tests",
                    "Gradually restore workloads",
                    "Monitor for issues post-recovery"
                ]
            },
            "performance_tuning": {
                "title": "Performance Optimization",
                "steps": [
                    "Monitor current performance metrics",
                    "Identify bottlenecks (CPU, GPU, memory, disk)",
                    "Adjust model batch sizes and concurrency limits",
                    "Optimize storage layout and caching",
                    "Update system configuration (kernel parameters, etc.)",
                    "Re-run performance benchmarks"
                ]
            }
        }

    def get_runbook(self, procedure: str) -> Optional[Dict[str, Any]]:
        """Get a specific runbook"""
        return self.runbooks.get(procedure)

    def list_runbooks(self) -> List[str]:
        """List available runbooks"""
        return list(self.runbooks.keys())

class AlertManager:
    """Alert management and notification system"""

    def __init__(self):
        self.alert_rules = self._load_alert_rules()
        self.notification_channels = []

    def _load_alert_rules(self) -> Dict[str, Any]:
        """Load alert rules and thresholds"""
        return {
            "cpu_critical": {
                "condition": lambda metrics: metrics.get("cpu_usage", 0) > 95,
                "severity": "critical",
                "message": "CPU usage above 95%",
                "actions": ["log", "notify", "scale_down"]
            },
            "memory_critical": {
                "condition": lambda metrics: metrics.get("memory_usage", 0) > 90,
                "severity": "critical",
                "message": "Memory usage above 90%",
                "actions": ["log", "notify", "kill_sessions"]
            },
            "gpu_memory_critical": {
                "condition": lambda metrics: metrics.get("gpu_memory_usage", 0) > 95,
                "severity": "critical",
                "message": "GPU memory usage above 95%",
                "actions": ["log", "notify", "restart_runtime"]
            },
            "disk_full": {
                "condition": lambda metrics: metrics.get("disk_usage", 0) > 95,
                "severity": "warning",
                "message": "Disk usage above 95%",
                "actions": ["log", "cleanup", "notify"]
            }
        }

    async def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check metrics against alert rules"""
        triggered_alerts = []

        for rule_name, rule in self.alert_rules.items():
            if rule["condition"](metrics):
                alert = {
                    "rule": rule_name,
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "timestamp": datetime.now().isoformat(),
                    "metrics": metrics,
                    "actions": rule["actions"]
                }
                triggered_alerts.append(alert)

        return triggered_alerts

    async def handle_alert(self, alert: Dict[str, Any]):
        """Handle a triggered alert"""
        severity = alert["severity"]
        actions = alert["actions"]

        # Log the alert
        logging.warning(f"ALERT [{severity}]: {alert['message']}")

        # Execute actions
        for action in actions:
            if action == "log":
                # Already logged above
                pass
            elif action == "notify":
                await self._send_notification(alert)
            elif action == "scale_down":
                await self._scale_down_workload()
            elif action == "kill_sessions":
                await self._kill_old_sessions()
            elif action == "restart_runtime":
                await self._restart_model_runtime()
            elif action == "cleanup":
                await self._cleanup_disk_space()

    async def _send_notification(self, alert: Dict[str, Any]):
        """Send alert notification"""
        # Implementation would integrate with email, Slack, etc.
        print(f"NOTIFICATION: {alert['message']}")

    async def _scale_down_workload(self):
        """Scale down workload to reduce resource usage"""
        print("Scaling down workload...")

    async def _kill_old_sessions(self):
        """Kill old/inactive sessions"""
        print("Killing old sessions...")

    async def _restart_model_runtime(self):
        """Restart model runtime"""
        print("Restarting model runtime...")

    async def _cleanup_disk_space(self):
        """Clean up disk space"""
        print("Cleaning up disk space...")

# Global instances
monitor = DGXMonitor()
operations = DGXOperations()
alert_manager = AlertManager()

async def initialize_operations(cluster):
    """Initialize operations and monitoring"""
    await monitor.start_monitoring(cluster)
    return {
        "monitor": monitor,
        "operations": operations,
        "alert_manager": alert_manager
    }

if __name__ == "__main__":
    # Example usage
    async def main():
        print("DGX Operations & Monitoring System")
        print("Available runbooks:", operations.list_runbooks())

        # Example health check
        health = await monitor.perform_health_check()
        print("Health status:", "HEALTHY" if health["healthy"] else "UNHEALTHY")

    asyncio.run(main())