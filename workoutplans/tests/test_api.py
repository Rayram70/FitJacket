import os
import django
from django.test import TestCase
from unittest.mock import patch
from workoutplans.utils import generate_workout_plan

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitJacket.settings')
django.setup()


class WorkoutPlanAPITests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.valid_input = """
            Age: 30
            Fitness Level: Intermediate
            Goal: Muscle Building
            Days/Week: 4
            Session Duration: 60 minutes
            Equipment: Dumbbells, Resistance Bands
            Injuries: None
            Preferences: Prefer compound movements
        """

    def test_successful_api_response(self):
        """Test that the API returns a valid response with good input"""
        result = generate_workout_plan(self.valid_input)

        self.assertIsNotNone(result, "API should return a non-None result")
        self.assertIsInstance(result, str, "Response should be a string")
        self.assertGreater(len(result), 100, "Response should be substantial")

        # Verify the response contains expected sections
        self.assertIn("Goal:", result, "Response should include Goal section")
        self.assertIn("Weekly Schedule:", result, "Response should include Schedule section")
        self.assertIn("Exercises:", result, "Response should include Exercises section")

    def test_empty_input_handling(self):
        """Test how the API handles empty input"""
        with self.assertLogs(level='ERROR') as log:
            result = generate_workout_plan("")
            self.assertIsNone(result, "API should return None for empty input")
            self.assertIn("API Error", ''.join(log.output), "Should log API error")

    @patch('workoutplans.utils.requests.post')
    def test_api_failure_handling(self, mock_post):
        """Test how the function handles API failures"""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Server Error"

        with self.assertLogs(level='ERROR') as log:
            result = generate_workout_plan(self.valid_input)
            self.assertIsNone(result, "Should return None on API failure")
            self.assertIn("API Request Failed", ''.join(log.output))