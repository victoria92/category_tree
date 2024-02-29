from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError


from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data["parent"] = kwargs["pk"]
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        image = request.data["file"]
        category = Category.objects.get(pk=pk)
        category.image = image
        category.save()
        return Response(status=status.HTTP_201_CREATED)


class CategoryTreeListing(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        query_type = self.kwargs["type"]
        category = Category.objects.get(pk=self.kwargs["pk"])
        if query_type == "subcategories":
            return Category.objects.filter(parent__id=self.kwargs["pk"])
        elif query_type == "siblings":
            return Category.objects.filter(parent=category.parent)
        elif query_type == "leaves":
            categories_checked = [category]
            result = []
            while categories_checked:
                current = categories_checked[0]
                children = list(Category.objects.filter(parent=current))
                if children == []:
                    result.append(current)
                categories_checked = categories_checked[1:] + children
            return result
        elif query_type == "descendants":
            categories_checked = [category]
            result = []
            while categories_checked:
                current = categories_checked[0]
                result.append(current)
                children = list(Category.objects.filter(parent=current))
                categories_checked = categories_checked[1:] + children
            return result
        else:
            raise ValidationError(
                {
                    "Invalid search type": "{} is not a valid search type option".format(
                        query_type
                    )
                }
            )
