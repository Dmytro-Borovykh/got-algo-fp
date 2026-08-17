"""
Симуляція кидання двох гральних кубиків методом Монте-Карло.

Обчислює емпіричні ймовірності кожної суми (від 2 до 12) та порівнює їх
з аналітичними значеннями.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")               # робота без графічного дисплея
import matplotlib.pyplot as plt

SUMS = list(range(2, 13))

# Аналітичні ймовірності: кількість способів отримати суму, поділена на 36
ANALYTICAL = {s: (6 - abs(7 - s)) / 36 for s in SUMS}


def simulate(n: int, seed: int = None) -> dict:
    """
    Кидає два кубики n разів і повертає частоту кожної суми.

    Обидва кубики генеруються векторизовано, без циклу Python:
    np.bincount рахує входження кожного значення за один прохід.
    """
    rng = np.random.default_rng(seed)

    die_1 = rng.integers(1, 7, n)       # верхня межа не включається
    die_2 = rng.integers(1, 7, n)
    totals = die_1 + die_2

    counts = np.bincount(totals, minlength=13)
    return {s: int(counts[s]) for s in SUMS}


def print_table(counts: dict, n: int) -> None:
    """Друкує таблицю порівняння емпіричних та аналітичних імовірностей."""
    print(f"\n{'=' * 74}")
    print(f"РЕЗУЛЬТАТИ СИМУЛЯЦІЇ ({n:,} кидків)".replace(",", " "))
    print(f"{'=' * 74}")
    print(f"{'Сума':>5} | {'Випадінь':>10} | {'Монте-Карло':>12} | "
          f"{'Аналітично':>12} | {'Відхилення':>11}")
    print("-" * 74)

    max_deviation = 0
    for s in SUMS:
        empirical = counts[s] / n
        theoretical = ANALYTICAL[s]
        deviation = abs(empirical - theoretical) / theoretical * 100
        max_deviation = max(max_deviation, deviation)
        ways = int(theoretical * 36)
        print(f"{s:>5} | {counts[s]:>10} | {empirical * 100:>11.4f}% | "
              f"{theoretical * 100:>10.4f}% ({ways}/36) | {deviation:>10.2f}%")

    print("-" * 74)
    print(f"Сума ймовірностей: {sum(counts.values()) / n * 100:.2f}%")
    print(f"Максимальне відносне відхилення: {max_deviation:.2f}%")


def convergence(n_values: list) -> None:
    """Показує, як точність зростає зі збільшенням кількості кидків."""
    print(f"\n{'=' * 74}")
    print("ЗБІЖНІСТЬ: максимальне відхилення від аналітичних значень")
    print(f"{'=' * 74}")
    print(f"{'Кидків':>12} | {'Макс. відхилення':>18} | {'P(7), %':>10} | {'P(2), %':>10}")
    print("-" * 60)

    for n in n_values:
        counts = simulate(n, seed=42)
        deviations = [abs(counts[s] / n - ANALYTICAL[s]) / ANALYTICAL[s] * 100 for s in SUMS]
        print(f"{n:>12,} | {max(deviations):>17.2f}% | "
              f"{counts[7] / n * 100:>9.3f} | {counts[2] / n * 100:>9.3f}".replace(",", " "))


def make_plot(counts: dict, n: int, filename: str = "dice_probabilities.png") -> None:
    """Будує стовпчикову діаграму порівняння емпіричних та аналітичних імовірностей."""
    empirical = [counts[s] / n * 100 for s in SUMS]
    theoretical = [ANALYTICAL[s] * 100 for s in SUMS]

    x = np.arange(len(SUMS))
    width = 0.38

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Ліва панель: порівняння стовпчиків
    ax1.bar(x - width / 2, empirical, width, label="Монте-Карло", color="#2e75b6")
    ax1.bar(x + width / 2, theoretical, width, label="Аналітично", color="#c00000", alpha=0.75)
    ax1.set_xticks(x)
    ax1.set_xticklabels(SUMS)
    ax1.set_xlabel("Сума на двох кубиках")
    ax1.set_ylabel("Імовірність, %")
    ax1.set_title(f"Розподіл сум ({n:,} кидків)".replace(",", " "))
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    # Права панель: абсолютне відхилення
    deviations = [e - t for e, t in zip(empirical, theoretical)]
    colors = ["#2e75b6" if d >= 0 else "#c00000" for d in deviations]
    ax2.bar(x, deviations, color=colors)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(SUMS)
    ax2.set_xlabel("Сума на двох кубиках")
    ax2.set_ylabel("Відхилення, відсоткові пункти")
    ax2.set_title("Різниця між Монте-Карло та аналітикою")
    ax2.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(filename, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"\nГрафік збережено: {filename}")


if __name__ == "__main__":
    N = 1_000_000

    counts = simulate(N, seed=42)
    print_table(counts, N)
    convergence([100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000])
    make_plot(counts, N)
