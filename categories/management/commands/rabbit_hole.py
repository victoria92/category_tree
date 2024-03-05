from django.core.management.base import BaseCommand, CommandError

from categories.models import Category, Similarity


class Command(BaseCommand):
    help = "Find the longest similar rabbit hole"

    def _bfs(self, edges, start):
        visited = set()
        to_visit = [start]
        parents = {start: None}
        distances = {start: 0}
        while to_visit:
            current = to_visit.pop(0)
            visited.add(current)
            for e in edges:
                if current in e:
                    neighbour = sum(e) - current
                    if neighbour not in visited and neighbour not in to_visit:
                        to_visit.append(neighbour)
                        parents[neighbour] = current
                        distances[neighbour] = distances[current] + 1

        return distances, parents

    def handle(self, *args, **options):
        vertices = [category.id for category in Category.objects.all()]
        edges = [(s.first.id, s.second.id) for s in Similarity.objects.all()]

        paths = []
        islands = set()
        for v in vertices:
            distances, parents = self._bfs(edges, v)
            vertex = max(distances, key=distances.get)
            path = []
            while vertex:
                path.append(vertex)
                vertex = parents[vertex]
            paths.append(path)
            islands.add(tuple(sorted(distances.keys())))

        max_path = max(paths, key=len)
        self.stdout.write("Longest rabbit hole: {}".format(max_path))
        self.stdout.write("Rabbit islands: {}".format(islands))
