from dashboard.models import Dashboard


class Activities:
    def __init__(self, signaled_object: Dashboard):
        self.object = signaled_object

    def report_dashboard_activity(self):
        pass

    def get_principal_site(self):
        pass
