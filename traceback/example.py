import logging
import sys
import traceback

def f(x, y):
    return x/y

def g(x):
    return x+1


if __name__ == '__main__':
    try:
        f(10, g(-1))
    except Exception as e:
        #print(str(e))
        print('method1:')
        exc_type, exc_value, exc_tb = sys.exc_info()
        tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
        print(''.join(tbe.format()))

        print('\nmethod2:')
        traceback.print_exc(file=sys.stdout)

        print('\nmethod3:')
        logging.exception('exection!')

