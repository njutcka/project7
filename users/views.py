from rest_framework.generics import CreateAPIView, RetrieveAPIView
from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()