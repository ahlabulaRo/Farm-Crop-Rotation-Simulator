# Farm & Crop Rotation Simulator (C++ OOP & Dynamic Programming)

An Object-Oriented Programming simulation engine built in **C++**. The application models a grid-based agricultural farm and maximizes net profit over a fixed number of days using **Depth-First Search with Dynamic Programming** while strictly enforcing crop-rotation and budget constraints.

---

## How to Build & Run

The project includes a `Makefile` with an integrated Python verification suite (`test1` through `test18`) that compiles the source files, runs the simulation, and validates outputs against reference test cases.

* **Compile and run all 18 automated tests (default target):**
```bash
make
```
*(or `make test-all`)*

* **Compile the executable (`ferma`) only:**
```bash
make build
```

* **Run the simulation on the default input (`ferma.txt` -> `ferma.out`):**
```bash
make run
```

* **Run and verify a single test case (e.g., `test1` through `test18`):**
```bash
make test1
```

* **Run manually on custom input/output files:**
```bash
./ferma <input_file> <output_file>
```

* **Clean build artifacts (`.o`), executable (`ferma`), and output files:**
```bash
make clean
```

---

## Architecture & Class Design

The codebase is modularized into three core classes following strict OOP principles and the **Rule of Three**:

* **`Leguma` (Crop):** Encapsulates crop properties—dynamically allocated name (`char*`), growth duration (`timpCultivare`), planting cost (`costPlantare`), and selling price (`pretVanzare`).
* **`Patrat` (Plot / Grid Cell):** Tracks the state of an individual farm plot, including the currently planted crop, the previously harvested crop, planting/harvesting timestamps, and availability status.
* **`Ferma` (Farm Controller):** Manages the `N x N` grid of plots, budget, crop compatibility matrix, action history log, and the optimization simulation loop.

---

## Optimization & Simulation Logic

1. **Crop Rotation & Cooldown Rules:**
   * Uses an adjacency/compatibility matrix (`permisiuni`) parsed from the input file to determine valid crop sequences on each plot.
   * Enforces distinct cooldown periods before replanting: a **4-day rest period (`SAME`)** when replanting the same crop species and a **1-day rest period (`FRIENDLY`)** when rotating to a compatible species.
2. **Profit Maximization via DFS + Memoization (`dfsPatrat`):**
   * Evaluates future planting and harvesting sequences per plot using a 3D memoization table (`dp[day][last_crop][is_free]`).
   * At each simulation step (day), the engine harvests all mature crops, updates the available budget, and selects the optimal crop to plant on each free plot based on immediate net profit plus projected future DP yield.
3. **Action Logging & Reporting:**
   * Records every `planteaza` (plant) and `culege` (harvest) action with exact day and grid coordinates (`00x00` format), outputting the chronological log alongside the final balance (`SUMA_FINALA`).

---

## Technologies & Concepts Applied
* **Language:** C++ (C++11 standard, compiled with `-Wall -Wextra`)
* **Build & Testing:** GNU Make, Python 3 test verification suite
* **OOP Concepts:** Encapsulation, Rule of Three, Modular Header/Source Separation
* **Algorithms:** Depth-First Search (DFS), Dynamic Programming (3D Memoization), Graph/Adjacency Matrix Modeling
* **Memory Management:** Manual heap allocation (`new` / `delete[]`) for 1D/2D dynamic arrays and C-strings with zero memory leaks
