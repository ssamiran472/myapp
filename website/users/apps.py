from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    def ready(self):
        from schedule_job import updater
        updater.start()
