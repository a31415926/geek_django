from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from my_shop.models import *
from api.serializers import *



class CategoriesView(APIView):
    def get(self, request, format=None):
        categories_list = Categories.objects.all()
        serializer = CategorySerializer(categories_list, many=True)
        return Response({'success':serializer.data})

    def post(self, request, format=None):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesDetailView(APIView):
    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        _category = self.get_object(pk) 
        serializer = CategorySerializer(_category)
        return Response({'success':serializer.data})
    
    def put(self, request, pk, format=None):
        _category = self.get_object(pk)
        serializer = CategorySerializer(_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        _category = self.get_object(pk)
        _category.delete()
        return Response({'success'}, status=status.HTTP_200_OK)
    


# Create your views here.
