import datetime

from jinja2 import meta

import composer_utils as cu
import input_utils

configs = cu.get_config()


def change_days(date, num_days):
    return date + datetime.timedelta(days=num_days)


def format_date(value, date_format=configs['Date']['DateFormatMachineReadable']):
    if type(value) == str:
        value = datetime.datetime.strptime(value, configs['Date']['DateFormatMachineReadable'])
    return value.strftime(date_format)


def change_time(time, num_hours, num_min):
    return cu.check_time(time, configs) + datetime.timedelta(hours=num_hours, minutes=num_min)


def format_time(value, time_format=configs['Time']['TimeFormatMachineReadable']):
    return cu.check_time(value, configs).strftime(time_format)


def discount(price):
    return input_utils.calculate_discount(price)


def setup(env):
    env.filters['format_date'] = format_date
    env.filters['change_days'] = change_days
    env.filters['format_time'] = format_time
    env.filters['change_time'] = change_time
    env.filters['discount'] = discount


def get_undeclared_vars(env):
    template_source = env.loader.get_source(env, configs['Files']['Template'])
    parsed_content = env.parse(template_source[0])
    return meta.find_undeclared_variables(parsed_content)
