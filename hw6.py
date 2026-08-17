"""
Задача вибору страв з максимальною сумарною калорійністю в межах бюджету
(класична задача про рюкзак 0/1).

Реалізовано два підходи:
    greedy_algorithm      - жадібний за співвідношенням калорій до вартості
    dynamic_programming   - динамічне програмування, гарантований оптимум

"""

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int):
    """
    Жадібний алгоритм: сортує страви за спаданням співвідношення
    калорій до вартості і бере кожну наступну, якщо вона вміщується в бюджет.

    Складність O(n log n) через сортування.
    Оптимум НЕ гарантується: локально вигідний вибір може завадити
    зібрати кращий набір далі.

    Повертає (список страв, сумарна вартість, сумарна калорійність).
    """
    # Сортуємо за «цінністю» одиниці вартості
    ranked = sorted(
        items.items(),
        key=lambda pair: pair[1]["calories"] / pair[1]["cost"],
        reverse=True,
    )

    chosen = []
    total_cost = 0
    total_calories = 0

    for name, data in ranked:
        if total_cost + data["cost"] <= budget:
            chosen.append(name)
            total_cost += data["cost"]
            total_calories += data["calories"]

    return chosen, total_cost, total_calories


def dynamic_programming(items: dict, budget: int):
    """
    Динамічне програмування: задача про рюкзак 0/1.

    dp[i][b] це максимальна калорійність, яку можна набрати
    з перших i страв за бюджету b. Перехід на кожному кроці:
        не беремо страву  -> dp[i-1][b]
        беремо страву     -> dp[i-1][b - cost] + calories
    Обираємо максимум з двох варіантів.

    Складність O(n * budget) за часом і пам'яттю. Оптимум гарантований.

    Повертає (список страв, сумарна вартість, сумарна калорійність).
    """
    names = list(items.keys())
    n = len(names)

    # Таблиця (n + 1) x (budget + 1), нульовий рядок означає «страв немає»
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]

        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]                     # варіант: страву не беремо
            if cost <= b:                               # варіант: страву беремо
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)

    # Відновлюємо набір, рухаючись таблицею назад:
    # якщо значення змінилось порівняно з попереднім рядком, страву було взято
    chosen = []
    remaining = budget
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            name = names[i - 1]
            chosen.append(name)
            remaining -= items[name]["cost"]

    chosen.reverse()
    total_cost = sum(items[name]["cost"] for name in chosen)

    return chosen, total_cost, dp[n][budget]


def brute_force(items: dict, budget: int):
    """Повний перебір усіх підмножин. Використовується лише для перевірки."""
    from itertools import combinations

    names = list(items.keys())
    best = ([], 0, 0)

    for size in range(len(names) + 1):
        for combo in combinations(names, size):
            cost = sum(items[name]["cost"] for name in combo)
            if cost <= budget:
                calories = sum(items[name]["calories"] for name in combo)
                if calories > best[2]:
                    best = (list(combo), cost, calories)

    return best


def show(label: str, result: tuple, budget: int) -> None:
    """Друкує результат роботи одного алгоритму."""
    chosen, cost, calories = result
    print(f"  {label}")
    print(f"    Страви:      {', '.join(chosen) if chosen else '(нічого)'}")
    print(f"    Вартість:    {cost} з {budget}")
    print(f"    Калорійність: {calories}")


if __name__ == "__main__":
    print("Меню:")
    for name, data in items.items():
        ratio = data["calories"] / data["cost"]
        print(f"  {name:<12} вартість {data['cost']:>3}, "
              f"калорій {data['calories']:>4}, співвідношення {ratio:.2f}")

    for budget in (40, 60, 100, 170):
        print(f"\n{'=' * 62}")
        print(f"БЮДЖЕТ: {budget}")
        print(f"{'=' * 62}")

        greedy = greedy_algorithm(items, budget)
        dp = dynamic_programming(items, budget)

        show("Жадібний алгоритм:", greedy, budget)
        print()
        show("Динамічне програмування:", dp, budget)

        difference = dp[2] - greedy[2]
        if difference > 0:
            print(f"\n  ДП виграє на {difference} калорій "
                  f"({difference / greedy[2] * 100:.1f}%)")
        else:
            print("\n  Результати збігаються")

    # Перевірка ДП повним перебором
    print(f"\n{'=' * 62}")
    print("ПЕРЕВІРКА ДП ПОВНИМ ПЕРЕБОРОМ")
    print(f"{'=' * 62}")
    mismatches = 0
    for budget in range(0, 201):
        if dynamic_programming(items, budget)[2] != brute_force(items, budget)[2]:
            mismatches += 1
    print(f"Бюджети від 0 до 200: розбіжностей {mismatches}")
