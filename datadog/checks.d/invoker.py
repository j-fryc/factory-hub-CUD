from datadog_checks.base import AgentCheck
import requests


class InvokerException(Exception):
    pass


class DBSync(AgentCheck):
    DEFAULT_CHECK_NAME = "custom.fastapi.check"
    DEFAULT_METRIC_NAME = "custom.fastapi.metric"

    def check(self, instance):
        url = instance.get("url")
        if not url:
            raise InvokerException("Sync url not provided in the configuration file")
        metric_name = instance.get("metric_name", self.DEFAULT_METRIC_NAME)
        service_check_name = instance.get("service_check_name", self.DEFAULT_CHECK_NAME)

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            value = data.get("metric", 0)
            if value:
                self.service_check(
                    service_check_name,
                    self.OK,
                    message=f"Successfully collected metric {metric_name}={value} from {url}"
                )
            else:
                self.service_check(
                    service_check_name,
                    self.WARNING,
                    message=f"Response JSON from {url} does not contain 'metric' key"
                )
            self.gauge(metric_name, value)
        except Exception as e:
            self.service_check(
                service_check_name,
                self.CRITICAL,
                message=f"Failed to collect from {url}: {str(e)}"
            )
