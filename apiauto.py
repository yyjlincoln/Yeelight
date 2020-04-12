# API Auto Configuration
from flask import jsonify, request
from functools import wraps
import inspect
import logger

def r(code,**kw):
    kw['code'] = code
    return jsonify(kw)


def auto(**req):
    'Required arguments & default value'
    def _auto(func):
        arguments = inspect.getargspec(func).args

        def _autoType(arg):
            try:
                if str(int(arg))==arg:
                    return int(arg)
            except:
                pass

            try:
                if str(float(arg)) == arg:
                    return float(arg)
            except:
                pass

            try:
                if arg.lower()=='true':
                    return True
                elif arg.lower()=='false':
                    return False
            except:
                pass
            
            return arg


        @wraps(func)
        def __auto(*args, **kw):
            argpass = {}

            for x in req:
                if x in arguments:
                    if request.values.get(x)!=None:
                        argpass[x] = _autoType(request.values.get(x))
                    else:
                        logger.log(f'Substituted default value for argument {x}')
                        argpass[x] = req[x]
                else:
                    logger.info(f'Argument {x} is defined in the requirement list but not defined as a parameter of the function.')

            return func(*args, **argpass, **kw)
        return __auto
    return _auto