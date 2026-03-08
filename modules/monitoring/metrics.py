"""
Performance Metrics and Profiler for v5.0
"""
import time

class MetricsCollector:
    def __init__(self):
        self.start_times = {}

    def start_timer(self, label):
        self.start_times[label] = time.time()

    def stop_timer(self, label):
        if label in self.start_times:
            duration = time.time() - self.start_times[label]
            print(f"Metrics> {label}: {duration:.4f}s")
            return duration
        return 0

class CodeProfiler:
    def profile_function(self, func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Profiler> {func.__name__} took {end-start:.4f}s")
        return result
