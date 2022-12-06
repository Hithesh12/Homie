from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

def check(premium_user,price,user,serializer):
    if premium_user is False:
                    user.save()
                    return Response(serializer.data)
    elif premium_user is True and price is False:
                    raise ValidationError('make payment')
    elif premium_user is True and price is True:
                    user.save()
                    return Response(serializer.data)

def check_premium_update(premium_user,price,user):
    if premium_user is False:
                    user.save()
                    return Response('sucessfull',status=status.HTTP_200_OK)
    elif premium_user is True and price is False:
                    raise ValidationError('make payment')
    elif premium_user is True and price is True:
                    user.save()
                    return Response('sucessfull',status=status.HTTP_200_OK)