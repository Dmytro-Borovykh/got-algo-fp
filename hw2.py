"""
Побудова фракталу «дерево Піфагора» з використанням рекурсії та модуля turtle.

Використання:
    python pythagoras_tree.py            # рівень рекурсії запитається інтерактивно
    python pythagoras_tree.py 8          # рівень рекурсії передано аргументом
"""

import sys
import turtle

ANGLE = 30              # кут відхилення гілки від напрямку стовбура, градуси
SHRINK = 0.75           # у скільки разів кожна наступна гілка коротша
MAX_LEVEL = 12          # обмеження: кількість гілок зростає як 2^n


def draw_branch(t: turtle.Turtle, length: float, level: int) -> None:
    """
    Рекурсивно малює гілку дерева.

    Базовий випадок (level == 0) означає, що гілку далі не розгалужуємо.
    Крок рекурсії: малюємо відрізок, потім з його кінця будуємо дві
    коротші гілки під кутами +ANGLE та -ANGLE, після чого повертаємо
    черепашку у вихідний стан.
    """
    if level == 0:
        return

    # Товщина гілки спадає разом з рівнем: стовбур товстіший за гілочки
    t.pensize(max(1, level))
    t.forward(length)

    # Ліва гілка
    t.left(ANGLE)
    draw_branch(t, length * SHRINK, level - 1)
    t.right(ANGLE)

    # Права гілка
    t.right(ANGLE)
    draw_branch(t, length * SHRINK, level - 1)
    t.left(ANGLE)

    # Повертаємось у точку, з якої почали цю гілку
    t.backward(length)


def draw_tree(level: int, trunk_length: float = 120) -> None:
    """Готує вікно та черепашку і запускає рекурсивне малювання."""
    screen = turtle.Screen()
    screen.title(f"Дерево Піфагора — рівень рекурсії {level}")
    screen.bgcolor("white")
    screen.tracer(0)                    # вимикаємо анімацію, малюємо миттєво

    t = turtle.Turtle()
    t.color("firebrick")
    t.hideturtle()

    # Стовбур росте вгору з нижньої частини екрана
    t.penup()
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()

    draw_branch(t, trunk_length, level)

    screen.update()
    screen.exitonclick()                # вікно закривається кліком миші


def get_level() -> int:
    """Отримує рівень рекурсії з аргументів командного рядка або від користувача."""
    raw = sys.argv[1] if len(sys.argv) > 1 else input(f"Введіть рівень рекурсії (1-{MAX_LEVEL}): ")

    try:
        level = int(raw)
    except ValueError:
        print("Помилка: рівень рекурсії має бути цілим числом.", file=sys.stderr)
        sys.exit(1)

    if level < 1:
        print("Помилка: рівень рекурсії має бути не меншим за 1.", file=sys.stderr)
        sys.exit(1)
    if level > MAX_LEVEL:
        print(f"Попередження: рівень > {MAX_LEVEL} малюється дуже довго. "
              f"Обмежено до {MAX_LEVEL}.")
        level = MAX_LEVEL

    return level


if __name__ == "__main__":
    draw_tree(get_level())
