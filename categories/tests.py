import json
import tempfile
from PIL import Image

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from categories.models import Category


class CategoryTests(APITestCase):
    def test_create_category(self):
        data = {"name": "банани", "description": "Еквадор"}
        response = self.client.post("/categories/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "банани")

    def test_list_categories(self):
        data = {"name": "банани", "description": "Еквадор"}
        self.client.post("/categories/", data, format="json")
        data = {"name": "круши", "description": "Кичево"}
        self.client.post("/categories/", data, format="json")
        response = self.client.get("/categories/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.getvalue())), 2)

    def test_list_category_with_id(self):
        data = {"name": "банани", "description": "Еквадор"}
        self.client.post("/categories/", data, format="json")
        response = self.client.get("/categories/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.getvalue())["name"], "банани")

    def test_create_subcategory(self):
        data = {"name": "банани", "description": "Еквадор"}
        self.client.post("/categories/", data, format="json")
        data = {"name": "круши", "description": "Кичево"}
        self.client.post("/categories/1/", data, format="json")
        response = self.client.get("/categories/2/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get(pk=2).parent.id, 1)

    def test_update_category(self):
        data = {"name": "банани", "description": "Еквадор"}
        self.client.post("/categories/", data, format="json")
        data["description"] = "Боливия"
        response = self.client.put("/categories/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.getvalue())["description"], "Боливия")

    def test_delete_category(self):
        data = {"name": "банани", "description": "Еквадор"}
        response = self.client.post("/categories/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        response = self.client.delete("/categories/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_upload_image(self):
        data = {"name": "банани", "description": "Еквадор"}
        self.client.post("/categories/", data, format="json")
        category = Category.objects.get()
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg", prefix="test_img_")
        image.save(tmp_file, "jpeg")
        tmp_file.seek(0)
        data = {"file": tmp_file}
        response = self.client.put("/categories/1/upload/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(category.image)
        # TODO Check why this is not working
        category.image.delete(True)


class CategoriesListingTest(APITestCase):
    def setUp(self):
        category_names = ["банани", "ябълки", "круши", "ягоди", "малини"]
        for name in category_names:
            data = {"name": name, "description": "text"}
            self.client.post("/categories/", data, format="json")
        data = {"name": name, "description": "text"}
        data["parent"] = 1
        self.client.put("/categories/2/", data, format="json")
        self.client.put("/categories/3/", data, format="json")
        data["parent"] = 2
        self.client.put("/categories/4/", data, format="json")
        data["parent"] = 3
        self.client.put("/categories/5/", data, format="json")

    def test_list_subcategories(self):
        self.assertEqual(Category.objects.count(), 5)
        response = self.client.get("/categories/1/subcategories/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [category["id"] for category in json.loads(response.getvalue())]
        self.assertEqual(result, [2, 3])

    def test_list_leaves(self):
        self.assertEqual(Category.objects.count(), 5)
        response = self.client.get("/categories/1/leaves/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [category["id"] for category in json.loads(response.getvalue())]
        self.assertEqual(result, [4, 5])

    def test_list_descendants(self):
        self.assertEqual(Category.objects.count(), 5)
        response = self.client.get("/categories/1/descendants/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [category["id"] for category in json.loads(response.getvalue())]
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_list_siblings(self):
        self.assertEqual(Category.objects.count(), 5)
        response = self.client.get("/categories/2/siblings/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [category["id"] for category in json.loads(response.getvalue())]
        self.assertEqual(result, [2, 3])

    def test_wrong_type_listing(self):
        self.assertEqual(Category.objects.count(), 5)
        response = self.client.get("/categories/2/sfweggr/", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
