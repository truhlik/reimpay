import django.dispatch

approved = django.dispatch.Signal(providing_args=["instance"])
