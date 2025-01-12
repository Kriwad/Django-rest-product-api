from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Person
from django.views.decorators.csrf import csrf_exempt
from home.serializers import PersonSerializers

@api_view(['GET', 'POST' , 'PUT'])
def index(request):
  courses = {
      'course_name': "Python",
      'learn': ['flask', 'Django', "Tornado", 'FastApi'],
      'course_provider': "krish",

    }
  if request.method == 'GET':
    print("You hit a get method")
    return Response(courses)
  elif request.method == 'POST':
    data = request.data
    print(data)

    print("You hit Post method")
    return Response(courses)
  elif request.method == 'PUT':
    print("You hit a put method")
    return Response(courses)

@csrf_exempt
@api_view(['GET', 'POST'])
def person(request):
  if request.method == 'GET':
    obj = Person.objects.all()  
    serializer = PersonSerializers(obj , many = True)
    return Response(serializer.data)

  else:
    data = request.data
    serializer = PersonSerializers(data = data )
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)

