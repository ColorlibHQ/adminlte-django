import datetime

from django.test import TestCase


class DashboardActivityTests(TestCase):
    def test_six_consecutive_months(self):
        data = self.client.get("/api/dashboard/activity.json").json()
        months = [datetime.date.fromisoformat(c) for c in data["categories"]]
        self.assertEqual(len(months), 6)
        for earlier, later in zip(months, months[1:]):
            self.assertEqual(
                (later.year * 12 + later.month) - (earlier.year * 12 + earlier.month), 1
            )
        self.assertEqual(months[-1], datetime.date.today().replace(day=1))
        self.assertEqual(len(data["series"]), 2)
        for series in data["series"]:
            self.assertEqual(len(series["data"]), 6)
