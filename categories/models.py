from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} id {}".format(self.name, self.id)


class Similarity(models.Model):
    first = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="first")
    second = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="second"
    )

    def __str__(self):
        return "{} ~ {}".format(self.first.id, self.second.id)
