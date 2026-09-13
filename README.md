# Pattern Studio

A static, interactive Python learning companion for NeetCode 150 and the Dynamic Programming section of Striver's A2Z curriculum. No API keys, paid models, backend, or npm dependencies are required.

## Use locally

Run `npm start`, then open http://127.0.0.1:4173. You can also serve `dist/` with any static HTTP server. Keep the same browser and origin to retain your learning state.

## Included

- All 150 NeetCode problems across 18 categories, with 510 example-verified Python approaches, detailed intuition, algorithm steps, complexity, pitfalls, and recognition cues.
- 26 conceptual topic guides explain definitions, mental models, correctness invariants, tradeoffs, memory hooks, and common mistakes.
- NeetCode visual labs contain 14,851 recorded Python execution steps with line highlighting, live variables, call stacks, arrays, pointers, grids, graphs, trees, linked nodes, intervals, and bits. Play, pause, scrub, step, change speed, or expand the lab.
- 300 NeetCode flashcards alongside the 112 DP flashcards below.

- 56 learning units covering 55 DP problems, with an additional matrix-chain tabulation workshop.
- 8 categories: 1D, grids, subsequences, strings, stocks, LIS, partition DP, and rectangles.
- Original paraphrased statements, intuition, recurrence, boundaries, Python recursion/memoization/tabulation/optimized approaches, complexity, and pattern notes.
- 772 computed states across interactive memoization dry runs, with dependency highlighting, state tables, playback, stepping, speed controls, and a scrubber.
- 112 active-recall flashcards with practice/remembered ratings.
- Personal notes, progress, bookmarks, and review ratings in browser localStorage. JSON backup export/import merges data and keeps existing local notes.
- Responsive layout, keyboard controls, focus indicators, reduced-motion support, escaped user content, and a progressive WebMCP navigation tool.

The code is presented for reading and copying; the browser does not execute arbitrary Python. Walkthroughs use verified, precomputed examples. Recursion is educational; prefer iterative code on large inputs. For problems where ordinary rolling-space reduction is invalid, the optimized tab explains the limitation and retains the necessary table.

## Content maintenance and checks

With Python 3.9+ available:

```
python build_curriculum.py
python validate_curriculum.py
npm run check
```

`build_curriculum.py` authors and validates all four Python versions and produces the committed `dist/curriculum.js`. `validate_curriculum.py` runs 2,912 executions with deterministic randomized and boundary cases, plus independent brute-force checks for selected objectives. Rebuild the data after modifying content.

## Sources and conventions

Curriculum organization: https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z and https://takeuforward.org/dynamic-programming/striver-dp-series-dynamic-programming-problems. Checked September 11, 2026. The current published sheet lists 55 DP problems. The historic DP lecture numbering has 56 units because matrix-chain tabulation is a separate workshop.

This is an independent companion, not affiliated with takeUforward. Explanations and code are original. Each statement declares conventions that vary between judges (such as numeric obstacle markers, exact counts instead of a modulus, and whether monotone bitonic subsequences qualify).

Google Fonts are optional; system fonts provide an offline fallback. Notes are never sent to a server. Localhost and the deployed site have separate browser storage; export/import transfers progress between them. Clearing site data removes local notes unless backed up.

## NeetCode content and validation

Approach explanations and Python implementations are adapted from the MIT-licensed neetcode-gh/leetcode repository, pinned to commit `9f104d45b1efc8c2e42b6dcc7b1216cdf8c4f80e`. The full license is distributed in `dist/licenses/neetcode.txt`, and every lesson links to its source. Problem paraphrases, topic guides, and visualizations were authored for this project.

Run `python build_neetcode.py --build` to validate the 510 approach examples and regenerate the data from the cached licensed articles. `npm run check` checks JavaScript syntax and renders all 1,030 lesson sections and 15,623 animation states in an isolated test environment. Example validation is not an exhaustive proof for arbitrary inputs.

Visual labs replay the recommended implementation on the included example; they do not run user-supplied Python. Node and interval problems use the practice platform’s supplied data classes. Some diagrams summarize the input while the live-variable panel shows the execution state. Large objects are compacted for readability.
