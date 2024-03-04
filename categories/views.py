from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from categories.models import Category, Similarity
from categories.serializers import CategorySerializer, SimilaritySerializer


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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Add patch method
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


class SimilarityList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if Similarity.objects.filter(
            first__id=request.data["first"], second__id=request.data["second"]
        ):
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        if Similarity.objects.filter(
            first__id=request.data["second"], second__id=request.data["first"]
        ):
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        return self.create(request, *args, **kwargs)


class SimilarityDetail(
    generics.ListAPIView,
):
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer

    def _get_similarity(self, first, second):
        similarity = Similarity.objects.filter(
            first__id=first, second__id=second
        ).first()
        if similarity is None:
            similarity = Similarity.objects.filter(
                first__id=second, second__id=first
            ).first()
        return similarity

    def get_queryset(self):
        category_id = self.kwargs.get("pk", None)
        similarities = Similarity.objects.filter(
            Q(first__id=category_id) | Q(second__id=category_id)
        )
        return similarities

    def post(self, request, *args, **kwargs):
        similarity = self._get_similarity(kwargs["pk"], request.data["category"])
        if similarity:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)

        data = {"first": kwargs["pk"], "second": request.data["category"]}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        similarity = self._get_similarity(kwargs["pk"], request.data["category"])
        if similarity:
            similarity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
