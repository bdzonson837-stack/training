"""График калорий по дням из сводной таблицы health/журнал-еды.md.

Столбцы — калории за день, линия — среднее за 7 дней.
Запуск: python3 health/plot_calories.py
"""
import datetime as dt
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
LOG = HERE / "журнал-еды.md"
OUT = HERE / "calories.png"
YEAR = 2026

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT2 = "#52514e"
GRID = "#e4e3df"
BAR = "#2a78d6"      # категориальный слот 1
AVG = "#eb6834"      # категориальный слот 2
BREAK_FILL = "#ecebe7"

MAINTENANCE = 2700
PHASES = [  # (начало, конец, подпись, перерыв?)
    (dt.date(2026, 6, 12), dt.date(2026, 8, 11), "фаза 1", False),
    (dt.date(2026, 8, 12), dt.date(2026, 8, 31), "перерыв", True),
    (dt.date(2026, 9, 1), dt.date(2026, 10, 16), "фаза 2", False),
    (dt.date(2026, 10, 17), None, "перерыв", True),
]

ROW = re.compile(r"^\| (\d\d)\.(\d\d) \([^)]*\) \|.*\| ~?(\d+)\s*\|[^|]*\|$", re.M)


def load():
    text = LOG.read_text(encoding="utf-8")
    days = {}
    for d, m, kcal in ROW.findall(text):
        days[dt.date(YEAR, int(m), int(d))] = int(kcal)
    return sorted(days.items())


def rolling(days, window=7):
    out = []
    for i, (d, _) in enumerate(days):
        vals = [k for dd, k in days if d - dt.timedelta(days=window - 1) <= dd <= d]
        if len(vals) >= 4:
            out.append((d, sum(vals) / len(vals)))
    return out


def main():
    days = load()
    if not days:
        raise SystemExit("нет данных")
    last = days[-1][0]
    avg = rolling(days)

    fig, ax = plt.subplots(figsize=(11, 5.6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for start, end, label, is_break in PHASES:
        end = end or last
        if is_break:
            ax.axvspan(start - dt.timedelta(hours=12), end + dt.timedelta(hours=12),
                       color=BREAK_FILL, zorder=0, lw=0)
        mid = start + (end - start) / 2
        ax.text(mid, 1.01, label, transform=ax.get_xaxis_transform(),
                ha="center", va="bottom", fontsize=9, color=TEXT2)
        vals = [k for d, k in days if start <= d <= end]
        if vals and not is_break:
            ax.text(mid, 0.95, f"в среднем {round(sum(vals) / len(vals)):,}".replace(",", " "),
                    transform=ax.get_xaxis_transform(), ha="center", va="top",
                    fontsize=9, color=TEXT)

    ax.bar([d for d, _ in days], [k for _, k in days], width=0.75,
           color=BAR, alpha=0.55, zorder=2, label="ккал за день")
    # линию рвём на пропусках в журнале (больше 3 дней без записей)
    segs, cur = [], []
    for d, v in avg:
        if cur and (d - cur[-1][0]).days > 3:
            segs.append(cur)
            cur = []
        cur.append((d, v))
    segs.append(cur)
    for i, seg in enumerate(segs):
        ax.plot([d for d, _ in seg], [v for _, v in seg], color=AVG, lw=2,
                zorder=3, label="среднее за 7 дней" if i == 0 else None)

    ax.axhline(MAINTENANCE, color=TEXT2, lw=1, ls="--", zorder=1)
    ax.text(days[0][0], MAINTENANCE + 40, f"поддержание ~{MAINTENANCE}",
            fontsize=8.5, color=TEXT2, va="bottom")

    ax.set_ylim(0, max(k for _, k in days) * 1.12)
    ax.set_ylabel("ккал", color=TEXT2)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.tick_params(colors=TEXT2, labelsize=9)
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)

    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88), frameon=False,
              fontsize=9, labelcolor=TEXT)
    ax.set_title(f"Калории по дням (12.06 — {last:%d.%m}, {len(days)} дней)",
                 color=TEXT, fontsize=13, fontweight="bold", pad=22)

    fig.tight_layout()
    fig.savefig(OUT, facecolor=SURFACE)
    print(f"saved {OUT} ({len(days)} дней)")


if __name__ == "__main__":
    main()
