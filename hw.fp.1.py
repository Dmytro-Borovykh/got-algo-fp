"""
Однозв'язний список: реверсування, сортування злиттям, об'єднання двох
відсортованих списків.
"""


class Node:
    """Вузол однозв'язного списку."""

    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """Однозв'язний список."""

    def __init__(self):
        self.head = None

    # ------------------------------------------------ базові операції

    def insert_at_end(self, data):
        """Додає елемент у кінець списку. Складність O(n)."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def from_list(self, values):
        """Заповнює список зі звичайного Python-списку."""
        for value in values:
            self.insert_at_end(value)
        return self

    def to_list(self):
        """Повертає вміст у вигляді звичайного Python-списку."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __str__(self):
        return " -> ".join(str(v) for v in self.to_list()) or "(порожній)"

    # --------------------------------------------------- реверсування

    def reverse(self):
        """
        Реверсує список, перенаправляючи посилання між вузлами.

        Нові вузли не створюються: на кожному кроці next поточного вузла
        перекидається на попередній. Складність O(n), пам'ять O(1).
        """
        previous = None
        current = self.head

        while current:
            next_node = current.next    # запам'ятовуємо наступний, бо зараз втратимо посилання
            current.next = previous     # розвертаємо стрілку назад
            previous = current          # зсуваємо обидва вказівники вперед
            current = next_node

        self.head = previous            # останній вузол став першим
        return self

    # ----------------------------------------------------- сортування

    @staticmethod
    def _split(head):
        """
        Ділить список навпіл методом двох вказівників.

        Повільний робить один крок, швидкий два. Коли швидкий досягає кінця,
        повільний стоїть на середині.
        """
        if head is None or head.next is None:
            return head, None

        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        middle = slow.next
        slow.next = None                # розриваємо зв'язок між половинами
        return head, middle

    @staticmethod
    def _merge_nodes(left, right):
        """Зливає два відсортовані ланцюжки вузлів в один відсортований."""
        dummy = Node()                  # фіктивна голова спрощує код: не треба окремо обробляти перший елемент
        tail = dummy

        while left and right:
            if left.data <= right.data:     # <= робить сортування стабільним
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next

        tail.next = left if left else right   # дочіпляємо залишок непорожнього списку
        return dummy.next

    def merge_sort(self):
        """
        Сортування злиттям для однозв'язного списку. Складність O(n log n).

        Для зв'язних списків це природний вибір: злиття вимагає лише
        перенаправлення посилань, тоді як швидке сортування потребує
        доступу за індексом, якого тут немає.
        """
        self.head = self._merge_sort_nodes(self.head)
        return self

    @classmethod
    def _merge_sort_nodes(cls, head):
        """Рекурсивна частина сортування злиттям."""
        if head is None or head.next is None:
            return head                       # базовий випадок: 0 або 1 елемент

        left, right = cls._split(head)
        return cls._merge_nodes(
            cls._merge_sort_nodes(left),
            cls._merge_sort_nodes(right),
        )


# --------------------------------------- об'єднання двох списків

def merge_sorted_lists(list_a: LinkedList, list_b: LinkedList) -> LinkedList:
    """
    Об'єднує два вже відсортовані списки в один відсортований.

    Вузли не копіюються, лише перезчіплюються, тому пам'ять O(1),
    а час O(n + m). Вхідні списки після виклику стають порожніми.
    """
    result = LinkedList()
    result.head = LinkedList._merge_nodes(list_a.head, list_b.head)
    list_a.head = None                  # вузли перейшли до result
    list_b.head = None
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("1. РЕВЕРСУВАННЯ")
    print("=" * 60)
    lst = LinkedList().from_list([1, 2, 3, 4, 5])
    print(f"До:    {lst}")
    print(f"Після: {lst.reverse()}")
    print(f"Порожній список: {LinkedList().reverse()}")
    print(f"Один елемент:    {LinkedList().from_list([7]).reverse()}")

    print("\n" + "=" * 60)
    print("2. СОРТУВАННЯ ЗЛИТТЯМ")
    print("=" * 60)
    values = [38, 27, 43, 3, 9, 82, 10, 3]
    lst = LinkedList().from_list(values)
    print(f"До:    {lst}")
    lst.merge_sort()
    print(f"Після: {lst}")
    assert lst.to_list() == sorted(values), "Сортування працює некоректно"
    print(f"Звірка з sorted(): {sorted(values)}  ->  збігається")

    print("\n" + "=" * 60)
    print("3. ОБ'ЄДНАННЯ ДВОХ ВІДСОРТОВАНИХ СПИСКІВ")
    print("=" * 60)
    a = LinkedList().from_list([1, 3, 5, 7, 9])
    b = LinkedList().from_list([2, 4, 6, 8, 10, 12])
    print(f"Список A: {a}")
    print(f"Список B: {b}")
    merged = merge_sorted_lists(a, b)
    print(f"Разом:    {merged}")
    assert merged.to_list() == sorted([1, 3, 5, 7, 9] + [2, 4, 6, 8, 10, 12])

    # Граничні випадки об'єднання
    empty = LinkedList()
    only = LinkedList().from_list([1, 2, 3])
    print(f"\nПорожній + [1, 2, 3]: {merge_sorted_lists(empty, only)}")
    print(f"Порожній + порожній:  {merge_sorted_lists(LinkedList(), LinkedList())}")
