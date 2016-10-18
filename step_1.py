import requests
from network_utilities import get_request, post_request

def catch_first_operand(url):
    op1_url = url + "/step1"
    return get_request(op1_url, 'value', 'next')

def catch_second_operand(url, next_op):
    op2_url = url + next_op
    return get_request(op2_url, 'value', 'next')

def catch_operator(url, next_op):
    operator_url = url + next_op
    return get_request(operator_url, 'value', 'next', 'uri')

def send_result(main_url, result_uri, result):
    result_url = main_url + result_uri
    json_info = {"value": result}
    headers = {"Content-Type": "application/json"}
    return post_request(result_url, json_info, headers)

def calc_result(op1, op2, operator):
    op1 = int(op1)
    op2 = int(op2)
    res = 0
    if operator == '+':
        res = op1 + op2
    elif operator == '/':
        res = op1 / op2
    elif operator == '-':
        res = op1 - op2
    elif operator == '*':
        res = op1 * op2
    return res

def make_step1(main_url):
    print("/////////\nSTEP 1\n/////////")
    first_op, op2_endpoint = catch_first_operand(main_url)
    second_op, operator_endpoint = catch_second_operand(main_url, op2_endpoint)
    operator, step2_endpoint, result_uri = catch_operator(main_url, operator_endpoint)
    result = calc_result(first_op, second_op, operator)
    status_code = send_result(main_url, result_uri, result)
    if status_code != 201:
        print("Exiting. Step 1 failed")
        exit(0)
    return step2_endpoint