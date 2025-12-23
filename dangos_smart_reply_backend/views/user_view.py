from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from ..middlewares.authentications import BearerTokenAuthentication
from ..middlewares.permissions import IsSuperUser
from ..serializers import UserSerializer
from ..models import UserToken, RefreshToken
    
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def create_user(request):
    try:
        User = get_user_model()

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        image = request.FILES.get('image')

        if User.objects.filter(email=email).exists():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request_data = request.data.copy()
        request_data['username'] = username
        request_data['first_name'] = username
        request_data['password'] = password

        if image:
            request_data['image'] = image

        serializer = UserSerializer(data=request_data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            access = UserToken.objects.create(user=user)
            refresh = RefreshToken.objects.create(user=user)
            user_serializer = UserSerializer(instance=user, context={'request': request})
            data = user_serializer.data
            data['access_token'] = access.key
            data['refresh_token'] = refresh.key

            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Register successful",
                "data": data,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsSuperUser])
def fetch_users(request):
    try:
        page = int(request.GET.get('page'))
        page_size = int(request.GET.get('page_size'))
        query_param = request.GET.get("query", "").strip()

        User = get_user_model()
        users = User.objects.all()
        
        if query_param:
            users = users.filter(email__icontains=query_param) | users.filter(phone_number__icontains=query_param)
        
        users = users.order_by('-date_joined')
        user_serializer = UserSerializer(users, many=True, context={'request': request})
        data = user_serializer.data
        start = (page - 1) * page_size
        end = start + page_size
        data = data[start:end]

        return Response({
            "status": status.HTTP_200_OK,
            "message": "Users fetched successfully.",
            "total_item": len(data),
            "page": page,
            "page_size": page_size,
            "total_page": (users.count() + page_size - 1) // page_size,
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_user(request, id):
    try:
        User = get_user_model()
        user = User.objects.get(id=id)
        user_serializer = UserSerializer(user, context={'request': request})
        data = user_serializer.data

        return Response({
            "status": status.HTTP_200_OK,
            "message": "User fetched successfully.",
            "data": data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["PUT"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    try:
        User = get_user_model()
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        email = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        image = request.FILES.get('image')
        
        if email and User.objects.filter(email=email).exclude(id=user.id).exists():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request_data = request.data.copy()
        
        serializer = UserSerializer(user, data=request_data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            updated_user = serializer.save()
            if password:
                updated_user.set_password(password)
                updated_user.save()
            
            user_serializer = UserSerializer(instance=updated_user, context={'request': request})
            
            return Response({
                "status": status.HTTP_200_OK,
                "message": "User updated successfully",
                "data": user_serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["DELETE"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsSuperUser])
def delete_users(request):
    try:
        ids = request.data.get('ids')
        if not isinstance(ids, list):
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "ids must be an array"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not ids:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "No ids provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            ids_int = [int(i) for i in ids]
        except Exception:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "All ids must be integers"
            }, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        users_qs = User.objects.filter(id__in=ids_int)
        existing_ids = list(users_qs.values_list('id', flat=True))
        UserToken.objects.filter(user__id__in=existing_ids).delete()
        users_qs.delete()

        return Response({
            "status": status.HTTP_200_OK,
            "message": f"{len(existing_ids)} Users deleted successfully",
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)