#!/usr/bin/env python3
"""Рисует график веса из weight_data.csv -> weight.png.

Использование: python3 health/plot_weight.py
Добавить замер: дописать строку date,weight,note в weight_data.csv.
Тренды считаются отдельно по фазам, без замеров из перерывов.
"""
import csv
import datetime as dt
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = Path(__file__).parent
CSV = HERE / "weight_data.csv"
OUT = HERE / "weight.png"

GOAL_PHASE1 = 78.0
GOAL_PHASE2 = 73.0
GOAL_FINAL = 70.0
BREAK1_START = dt.datetime(2026, 8, 12)
PHASE2_START = dt.datetime(2026, 9, 1)
BREAK2_START = dt.datetime(2026, 10, 17)
PHASE3_START = dt.datetime(2026, 11, 2)
# Первые дни после перерыва чувствительны к воде и гликогену.
# Это порог для отображения описательного тренда, не гарантия его точности.
MIN_TREND_POINTS = 7
MIN_TREND_SPAN_DAYS = 13  # 14 календарных дней включительно
# По просьбе пользователя тренд текущей фазы показывается раньше полного порога,
# но с пометкой «предварительно»: на коротком отрезке его сильно сдвигает вода.
MIN_PRELIM_POINTS = 5
MIN_PRELIM_SPAN_DAYS = 6


def phase_points(dates, weights, start=None, end=None):
    """Правая граница исключается: первый день перерыва уже вне фазы."""
    return [(day, weight) for day, weight in zip(dates, weights)
            if (start is None or day >= start) and (end is None or day < end)]


def fit(points):
    """МНК по реальным дням, а не порядковым номерам замеров."""
    xs = [(day - points[0][0]).days for day, _ in points]
    ws = [weight for _, weight in points]
    mx, my = sum(xs) / len(xs), sum(ws) / len(ws)
    denominator = sum((x - mx) ** 2 for x in xs)
    if not denominator:
        raise ValueError("Для тренда нужны замеры в разные дни")
    slope = sum((x - mx) * (w - my) for x, w in zip(xs, ws)) / denominator
    return slope, my - slope * mx


def trend_ready(points):
    return (len(points) >= MIN_TREND_POINTS
            and (points[-1][0] - points[0][0]).days >= MIN_TREND_SPAN_DAYS)


def prelim_ready(points):
    return (len(points) >= MIN_PRELIM_POINTS
            and (points[-1][0] - points[0][0]).days >= MIN_PRELIM_SPAN_DAYS)


def main():
    with CSV.open(encoding="utf-8") as source:
        rows = sorted((dt.datetime.strptime(row["date"], "%Y-%m-%d"),
                       float(row["weight"])) for row in csv.DictReader(source))
    dates, weights = zip(*rows)
    phases = [
        ("Фаза 1", phase_points(dates, weights, end=BREAK1_START), "#f59e0b", "-"),
        ("Фаза 2", phase_points(dates, weights, PHASE2_START, BREAK2_START), "#dc2626", "--"),
        ("Фаза 3", phase_points(dates, weights, PHASE3_START), "#7c3aed", "-."),
    ]

    plt.rcParams.update({"font.size": 11, "axes.edgecolor": "#cccccc", "axes.linewidth": 0.8})
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafafa")
    ax.plot(dates, weights, color="#2563eb", linewidth=2.0, marker="o",
            markersize=4, markerfacecolor="white", markeredgewidth=1.5,
            zorder=3, label="Вес")

    for i, (name, points, color, linestyle) in enumerate(phases):
        current = i == len(phases) - 1
        prelim = current and not trend_ready(points)
        if not (trend_ready(points) or (current and prelim_ready(points))):
            continue
        slope, intercept = fit(points)
        # Линия ограничена наблюдениями своей фазы; экстраполяции нет.
        endpoints = [points[0][0], points[-1][0]]
        trend = [intercept + slope * (day - endpoints[0]).days for day in endpoints]
        rate = f"{slope * 7:+.2f}".replace(".", ",")
        ax.plot(endpoints, trend, color=color, linestyle=linestyle, linewidth=2,
                zorder=4, label=f"{name}: тренд {rate} кг/нед" + (" (предварительно)" if prelim else ""))
        print(f"{name}: {len(points)} замеров, {endpoints[0]:%d.%m}–{endpoints[-1]:%d.%m}, {rate} кг/нед")

    # Перерывы видны на графике, но не участвуют в регрессиях дефицита.
    for start, end in [(BREAK1_START, PHASE2_START), (BREAK2_START, PHASE3_START)]:
        ax.axvspan(start, end, color="#d1d5db", alpha=0.35, zorder=0)
        ax.text(start + (end - start) / 2, 0.98, "Перерыв", transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=9, color="#4b5563")
    for label, start, end in [("Фаза 1", dates[0], BREAK1_START),
                              ("Фаза 2", PHASE2_START, BREAK2_START)]:
        ax.text(start + (end - start) / 2, 0.98, label, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=10, color="#374151")
    ax.axvline(PHASE2_START, color="#9ca3af", linestyle=":", linewidth=1, zorder=1)
    ax.axvline(PHASE3_START, color="#7c3aed", linestyle=":", linewidth=1.3, zorder=1)
    ax.annotate("Фаза 3\nс 02.11", (PHASE3_START, 79.5), xytext=(-8, 0),
                textcoords="offset points", ha="right", color="#6d28d9", fontsize=10)

    p3 = phases[-1][1]
    if p3:
        ax.scatter([day for day, _ in p3], [weight for _, weight in p3],
                   color="#7c3aed", marker="D", s=28, zorder=5, label="Замеры фазы 3")
    ax.annotate(f"{weights[-1]:.1f}".replace(".", ","), (dates[-1], weights[-1]),
                textcoords="offset points", xytext=(8, -18), ha="left",
                fontweight="bold", color="#1e3a8a")

    for goal, label, color in [(GOAL_PHASE1, "78 кг — прежний ориентир", "#6b7280"),
                               (GOAL_PHASE2, "73 кг — прежний ориентир", "#6b7280"),
                               (GOAL_FINAL, "70 кг — цель фазы 3", "#4d7c0f")]:
        ax.axhline(goal, color=color, linestyle="--", linewidth=1.1, alpha=0.8, zorder=1)
        ax.annotate(label, (dates[0], goal), textcoords="offset points",
                    xytext=(4, 5), color=color, fontsize=9)

    ax.set_title("Вес — фазы 1–3 · цель 70 кг", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylabel("кг")
    ax.set_ylim(min(GOAL_FINAL, min(weights)) - 0.8, max(weights) + 1.2)
    ax.set_yticks(range(int(min(GOAL_FINAL, min(weights))), int(max(weights)) + 2))
    ax.grid(True, axis="y", color="#e5e5e5", linewidth=0.8)
    # Календарные интервалы, первая и последняя даты всегда видны.
    ticks = [dates[0]]
    day = dates[0].replace(day=1) + dt.timedelta(days=32)
    day = day.replace(day=1)
    while day < dates[-1]:
        if (day - dates[0]).days >= 7 and (dates[-1] - day).days >= 7:
            ticks.append(day)
        day = (day + dt.timedelta(days=32)).replace(day=1)
    ticks.append(dates[-1])
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.margins(x=0.05)
    ax.legend(loc="upper right", bbox_to_anchor=(0.99, 0.90), fontsize=9, framealpha=0.95)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    if not trend_ready(p3):
        days = (p3[-1][0] - p3[0][0]).days + 1 if p3 else 0
        note = (f"Фаза 3: {len(p3)} замеров за {days} дн. — тренд предварительный, надёжным станет после ≥7 замеров за ≥14 дней.\n"
                "Тренды описывают вес; изменения воды и гликогена не отделены от изменений жировой массы.")
    else:
        note = "Тренды описывают вес; изменения воды и гликогена не отделены от изменений жировой массы."
    fig.text(0.08, 0.025, note, fontsize=9, color="#4b5563", va="bottom")
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"saved {OUT} ({len(weights)} точек)")


if __name__ == "__main__":
    main()
