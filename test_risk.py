import unittest
from risk import calculate_risk


class TestRisk(unittest.TestCase):

    def test_completed_task(self):
        result = calculate_risk("2099-01-01", 2, "Low", 100)
        self.assertEqual(result, "Low Risk")

    def test_high_effort_task(self):
        result = calculate_risk("2099-01-01", 10, "High", 0)
        self.assertEqual(result, "High Risk")

    def test_overdue_task(self):
        result = calculate_risk("2000-01-01", 5, "High", 0)
        self.assertEqual(result, "High Risk")

    def test_completed_task_has_low_risk(self):
        result = calculate_risk("2099-01-01", 10, "High", 100)
        self.assertEqual(result, "Low Risk")

    def test_overdue_incomplete_task(self):
        result = calculate_risk("2000-01-01", 5, "High", 20)
        self.assertEqual(result, "High Risk")
        
    
    def test_completed_overdue_task(self):
     result = calculate_risk("2000-01-01", 5, "High", 100)
     self.assertEqual(result, "Low Risk")


if __name__ == "__main__":
    unittest.main()
    def test_completed_overdue_task(self):
        result = calculate_risk("2000-01-01", 5, "High", 100)
        self.assertEqual(result, "Low Risk")