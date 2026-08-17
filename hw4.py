"""
Візуалізація бінарної купи у вигляді дерева.

Купа зберігається як масив, де для елемента з індексом i:
    лівий нащадок  -> 2*i + 1
    правий нащадок -> 2*i + 2
Функція build_heap_tree перетворює цей масив на дерево з вузлів Node,
після чого дерево малюється кодом із завдання.

"""

import uuid
import heapq

import networkx as nx
import matplotlib
matplotlib.use("Agg")               # робота без графічного дисплея
import matplotlib.pyplot as plt


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає вузли та ребра, обчислюючи координати для малювання."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


# ------------------------------------------- побудова дерева з купи

def build_heap_tree(heap: list, index: int = 0, depth: int = 0):
    """
    Рекурсивно перетворює масив купи на дерево з вузлів Node.

    Ключова ідея: купа це повне бінарне дерево, записане в масив,
    тому структура дерева повністю визначається індексами.
    Нащадки елемента i лежать на позиціях 2i+1 та 2i+2.

    Колір вузла залежить від глибини: корінь найтемніший, листя найсвітліші.
    Це робить рівні купи візуально помітними.
    """
    if index >= len(heap):
        return None

    palette = ["#1f4e79", "#2e75b6", "#5b9bd5", "#9dc3e6", "#bdd7ee", "#deebf7"]
    node = Node(heap[index], color=palette[min(depth, len(palette) - 1)])

    node.left = build_heap_tree(heap, 2 * index + 1, depth + 1)
    node.right = build_heap_tree(heap, 2 * index + 2, depth + 1)

    return node


def draw_heap(heap: list, title: str = "Бінарна купа", filename: str = None):
    """Малює бінарну купу, задану масивом."""
    if not heap:
        print("Купа порожня, малювати нічого.")
        return

    root = build_heap_tree(heap)

    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(12, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2000, node_color=colors, font_color="white", font_size=10)
    plt.title(f"{title}\n{heap}", fontsize=11)

    if filename:
        plt.savefig(filename, dpi=110, bbox_inches="tight")
        print(f"Збережено: {filename}")
        plt.close()
    else:
        plt.show()


def verify_min_heap(heap: list) -> bool:
    """Перевіряє властивість мінімальної купи: батько не більший за нащадків."""
    for i in range(len(heap)):
        for child in (2 * i + 1, 2 * i + 2):
            if child < len(heap) and heap[i] > heap[child]:
                return False
    return True


if __name__ == "__main__":
    # Мінімальна купа, побудована через heapq
    values = [15, 3, 17, 10, 84, 19, 6, 22, 9]
    min_heap = values.copy()
    heapq.heapify(min_heap)

    print(f"Вихідний масив: {values}")
    print(f"Після heapify:  {min_heap}")
    print(f"Властивість мінімальної купи виконується: {verify_min_heap(min_heap)}")
    draw_heap(min_heap, "Мінімальна купа (min-heap)", "min_heap.png")

    # Максимальна купа: heapq працює лише з мінімальними,
    # тому інвертуємо знаки, будуємо купу і повертаємо знаки назад
    max_heap = [-v for v in values]
    heapq.heapify(max_heap)
    max_heap = [-v for v in max_heap]

    print(f"\nМаксимальна купа: {max_heap}")
    draw_heap(max_heap, "Максимальна купа (max-heap)", "max_heap.png")
