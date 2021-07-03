from rest_framework.response import Response

def validate_user(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('email') is None:
            return Response({'Email is required field'})
        if kwargs.get('username') is None:
            return Response({'Username is required field'})
        if kwargs.get('password') is None:
            return Response({'Password is required field'})
        return func(*args, **kwargs)
    return wrapper