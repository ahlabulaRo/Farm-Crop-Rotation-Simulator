# Farm & Crop Rotation Simulator (C++ OOP & Dynamic Programming)

An Object-Oriented Programming (OOP) simulation engine built in **C++**, developed for the OOP course at the Faculty of Automatic Control and Computer Science (POLITEHNICA Bucharest). The application models a grid-based agricultural farm and maximizes net profit over a fixed number of days using **Depth-First Search (DFS) with Dynamic Programming (memoization)** while strictly enforcing crop-rotation and budget constraints.

---

## How to Build & Run

### Compilation

Compile the project using `g++` (or via the included `Makefile` if available):

```bash
g++ -std=c++11 -Wall -Wextra main.cpp ferma.cpp patrat.cpp leguma.cpp -o farm_sim
```

### Execution

The program accepts two command-line arguments: the input configuration file and the output log file:

```bash
./farm_sim <input_file> <output_file>
```

_Example:_

```bash
./farm_sim input.txt output.txt
```

---

## Architecture & Class Design

The codebase is modularized into three core classes following strict OOP principles and the **Rule of Three** (custom copy constructors, copy assignment operators, and destructors for manual dynamic memory management):

- **`Leguma` (Crop):** Encapsulates crop properties—dynamically allocated name (`char*`), growth duration (`timpCultivare`), planting cost (`costPlantare`), and selling price (`pretVanzare`).
- **`Patrat` (Plot / Grid Cell):** Tracks the state of an individual farm plot, including the currently planted crop, the previously harvested crop, planting/harvesting timestamps, and availability status.
- **`Ferma` (Farm Controller):** Manages the `N x N` grid of plots, budget, crop compatibility matrix, action history log, and the optimization simulation loop.

---

## Optimization & Simulation Logic

1. **Crop Rotation & Cooldown Rules:**
   - Uses an adjacency/compatibility matrix (`permisiuni`) parsed from the input file to determine valid crop sequences on each plot.
   - Enforces distinct cooldown periods before replanting: a **4-day rest period (`SAME`)** when replanting the same crop species and a **1-day rest period (`FRIENDLY`)** when rotating to a compatible species.
2. **Profit Maximization via DFS + Memoization (`dfsPatrat`):**
   - Evaluates future planting and harvesting sequences per plot using a 3D memoization table (`dp[day][last_crop][is_free]`).
   - At each simulation step (day), the engine harvests all mature crops, updates the available budget, and selects the optimal crop to plant on each free plot based on immediate net profit plus projected future DP yield.
3. **Action Logging & Reporting:**
   - Records every `planteaza` (plant) and `culege` (harvest) action with exact day and grid coordinates (`00x00` format), outputting the chronological log alongside the final balance (`SUMA_FINALA`).

---

## Technologies & Concepts Applied

- **Language:** C++ (C++11)
- **OOP Concepts:** Encapsulation, Rule of Three, Modular Header/Source Separation
- **Algorithms:** Depth-First Search (DFS), Dynamic Programming (3D Memoization), Graph/Adjacency Matrix Modeling
- **Memory Management:** Manual heap allocation (`new` / `delete[]`) for 1D/2D dynamic arrays and C-strings with zero memory leaks
