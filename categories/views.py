from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerilizer


@api_view(["GET", "POST"])
def categories(request):

    if request.method == "GET":
        all_categories = Category.objects.all()
        serilizer = CategorySerilizer(all_categories, many=True)
        return Response(serilizer.data)
    elif request.method == "POST":
        serializer = CategorySerilizer(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serilizer = CategorySerilizer(category)
    return Response(serilizer.data)
