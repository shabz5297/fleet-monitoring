from prometheus_client import Gauge

def test_metrics_initialize():
    # Simple test to ensure Prometheus metrics can be created.
    test_gauge = Gauge('test_metric', 'A test metric', ['label'])
    test_gauge.labels(label='test').set(1)
    assert True
