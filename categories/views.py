from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerilizer


class Categories(APIView):

    def get(self, request):
        all_categories = Category.objects.all()
        serilizer = CategorySerilizer(all_categories, many=True)
        return Response(serilizer.data)

    def post(self, request):
        serializer = CategorySerilizer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(
                CategorySerilizer(new_category).data,
            )


class CategoryDetail(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serilizer = CategorySerilizer(self.get_object(pk))
        return Response(serilizer.data)

    def put(self, request, pk):
        serilizer = CategorySerilizer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serilizer.is_valid():
            updated_category = serilizer.save()
            return Response(CategorySerilizer(updated_category).data)
        else:
            return Response(serilizer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
