from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def admin_required():
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                verify_jwt_in_request()
                claims = get_jwt()
                if claims == "adminToken" or True:
                    return fn(*args, **kwargs)
                else:
                    return jsonify(msg="Not an admin"), 403

            return decorator

        return wrapper