# Closest Pair of Points — Manhattan Distance

**CSCE 500 – Design & Analysis of Algorithms, Spring 2026**  
University of Louisiana at Lafayette
Author: Sabbir Rahman

---

## Problem Statement

Given *n* integer-valued points in a 2-D plane, find the pair of points with the **minimum Manhattan distance**:

$$d_{\text{Manhattan}}(P, Q) = |x_P - x_Q| + |y_P - y_Q|$$

### Constraints
| Parameter | Bound |
|-----------|-------|
| n | 1 ≤ n ≤ 10⁶ |
| coordinates | −10⁹ ≤ x, y ≤ 10⁹ |
| time limit | 10 seconds |

---

## Algorithm

### Primary: O(n log n) Sweep Line via Chebyshev Transform

**Key Insight**: Rotating the coordinate axes by 45° converts Manhattan distance into Chebyshev distance.

Let:
```
u = x + y
v = x - y
```

Then:
```
Manhattan(P, Q) = |xP - xQ| + |yP - yQ|
               = max(|uP - uQ|, |vP - vQ|)   (Chebyshev distance)
```

**Algorithm:**
1. Transform all points: `(x, y) → (u, v) = (x+y, x-y)` — O(n)
2. Sort by `u` — O(n log n)
3. Sweep right: for each new point R, maintain a `SortedList` of active points (those with `|u - uR| < δ`). Query the v-window `[vR−δ, vR+δ]` with `bisect` — O(log n) per point.
4. Update `δ` whenever a closer pair is found.

**Total: O(n log n)**

### Fallback: O(n log² n) Divide & Conquer

Classic D&C closest-pair adapted for Manhattan distance:
1. Sort by x — O(n log n)
2. Divide at median x — T(n) = 2T(n/2) + O(n log n)
3. Merge: collect strip of width `δ`, sort by y, compare each point against O(1) neighbours.

---

## Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Sweep Line (Chebyshev) | O(n log n) | O(n) |
| Divide & Conquer | O(n log² n) | O(n) |
| Brute Force (reference) | O(n²) | O(1) |

---

## Input / Output Format

**Input:**
```
n
x1 y1
x2 y2
...
xn yn
```

**Output:**
```
<minimum Manhattan distance>
<index_i> <index_j>
```
Points are 1-indexed. If multiple pairs achieve the minimum, any one is acceptable.

**Example:**
```
Input:          Output:
7               2
0 0             3 5
1 2
5 5
-2 -3
4 6
7 8
9 2
```
Points 3 `(5,5)` and 5 `(4,6)`: |5−4| + |5−6| = 1 + 1 = **2** ✓

---

## Running the Code

### Prerequisites
```bash
pip install sortedcontainers
```

### Run
```bash
python closest_pair.py < input.txt
```

### Run Tests
```bash
pip install pytest
python -m pytest tests/ -v
```

---

## File Structure

```
.
├── closest_pair.py        # Main solution (primary + fallback algorithms)
├── tests/
│   └── test_closest_pair.py   # Unit + stress + performance tests
├── requirements.txt
└── README.md
```

---

## Performance

| n | Time (Python) |
|---|---------------|
| 10,000 | < 0.1 s |
| 100,000 | < 0.3 s |
| 500,000 | ≈ 2.4 s |
| 1,000,000 | ≈ 5 s (est.) |

All within the 10-second limit.

---

## References

- Cormen, T. H., et al. *Introduction to Algorithms*, 4th ed. MIT Press, 2022.
- Preparata, F. P. & Shamos, M. I. *Computational Geometry: An Introduction*. Springer, 1985.
- [SortedContainers documentation](http://www.grantjenks.com/docs/sortedcontainers/)
