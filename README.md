# Categories

## Instalation

Create virtual environment
```
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

Set up projects database and fill it with example data
```
python manage.py migrate
python manage.py loaddata fixtures/example.json
```

This will also create superuser account named viki with password `viki`.

Run server on port 8000:
```
python manage.py runserver
```
It also exposes an admin panel on http://localhost:8000/admin


Run tests
```
python manage.py test
```
## API

###  /categories/

On GET return all categories

Example:

request:
```
GET /categories/
```

response:
```json
[
  {
    "id": 1,
    "name": "Краставици",
    "description": "свежи и сочни",
    "image": "http://localhost:8000/media/images/%D0%B3%D1%8A%D0%B1%D0%BA%D0%B0.jpg",
    "parent": null
  },
  {
    "id": 2,
    "name": "ябълки",
    "description": "here",
    "image": "http://localhost:8000/media/images/%D0%B2%D1%80%D0%B0%D0%B1%D1%87%D0%B5.jpg",
    "parent": 1
  },
  {
    "id": 8,
    "name": "диня",
    "description": "сочна и червена",
    "image": "http://localhost:8000/media/images/%D0%B4%D0%B8%D0%BD%D1%8F.jpeg",
    "parent": 2
  }
]
```

On POST add new category and return it on success

Exaple:

request:
```json
POST /categories/
{
    "name": "orange",
    "description": "example",
}
```
response:
```json
{
    "id": 5,
    "name": "orange",
    "description": "example"
}
```

### /categories/{id}/

On GET return category with id

Example:

request:
```
GET /categories/1/
```
response:
```json
{
    "id": 1,
    "name": "Краставици",
    "description": "свежи и сочни",
    "image": "http://localhost:8000mediaimages%D0%B3%D1%8A%D0%B1%D0%BA%D0%B0.jpg",
    "parent": null
}
```
On PUT update category information

Example:

request:
```json
PUT /categories/1/ 
{
    "id": 1,
    "name": "Краставици",
    "description": "свежи и сочни",
    "parent": 2
}
```

response:
```json
{
    "id": 1,
    "name": "Краставици",
    "description": "свежи и сочни",
    "image": "http://localhost:8000mediaimages%D0%B3%D1%8A%D0%B1%D0%BA%D0%B0.jpg",
    "parent": 2
}
```
On DELETE remove category with id

### /categories/1/upload/

On PUT send image and add it to category with id

### /categories/{id}/{type}/

Retrieve categories in different ways, depending on {type}

`subcategories` - returns all direct subcategories of category with id
`leaves` - returns all descendants of category with id which doesn't have subcategories
`siblings` - returns categories with same parent as category with id
`descendants` - returns all subcategories of category with id

### /similarity/

On GET return all similarities

Example:

request:
```
GET /similarity/
```

response:
```json
[
  {
    "first": 1,
    "second": 8
  },
  {
    "first": 1,
    "second": 4
  },
  {
    "first": 1,
    "second": 2
  },
  {
    "first": 6,
    "second": 7
  }
]
```

On POST add new similarity and return it on success

Exaple:

request:
```json
POST /categories/
{
    "first": 3,
    "second": 4
}
```
response:
```json
{
    "first": 3,
    "second": 4
}
```

### /categories/{id}/similar/

On GET returns list of all similar categories to category with id

On POST add new similar category to category with id. Returns 208 if they are already similar
Exaple:

request:
```json
POST /categories/1/similar/
{
    "category": 2
}
```
Make 1 and 2 similar

On PATCH remove similar category to category with id
Exaple:

request:
```json
PATCH /categories/1/similar/
{
    "category": 2
}
```
Remove similarity between 1 and 2

## Commands

### rabbit_hole

Print longest rabbit hole and all rabbit islands
```
python manage.py rabbit_hole
```