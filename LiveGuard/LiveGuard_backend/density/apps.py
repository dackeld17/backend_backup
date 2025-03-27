from django.apps import AppConfig
import threading


class DensityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'density'

    def ready(self):
        from .yolo_runner import run_yolo_analysis
        t = threading.Thread(target=run_yolo_analysis, daemon=True)
        t.start()