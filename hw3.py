"""
Алгоритм Дейкстри для пошуку найкоротших шляхів у зваженому графі
з використанням бінарної купи (модуль heapq).
"""

import heapq


class Graph:
    """Зважений граф на списках суміжності."""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adjacency = {}

    def add_vertex(self, vertex):
        """Додає вершину без ребер."""
        self.adjacency.setdefault(vertex, [])

    def add_edge(self, source, target, weight: float):
        """Додає ребро. Від'ємні ваги алгоритм Дейкстри не підтримує."""
        if weight < 0:
            raise ValueError(
                f"Від'ємна вага ребра {source} -> {target}: {weight}. "
                "Алгоритм Дейкстри працює лише з невід'ємними вагами."
            )
        self.add_vertex(source)
        self.add_vertex(target)
        self.adjacency[source].append((target, weight))
        if not self.directed:
            self.adjacency[target].append((source, weight))

    @property
    def vertices(self):
        return list(self.adjacency.keys())

    def __str__(self):
        lines = []
        for vertex, neighbors in sorted(self.adjacency.items()):
            edges = ", ".join(f"{n}({w})" for n, w in sorted(neighbors))
            lines.append(f"  {vertex}: {edges}")
        return "\n".join(lines)


def dijkstra(graph: Graph, start):
    """
    Знаходить найкоротші відстані від start до всіх досяжних вершин.

    Бінарна купа зберігає пари (відстань, вершина) і дає вершину
    з найменшою поточною відстанню за O(log n) замість лінійного пошуку O(n).
    Загальна складність O((V + E) log V).

    Повертає (distances, previous), де previous дозволяє відновити маршрут.
    """
    if start not in graph.adjacency:
        raise ValueError(f"Вершини {start} немає у графі")

    distances = {vertex: float("inf") for vertex in graph.vertices}
    previous = {vertex: None for vertex in graph.vertices}
    distances[start] = 0

    visited = set()
    heap = [(0, start)]                  # бінарна купа: (відстань, вершина)

    while heap:
        current_distance, current = heapq.heappop(heap)

        # Купа може містити застарілі записи для вже опрацьованих вершин:
        # замість дорогої операції decrease-key ми просто додаємо новий запис,
        # а старий пропускаємо тут.
        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.adjacency[current]:
            if neighbor in visited:
                continue
            new_distance = current_distance + weight
            # Релаксація ребра: знайдено коротший шлях до сусіда
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(heap, (new_distance, neighbor))

    return distances, previous


def restore_path(previous: dict, start, target) -> list:
    """Відновлює маршрут від start до target за словником попередників."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path if path and path[0] == start else []


def print_results(graph: Graph, start):
    """Виводить таблицю найкоротших шляхів від заданої вершини."""
    distances, previous = dijkstra(graph, start)

    print(f"\nНайкоротші шляхи від вершини «{start}»")
    print("-" * 56)
    print(f"{'Вершина':<10} | {'Відстань':>9} | {'Маршрут'}")
    print("-" * 56)

    for vertex in sorted(distances, key=lambda v: (distances[v] == float("inf"), distances[v])):
        distance = distances[vertex]
        if distance == float("inf"):
            print(f"{vertex:<10} | {'недосяжна':>9} | -")
        else:
            path = " -> ".join(restore_path(previous, start, vertex))
            print(f"{vertex:<10} | {distance:>9} | {path}")


if __name__ == "__main__":
    # Тестовий граф: спрощена мережа маршрутів
    graph = Graph(directed=False)
    edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3),
    ]
    for source, target, weight in edges:
        graph.add_edge(source, target, weight)

    graph.add_vertex("Z")               # ізольована вершина для перевірки недосяжності

    print("Граф (список суміжності):")
    print(graph)

    print_results(graph, "A")

    # Перевірка результату для вершини F вручну:
    # A -> C (2) -> B (1) -> D (5) -> E (2) -> F (3) = 13
    distances, previous = dijkstra(graph, "A")
    assert distances["F"] == 13, f"Очікували 13, отримали {distances['F']}"
    assert restore_path(previous, "A", "F") == ["A", "C", "B", "D", "E", "F"]
    print("\nПеревірка маршруту до F пройдена.")

    # Орієнтований граф
    print("\n" + "=" * 56)
    print("ОРІЄНТОВАНИЙ ГРАФ")
    print("=" * 56)
    digraph = Graph(directed=True)
    for source, target, weight in [("A", "B", 1), ("B", "C", 2), ("C", "A", 4), ("A", "D", 7)]:
        digraph.add_edge(source, target, weight)
    print_results(digraph, "A")

    # Захист від від'ємних ваг
    print("\n" + "=" * 56)
    try:
        Graph().add_edge("X", "Y", -3)
    except ValueError as error:
        print(f"Очікувана помилка: {error}")
