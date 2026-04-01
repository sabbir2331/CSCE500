"""
Unit tests for closest_pair.py
Run with: python -m pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from closest_pair import find_closest_pair, manhattan


# ── helpers ──────────────────────────────────────────────────────────────────

def brute_force(points):
    """Exhaustive O(n²) reference answer."""
    n = len(points)
    best_d = float('inf')
    best_pair = (-1, -1)
    for i in range(n):
        for j in range(i + 1, n):
            d = manhattan(points[i][0], points[i][1], points[j][0], points[j][1])
            if d < best_d:
                best_d = d
                best_pair = (i + 1, j + 1)
    return best_d, best_pair[0], best_pair[1]


# ── basic tests ───────────────────────────────────────────────────────────────

def test_example_from_pdf():
    points = [(0,0),(1,2),(5,5),(-2,-3),(4,6),(7,8),(9,2)]
    d, a, b = find_closest_pair(points)
    assert d == 2
    assert {a, b} == {3, 5}


def test_two_points():
    d, a, b = find_closest_pair([(0,0),(3,4)])
    assert d == 7
    assert {a, b} == {1, 2}


def test_single_point():
    d, a, b = find_closest_pair([(5, 5)])
    assert d == 0


def test_coincident_points():
    d, _, _ = find_closest_pair([(1,1),(1,1),(2,2)])
    assert d == 0


def test_negative_coords():
    d, a, b = find_closest_pair([(-10**9, -10**9), (-10**9 + 1, -10**9)])
    assert d == 1


def test_large_coords():
    d, a, b = find_closest_pair([(10**9, 10**9), (10**9 - 1, 10**9)])
    assert d == 1


def test_horizontal_line():
    points = [(i, 0) for i in range(10)]
    d, a, b = find_closest_pair(points)
    assert d == 1


def test_vertical_line():
    points = [(0, i) for i in range(10)]
    d, a, b = find_closest_pair(points)
    assert d == 1


# ── random stress tests ───────────────────────────────────────────────────────

import random

def test_stress_small():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(2, 20)
        pts = [(rng.randint(-100, 100), rng.randint(-100, 100)) for _ in range(n)]
        expected_d, *_ = brute_force(pts)
        got_d, ga, gb = find_closest_pair(pts)
        assert got_d == expected_d, f"Failed on {pts}: expected {expected_d}, got {got_d}"
        # verify the returned pair actually achieves the claimed distance
        ox, oy = pts[ga - 1]
        qx, qy = pts[gb - 1]
        assert manhattan(ox, oy, qx, qy) == got_d


def test_stress_medium():
    rng = random.Random(42)
    for _ in range(20):
        n = rng.randint(100, 500)
        pts = [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(n)]
        expected_d, *_ = brute_force(pts)
        got_d, ga, gb = find_closest_pair(pts)
        assert got_d == expected_d


# ── performance smoke test ────────────────────────────────────────────────────

def test_large_n_terminates():
    """Ensure n=10^5 finishes quickly (< 5 s in pytest)."""
    import time
    rng = random.Random(7)
    n = 100_000
    pts = [(rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)) for _ in range(n)]
    t0 = time.time()
    find_closest_pair(pts)
    elapsed = time.time() - t0
    assert elapsed < 5.0, f"Took {elapsed:.2f}s for n={n}"
