"""
This program is designed to be run apart from the API so it can be executed
manually or scheduled as a cron job. See README for more information.
"""

import os
import logging
from datetime import datetime, date

import dill
import numpy
import redis

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LongestIntervalNotFoundException(Exception):
    pass


def get_customers_and_calculate_scores(filename='./data/orders.csv'):
    """
    Get orders from CSV file. It calculates and returns
    max_num_items, max_revenue, total_revenue, days_since_last_order,
    longest_interval, num_orders of the customers.

    :param filename: Orders CSV file (absolute path).
    :return: dict (customers)
    """
    orders = open(os.path.abspath(filename), 'r')
    orders.readline()  # Skip the header.

    customers = dict()

    while True:
        order = orders.readline()

        # Stop iteration.
        if not order:
            break

        # Split variables by comma (,).
        customer_id, _, _, num_items, revenue, created_at_date = order.split(',')

        if 'NA' in (num_items, revenue):
            # Pass the orders which they have not any score.
            continue

        num_items = int(num_items)
        revenue = float(revenue)

        # Split variables of the date by (-).
        year, month, day = created_at_date.split('-')
        created_at_date = date(int(year), int(month), int(day))

        # Calculate days since last order.
        days_since_last_order = (date.today() - created_at_date).days

        # Initialize object if not in customers dict.
        if customer_id not in customers:
            customers[customer_id] = {
                'max_num_items': num_items,
                'max_revenue': revenue,
                'total_revenue': revenue,
                'days_since_last_order': days_since_last_order,
                'longest_interval': 0,
                'num_orders': 1,
            }
        # Object found, update it in this condition.
        else:
            # If the new num_items greater than the current maximum one, update it.
            if num_items > customers[customer_id]['max_num_items']:
                customers[customer_id]['max_num_items'] = num_items

            # If the new revenue greater than the current maximum one, update it.
            if revenue > customers[customer_id]['max_revenue']:
                customers[customer_id]['max_revenue'] = revenue

            new_interval = customers[customer_id]['days_since_last_order'] - days_since_last_order

            # If the new_interval greater than the current longest one, update it.
            if new_interval > customers[customer_id]['longest_interval']:
                customers[customer_id]['longest_interval'] = new_interval

            # Update rest of the keys.
            customers[customer_id]['days_since_last_order'] = days_since_last_order
            customers[customer_id]['total_revenue'] += revenue
            customers[customer_id]['num_orders'] += 1

    return customers


def get_avg_longest_interval(customers):
    """
    Get average longest interval among the customers.

    :param customers: dict
    :return: int|float
    """
    longest_intervals = list()

    for customer_values in customers.values():
        # Get longest intervals which they have greater than 0 (zero) days.
        if customer_values['longest_interval'] > 0:
            longest_intervals.append(customer_values['longest_interval'])

    if not longest_intervals:
        raise LongestIntervalNotFoundException('Longest interval values were not found. Aborting operation.')

    # Calculate average longest interval.
    return sum(longest_intervals) / len(longest_intervals)


def set_longest_intervals(customers, avg_longest_interval):
    """
    Set longest intervals to the customers which they have 0 (zero) days longest_interval value.

    :param customers: dict
    :param avg_longest_interval: int|float
    :return:
    """
    for customer_values in customers.values():
        if customer_values['longest_interval'] == 0:
            customer_values['longest_interval'] = avg_longest_interval + customer_values['days_since_last_order']


def load_model(filename='./data/model.dill'):
    """
    Loads and returns dill model.

    :param filename: model file (absolute path).
    :return:
    """
    with open(os.path.abspath(filename), 'rb') as file:
        model = dill.load(file)

    return model


def predict_and_save_predicted_values(customers, model, db=0):
    """
    Predicts the CLV of each customer using given model.

    :param customers: dict
    :param model: instance of dill.load()
    :param db: redis database
    :return:
    """

    # Use pipeline to reduce the number of back-and-forth TCP packets between two containers.
    pipeline = redis.Redis(host='redis', db=db).pipeline()

    for customer_id, values in customers.items():
        # Set predicted CLV to the redis.
        pipeline.set(customer_id, model.predict(x=numpy.array([[
            values['max_num_items'],
            values['max_revenue'],
            values['total_revenue'],
            values['num_orders'],
            values['days_since_last_order'],
            values['longest_interval'],
        ]]))[0])

    pipeline.execute()


def main():
    t1 = datetime.now()
    model = load_model()

    customers = get_customers_and_calculate_scores()
    set_longest_intervals(customers, get_avg_longest_interval(customers))
    predict_and_save_predicted_values(customers, model)

    logger.info('Completed at {} seconds.'.format((datetime.now() - t1).total_seconds()))


if __name__ == '__main__':
    main()
