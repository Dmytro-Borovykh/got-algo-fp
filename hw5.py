"""
Візуалізація обходів бінарного дерева: у глибину (DFS) та в ширину (BFS).

Обидва обходи реалізовані ітеративно:
    DFS -> стек (list з методами append / pop)
    BFS -> черга (collections.deque з методами append / popleft)

Порядок відвідування показано кольором вузла: від темного до світлого.
"""

import uuid
from collections import deque

import networkx as nx
import matplotlib
matplotlib.use("Agg")               # робота без графічного дисплея
import matplotlib.pyplot as plt


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, key, color="#CCCCCC"):
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


def build_heap_tree(heap: list, index: int = 0):
    """Перетворює масив купи на дерево: нащадки елемента i лежать на 2i+1 та 2i+2."""
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = build_heap_tree(heap, 2 * index + 1)
    node.right = build_heap_tree(heap, 2 * index + 2)
    return node


# ------------------------------------------------ генерація кольорів

def generate_colors(count: int, base_rgb=(18, 60, 140)) -> list:
    """
    Генерує count кольорів у форматі #RRGGBB від темного до світлого.

    Кожен канал лінійно інтерполюється від базового (темного) значення
    до майже білого. Індекс кольору відповідає порядку відвідування:
    перший відвіданий вузол найтемніший, останній найсвітліший.
    """
    if count == 0:
        return []
    if count == 1:
        return [f"#{base_rgb[0]:02X}{base_rgb[1]:02X}{base_rgb[2]:02X}"]

    colors = []
    for i in range(count):
        ratio = i / (count - 1)             # від 0.0 до 1.0
        rgb = tuple(int(channel + (235 - channel) * ratio) for channel in base_rgb)
        colors.append(f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}")
    return colors


def count_nodes(root) -> int:
    """Рахує кількість вузлів у дереві (ітеративно, через стек)."""
    if root is None:
        return 0
    total = 0
    stack = [root]
    while stack:
        node = stack.pop()
        total += 1
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return total


# ------------------------------------------------------------ обходи

def dfs_iterative(root) -> list:
    """
    Обхід у глибину з використанням СТЕКУ (без рекурсії).

    Правий нащадок кладеться у стек раніше за лівого, щоб лівий
    вийшов першим: стек працює за принципом LIFO.
    Повертає список вузлів у порядку відвідування (preorder).
    """
    if root is None:
        return []

    visited = []
    stack = [root]

    while stack:
        node = stack.pop()              # беремо з вершини стека
        visited.append(node)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return visited


def bfs_iterative(root) -> list:
    """
    Обхід у ширину з використанням ЧЕРГИ (без рекурсії).

    Черга працює за принципом FIFO, тому вузли опрацьовуються
    рівень за рівнем зліва направо.
    """
    if root is None:
        return []

    visited = []
    queue = deque([root])

    while queue:
        node = queue.popleft()          # беремо з початку черги

        visited.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return visited


# ---------------------------------------------------- візуалізація

def colorize(order: list, base_rgb) -> None:
    """Призначає вузлам кольори відповідно до порядку відвідування."""
    colors = generate_colors(len(order), base_rgb)
    for node, color in zip(order, colors):
        node.color = color


def draw_traversal(root, order: list, title: str, filename: str) -> None:
    """Малює дерево з підписаним порядком обходу."""
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    colors = [tree.nodes[node_id]["color"] for node_id in tree.nodes()]
    labels = {node_id: tree.nodes[node_id]["label"] for node_id in tree.nodes()}

    plt.figure(figsize=(12, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2000, node_color=colors,
            font_color="white", font_size=10, font_weight="bold")

    sequence = " -> ".join(str(node.val) for node in order)
    plt.title(f"{title}\nПорядок відвідування: {sequence}", fontsize=11)

    plt.savefig(filename, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"Збережено: {filename}")


def print_order(name: str, order: list, base_rgb) -> None:
    """Виводить крок за кроком порядок обходу з відповідними кольорами."""
    colors = generate_colors(len(order), base_rgb)
    print(f"\n{name}")
    print("-" * 40)
    for step, (node, color) in enumerate(zip(order, colors), 1):
        print(f"  Крок {step:>2}: вузол {str(node.val):<4} колір {color}")


if __name__ == "__main__":
    values = [3, 9, 6, 10, 84, 19, 17, 22, 15]

    # DFS
    root_dfs = build_heap_tree(values)
    order_dfs = dfs_iterative(root_dfs)
    colorize(order_dfs, base_rgb=(18, 60, 140))          # синя гама
    print_order("ОБХІД У ГЛИБИНУ (DFS, стек)", order_dfs, (18, 60, 140))
    draw_traversal(root_dfs, order_dfs,
                   "Обхід у глибину (DFS) з використанням стека", "dfs_traversal.png")

    # BFS: будуємо дерево заново, щоб кольори не перемішались
    root_bfs = build_heap_tree(values)
    order_bfs = bfs_iterative(root_bfs)
    colorize(order_bfs, base_rgb=(140, 25, 25))          # червона гама
    print_order("ОБХІД У ШИРИНУ (BFS, черга)", order_bfs, (140, 25, 25))
    draw_traversal(root_bfs, order_bfs,
                   "Обхід у ширину (BFS) з використанням черги", "bfs_traversal.png")

    # Перевірка: обидва обходи мають відвідати всі вузли рівно один раз
    total = count_nodes(build_heap_tree(values))
    assert len(order_dfs) == total, "DFS відвідав не всі вузли"
    assert len(order_bfs) == total, "BFS відвідав не всі вузли"
    assert {n.val for n in order_dfs} == {n.val for n in order_bfs} == set(values)
    print(f"\nОбидва обходи відвідали всі {total} вузлів рівно один раз.")
