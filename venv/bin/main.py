import sys
import os
from bin.parsing import check_opening_time

def main():
    if len(sys.argv) < 2:
        raise RuntimeError('please input the opening_time and date')

    param_list = sys.argv[1].split(",")
    if len(param_list) != 2:
        raise RuntimeError('The opening_time and date parameteres are invalid')

    #opening_time = '11:48-23:18'       '2021-09-06T23:18:00z'
    is_opening = check_opening_time(param_list[0], param_list[1])
    print('Open' if is_opening else 'Close')

if __name__ == "__main__":
    main()