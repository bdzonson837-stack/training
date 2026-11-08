# Учебный план: GPU / Parallel Computing / LLM / Математика

> Составлен: 13 июня 2026. Горизонт: ~4 месяца (до середины октября 2026).

## Цели

1. **PMPP** — книга "Programming Massively Parallel Processors" (4-е изд., CUDA)
2. **CS149** — Stanford Parallel Computing
3. **CS336** — Stanford Language Modeling from Scratch
4. **MathAcademy** — Calculus 2 → Mathematics for Machine Learning

## Стартовая точка (на 13.06.2026)

- MathAcademy: Calculus 1 пройден, Calculus 2 в процессе
- CS149: лекции 1–6 просмотрены, assignment 1 завершён
- PMPP: главы 1–4 прочитаны
- CS336: лекции 1–2 просмотрены, assignment 1 частично (остановился на LR scheduler)

## Главный принцип

**Не 4 параллельных трека, а 2 + фон:**

- Математика — ежедневный фон (45–60 XP ≈ 45–60 мин), не конкурирует за глубокую концентрацию
- PMPP + CS149 — **один** GPU-трек (книга = теория, курс = задания), проходятся синхронно
- CS336 — следующий трек после GPU-трека (CS149 — фактический пререквизит для assignment 2 на Triton)

**Правило одного тяжёлого дела в день:** в глубокой работе только один assignment. Лекции и книга — лёгкая нагрузка, совместимы с чем угодно.

---

> CS336 полностью отложен до Фазы 2 (решение от 13.06.2026) — сначала GPU-фундамент.

## Фаза 1 — сейчас, недели 1–7 (≈ середина июня → начало августа): GPU-трек

**CS149:**
- [ ] Лекции 7–18 (темп: 2–3 в неделю)
- [ ] Assignment 2 — task graph scheduling / thread pool (~15–20 ч)
- [ ] Assignment 3 — CUDA circle renderer (~20–30 ч, самое тяжёлое)
- [ ] Assignment 5 — оптимизация CUDA-ядер (~15–25 ч)
- Assignment 4 (Trainium2) — пропустить или взять версию Fall 2023/24

**PMPP** (темп: 2 главы в неделю, синхронно с GPU-лекциями CS149, ядра писать руками):
- [ ] Главы 5–6 (память, performance) — ядро Части I
- [ ] Главы 7–12 (convolution, stencil, histogram, reduction, scan, merge)
- Видео-сопровождение: лекции Izzat El Hajj (соавтор книги, YouTube)

**MathAcademy:**
- [ ] Добить Calculus 2 при 45–60 XP/день

## Фаза 2 — недели 8–16 (≈ август → начало октября): CS336

**CS336:**
- [ ] Дозакрыть Assignment 1 (точка остановки — cosine LR scheduler с warmup; перед продолжением освежить свой код tokenizer/transformer)
- [ ] Лекции 3–19 (все на YouTube)
- [ ] Assignment 2 — FlashAttention-2 на Triton, DDP, optimizer sharding (~40–50 ч)
- [ ] Assignment 3 — scaling laws (частично: без стэнфордского API, ~10 ч)
- [ ] Assignment 4 — data pipeline: Common Crawl, дедупликация, фильтры (~20–25 ч)
- [ ] Assignment 5 — alignment: SFT, GRPO, опционально DPO (~30–40 ч)

**MathAcademy:**
- [ ] Mathematics for Machine Learning (~70 ч ≈ вся фаза при 50 XP/день)

**PMPP (точечно):**
- [ ] Глава 14 (sparse matrix), глава 16 (deep learning), глава 20 (streams)
- [ ] Лекции GPU MODE про Triton / FlashAttention — мост к assignment 2

---

## Шаблон дня

| Время | Что |
|---|---|
| Утро, ~1 ч | MathAcademy, 45–60 XP (первым делом, на свежую голову) |
| Блок 1, 3–4 ч | Глубокая работа: текущий assignment |
| Перерыв | Обед / прогулка, реальный отдых |
| Блок 2, 2–3 ч | Лекции + чтение PMPP |
| 21:00–22:30 пн–чт | Английский язык (фиксировано) |

Итого ~6–7 ч учёбы в день. Пятница-вечер + один полный выходной — свободны (защита от выгорания, критично перед CS336).

## Практические заметки

- **GPU:** основная машина — Mac. Для CS149 asst3/asst5 и CS336 asst2 нужна NVIDIA-карта → аренда Vast.ai / Lambda / Lightning AI (RTX 4090 почасово; для DDP-части asst2 — 2 GPU на несколько часов). Бюджет ~$30–60 на весь план.
- **MathAcademy:** >60 XP/день — путь к выгоранию, не форсировать.
- **CS336:** лекции не пропускать — в них исследовательский контекст, которого нет в раздатках.
- **Сообщество:** GPU MODE Discord (бывш. CUDA MODE) — reading group по PMPP, kernel leaderboard, лекции после книги.

## Оценки трудозатрат (из исследования 06.2026)

| Курс | Объём | Источник оценки |
|---|---|---|
| CS149 | ~150 ч | csdiy.wiki |
| CS336 | ~190–250 ч | официальная оценка 20–25 ч/нед × 10 нед; обзор Andy Timm ~190 ч |
| PMPP (ядро: гл. 1–12, 14, 16, 20) | ~60–100 ч | 4–8 ч/глава с упражнениями |
| Calculus 2 (остаток) + Math for ML | ~100–130 ч | 1 XP ≈ 1 мин; Math for ML ≈ 5000 XP |

## Ссылки

- CS149 Fall 2025: https://gfxcourses.stanford.edu/cs149/fall25 (лекции Fall 2023 на YouTube, код: github.com/stanford-cs149)
- CS336 Spring 2025: https://cs336.stanford.edu/spring2025 (код: github.com/stanford-cs336)
- Лекции El Hajj по PMPP: https://ielhajj.github.io/
- GPU MODE: https://github.com/gpu-mode/lectures + discord.gg/gpumode
- Решения упражнений PMPP: https://github.com/tugot17/pmpp
- Math for ML: https://www.mathacademy.com/courses/mathematics-for-machine-learning
- Обзор CS336: https://andytimm.github.io/posts/cs336/cs336_review.html
