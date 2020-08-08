from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from profiles.models.profilePicture import ProfilePicture
from profiles.models.user import User
from profiles.serializers.fakeUsersSerializers import FakeUserSerializer
from profiles.serializers.profilePictureSerializers import GetProfilePictureSerializer
from profiles.utils.userUtils import generate_birthday_from_age, generate_fake_phone_number


class CreateFakeUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FakeUserSerializer(data=request.data)
        user = request.user
        if not user.is_superuser:
            return Response(data={"message": "you do not have permission to add fake users"},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            try:
                image1 = serializer.validated_data.get('profile_picture1')
                image2 = serializer.validated_data.get('profile_picture2')
                image3 = serializer.validated_data.get('profile_picture3')
                image4 = serializer.validated_data.get('profile_picture4')
                image5 = serializer.validated_data.get('profile_picture5')
                name = serializer.validated_data.get('name')
                bio = serializer.validated_data.get('bio')
                school = serializer.validated_data.get('school')
                job = serializer.validated_data.get('job')
                gender = serializer.validated_data.get('gender')
                age = serializer.validated_data.get('age')
                city = serializer.validated_data.get('city')
                latitude = serializer.validated_data.get('latitude')
                longitude = serializer.validated_data.get('longitude')
                try:
                    birthday = generate_birthday_from_age(age)
                    phone_number = generate_fake_phone_number()
                    location = Point(longitude, latitude)
                    fake_user = User(is_fake=True, username=phone_number, phone_number=phone_number, gender=gender,
                                     name=name, location=location, birthday=birthday, is_active=True,
                                     is_superuser=False, is_phone_number_verified=True, is_info_initialized=True,
                                     is_staff=False)
                    if bio:
                        fake_user.bio = bio
                    if school:
                        fake_user.school = school
                    if job:
                        fake_user.job = job
                    if city:
                        fake_user.city = city
                    fake_user.save()
                    if image1:
                        ProfilePicture.objects.create(user=fake_user, image=image1, thumbnail=image1, priority=1)
                    if image2:
                        ProfilePicture.objects.create(user=fake_user, image=image2, thumbnail=image2, priority=2)
                    if image3:
                        ProfilePicture.objects.create(user=fake_user, image=image3, thumbnail=image3, priority=3)
                    if image4:
                        ProfilePicture.objects.create(user=fake_user, image=image4, thumbnail=image4, priority=4)
                    if image5:
                        ProfilePicture.objects.create(user=fake_user, image=image5, thumbnail=image5, priority=5)
                    return Response(data={'message': 'success'}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={'message': 'something went wrong in creating user'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                # Handle Exception
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)