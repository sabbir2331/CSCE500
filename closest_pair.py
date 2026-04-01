"""
CSCE 500 – Algorithm Design & Analysis – Spring 2026
Project 3: Closest Pair of Points (Manhattan Distance)

Algorithm : O(n log n) Sweep Line via Chebyshev Transform
            + O(n log² n) Divide & Conquer fallback

Author    : Sabbir Rahman  (Louisiana State University)
"""

import sys
from sortedcontainers import SortedList


# ─────────────────────────────────────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────────────────────────────────────

def manhattan(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 1 – O(n log n) Sweep Line  (PRIMARY)
#
# Key insight : rotate axes 45°
#     u = x + y,   v = x - y
# Then  Manhattan(P, Q) == max(|u_P − u_Q|, |v_P − v_Q|)
#                       == Chebyshev distance in (u,v) space
#
# Proof sketch:
#   max(|Δu|, |Δv|) = max(|(Δx+Δy)|, |(Δx−Δy)|) = |Δx| + |Δy|
#
# Sweep on u: maintain a SortedList of active points keyed by v.
# For each new point R, candidates lie in u-window [u_R−δ, u_R] and
# v-window [v_R−δ, v_R+δ].  Bisect finds them in O(log n).
# ─────────────────────────────────────────────────────────────────────────────

def solve_sweep(points):
    """
    O(n log n) sweep-line closest pair under Manhattan distance.

    Parameters
    ----------
    points : list of (x, y) — 0-indexed

    Returns
    -------
    (dist, i, j)  — 1-based indices, i < j
    """
    n = len(points)
    if n == 1:
        return (0, 1, 1)

    # Build (u, v, 1-based-idx) and sort by u
    transformed = sorted(
        ((x + y, x - y, i + 1) for i, (x, y) in enumerate(points)),
        key=lambda t: t[0]
    )

    INF = float('inf')
    best_d = INF
    best_i, best_j = -1, -1

    # SortedList of (v, 1-based-index), sorted by v for range queries
    active = SortedList(key=lambda t: t[0])
    left = 0

    for right in range(n):
        u_r, v_r, idx_r = transformed[right]

        # Evict points whose u-distance from current point >= delta
        while left < right and (u_r - transformed[left][0]) >= best_d:
            _, v_l, idx_l = transformed[left]
            active.remove((v_l, idx_l))
            left += 1

        # Binary-search for v-window candidates
        lo_v = v_r - best_d + 1 if best_d < INF else -10**18
        hi_v = v_r + best_d - 1 if best_d < INF else  10**18

        lo_pos = active.bisect_left((lo_v, -10**18))
        hi_pos = active.bisect_right((hi_v,  10**18))

        for k in range(lo_pos, hi_pos):
            v_k, idx_k = active[k]
            ox, oy = points[idx_k - 1]
            rx, ry = points[idx_r - 1]
            d = manhattan(ox, oy, rx, ry)
            if d < best_d:
                best_d = d
                a, b = idx_k, idx_r
                if a > b:
                    a, b = b, a
                best_i, best_j = a, b

        active.add((v_r, idx_r))

    return (int(best_d), best_i, best_j)


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 2 – O(n log² n) Divide & Conquer  (FALLBACK / COMPARISON)
# ─────────────────────────────────────────────────────────────────────────────

def _brute(pts, lo, hi):
    best = (float('inf'), -1, -1)
    for i in range(lo, hi + 1):
        for j in range(i + 1, hi + 1):
            d = manhattan(pts[i][0], pts[i][1], pts[j][0], pts[j][1])
            a, b = pts[i][2], pts[j][2]
            if a > b:
                a, b = b, a
            if d < best[0]:
                best = (d, a, b)
    return best


def _dnc(pts_x, lo, hi):
    if hi - lo + 1 <= 3:
        return _brute(pts_x, lo, hi)

    mid = (lo + hi) // 2
    mid_x = pts_x[mid][0]

    lb = _dnc(pts_x, lo, mid)
    rb = _dnc(pts_x, mid + 1, hi)
    best = lb if lb[0] <= rb[0] else rb
    delta = best[0]

    strip = sorted(
        [pts_x[i] for i in range(lo, hi + 1)
         if abs(pts_x[i][0] - mid_x) < delta],
        key=lambda p: p[1]
    )

    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < delta:
            d = manhattan(strip[i][0], strip[i][1], strip[j][0], strip[j][1])
            if d < delta:
                delta = d
                a, b = strip[i][2], strip[j][2]
                if a > b:
                    a, b = b, a
                best = (d, a, b)
            j += 1

    return best


def solve_dnc(points):
    """O(n log² n) divide-and-conquer."""
    n = len(points)
    if n == 1:
        return (0, 1, 1)
    indexed = [(x, y, i + 1) for i, (x, y) in enumerate(points)]
    pts_x = sorted(indexed, key=lambda p: (p[0], p[1]))
    return _dnc(pts_x, 0, n - 1)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def find_closest_pair(points):
    """
    Find the closest pair of points under Manhattan distance.

    Parameters
    ----------
    points : list of (x, y) — 0-indexed

    Returns
    -------
    (distance, i, j)  where i, j are 1-based indices with i < j
    """
    return solve_sweep(points)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point (fast I/O for n up to 10^6)
# ─────────────────────────────────────────────────────────────────────────────

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    points = []
    for _ in range(n):
        x = int(data[pos]); pos += 1
        y = int(data[pos]); pos += 1
        points.append((x, y))

    dist, a, b = find_closest_pair(points)
    sys.stdout.write(f"{dist}\n{a} {b}\n")


if __name__ == "__main__":
    main()
