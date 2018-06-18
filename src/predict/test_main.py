"""
Tests for main.
"""

import unittest


from .main import (
    get_customers_and_calculate_scores, get_avg_longest_interval, set_longest_intervals, load_model,
    LongestIntervalNotFoundException
)


class TestMain(unittest.TestCase):
    """
    Unit tests for main.
    """
    def test_get_customers_and_calculate_scores(self):
        expected_result = {
            'd951a5c5ceef8610d13534f41f7e083d': {
                'max_num_items': 2,
                'max_revenue': 42.0,
                'total_revenue': 192.28000000000003,
                'days_since_last_order': 289,
                'longest_interval': 0,
                'num_orders': 19
            }
        }

        result = get_customers_and_calculate_scores(filename='./data/orders_sample.csv')

        self.assertIsInstance(result, dict)
        self.assertEqual(result, expected_result)

    def test_get_avg_longest_interval_fail(self):
        customers = get_customers_and_calculate_scores(filename='./data/orders_sample.csv')

        with self.assertRaises(LongestIntervalNotFoundException):
            get_avg_longest_interval(customers)

    def test_get_avg_longest_interval_success(self):
        customers = get_customers_and_calculate_scores(filename='./data/orders.csv')
        result = get_avg_longest_interval(customers)

        self.assertIsInstance(result, (int, float))
        self.assertEqual(result, 12.901625478081789)

    def test_set_longest_intervals(self):
        customers = get_customers_and_calculate_scores(filename='./data/orders.csv')
        set_longest_intervals(customers, get_avg_longest_interval(customers))

        for customer_values in customers.values():
            self.assertIsNot(customer_values['longest_interval'], 0)

    def test_load_model(self):
        model = load_model()
        self.assertIsInstance(model, object)
