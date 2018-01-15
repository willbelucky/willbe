import re
import string
import json



def code_to_isin(code):
    number_code = code
    order_code = '00'
    if re.findall("([" + string.ascii_uppercase + "])+", code):
        alphabet = re.findall("([" + string.ascii_uppercase + "])+", code)[0]
        number_code = re.sub(alphabet, str(ord(alphabet) - 55), number_code)
        order_code = '0' + str(ord(alphabet) - 74)
    val_list = [40, 47, 14] + [x * y for x, y in zip([int(ch) for ch in number_code], [1, 2, 1, 2, 1, 2])] + [0, 0]
    check_val = sum([int(v / 10) + v % 10 for v in val_list]) % 10
    check_str = '0'
    if check_val > 0:
        check_str = str(10 - check_val)

    return 'KR7' + code + order_code + check_str


def isin_to_code(isin):
    return isin[3:9]


json.loads(origin)
