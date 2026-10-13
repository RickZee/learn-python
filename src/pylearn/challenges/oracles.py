"""Slow-by-construction oracles for challenge cross-checks.

One block per problem, in problem order. Oracles try every option; they must not
match a reference solution's normalized AST.
"""

from __future__ import annotations

import copy
import random
from collections.abc import Iterator

from pylearn.challenges import OpsOracle, Oracle, register, register_ops


def slow_edit_distance(a: str, b: str) -> int:
    """Try all three edits at every mismatch. Exponential on purpose."""
    if not a or not b:
        return len(a) + len(b)
    if a[0] == b[0]:
        return slow_edit_distance(a[1:], b[1:])
    return (
        1
        + min(
            slow_edit_distance(a[1:], b),  # delete
            slow_edit_distance(a, b[1:]),  # insert
            slow_edit_distance(a[1:], b[1:]),  # replace
        )
    )


def _edit_distance_cases(rng: random.Random) -> Iterator[tuple[str, str]]:
    while True:
        yield (
            "".join(rng.choice("abc") for _ in range(rng.randint(0, 5))),
            "".join(rng.choice("abc") for _ in range(rng.randint(0, 5))),
        )


register("57-edit-distance", Oracle(slow_edit_distance, _edit_distance_cases))


def _same_groups(got, want) -> bool:
    """Compare lists of groups without caring about group order or order inside."""

    def norm(groups):
        return sorted(tuple(sorted(g)) for g in groups)

    return norm(got) == norm(want)


def slow_group_anagrams(words: list[str]) -> list[list[str]]:
    """Pair each word with every other by sorting both; O(n² · k log k)."""
    groups: list[list[str]] = []
    used = [False] * len(words)
    for i, word in enumerate(words):
        if used[i]:
            continue
        bucket = [word]
        used[i] = True
        key = sorted(word)
        for j in range(i + 1, len(words)):
            if not used[j] and sorted(words[j]) == key:
                bucket.append(words[j])
                used[j] = True
        groups.append(bucket)
    return groups


def _group_anagrams_cases(rng: random.Random) -> Iterator[tuple[list[str],]]:
    alphabet = "ab"
    while True:
        n = rng.randint(0, 5)
        yield (["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 3))) for _ in range(n)],)


register(
    "02-group-anagrams",
    Oracle(slow_group_anagrams, _group_anagrams_cases, same=_same_groups),
)


def slow_longest_substring(s: str) -> int:
    """Every start index, grow until a repeat; O(n²)."""
    best = 0
    for i in range(len(s)):
        seen: set[str] = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best


def _longest_substring_cases(rng: random.Random) -> Iterator[tuple[str,]]:
    while True:
        yield ("".join(rng.choice("abc") for _ in range(rng.randint(0, 8))),)


register(
    "03-longest-substring-without-repeating-characters",
    Oracle(slow_longest_substring, _longest_substring_cases),
)


def slow_three_sum(nums: list[int]) -> list[list[int]]:
    """Three nested loops; O(n³)."""
    found: set[tuple[int, int, int]] = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in found]


def _three_sum_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(-3, 3) for _ in range(rng.randint(0, 6))],)


register("04-3sum", Oracle(slow_three_sum, _three_sum_cases, same=_same_groups))


def slow_max_area(height: list[int]) -> int:
    """Every pair of lines; O(n²)."""
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best


def _max_area_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 8) for _ in range(rng.randint(0, 7))],)


register("05-container-with-most-water", Oracle(slow_max_area, _max_area_cases))


def slow_product_except_self(nums: list[int]) -> list[int]:
    """Multiply every other index for each i; O(n²)."""
    n = len(nums)
    out = []
    for i in range(n):
        product = 1
        for j in range(n):
            if i != j:
                product *= nums[j]
        out.append(product)
    return out


def _product_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(-3, 3) for _ in range(rng.randint(0, 5))],)


register("06-product-of-array-except-self", Oracle(slow_product_except_self, _product_cases))


def slow_merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Repeatedly merge any overlapping pair until stable."""
    if not intervals:
        return []
    spans = [list(span) for span in intervals]
    changed = True
    while changed:
        changed = False
        merged: list[list[int]] = []
        used = [False] * len(spans)
        for i, a in enumerate(spans):
            if used[i]:
                continue
            cur = list(a)
            used[i] = True
            for j, b in enumerate(spans):
                if used[j]:
                    continue
                if not (cur[1] < b[0] or b[1] < cur[0]):
                    cur = [min(cur[0], b[0]), max(cur[1], b[1])]
                    used[j] = True
                    changed = True
            merged.append(cur)
        spans = merged
    return sorted(spans, key=lambda s: s[0])


def _merge_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        n = rng.randint(0, 4)
        spans = []
        for _ in range(n):
            a = rng.randint(0, 6)
            b = a + rng.randint(0, 4)
            spans.append([a, b])
        yield (spans,)


register("07-merge-intervals", Oracle(slow_merge_intervals, _merge_cases))


def slow_is_valid(s: str) -> bool:
    """Strip matched pairs until stuck; O(n²) string rebuilds."""
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


def _valid_cases(rng: random.Random) -> Iterator[tuple[str,]]:
    chars = "()[]{}"
    while True:
        yield ("".join(rng.choice(chars) for _ in range(rng.randint(0, 8))),)


register("08-valid-parentheses", Oracle(slow_is_valid, _valid_cases))


def slow_binary_search(nums: list[int], target: int) -> int:
    """Linear scan."""
    for i, value in enumerate(nums):
        if value == target:
            return i
    return -1


def _binary_search_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        n = rng.randint(0, 8)
        nums = sorted({rng.randint(-10, 10) for _ in range(n)})
        target = rng.randint(-12, 12)
        yield (nums, target)


register("09-binary-search", Oracle(slow_binary_search, _binary_search_cases))


def slow_search_rotated(nums: list[int], target: int) -> int:
    """Linear scan on a rotated array."""
    for i, value in enumerate(nums):
        if value == target:
            return i
    return -1


def _rotated_search_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        n = rng.randint(0, 7)
        vals = sorted({rng.randint(-8, 8) for _ in range(n)})
        if vals:
            k = rng.randint(0, len(vals) - 1)
            vals = vals[k:] + vals[:k]
        target = rng.randint(-10, 10)
        yield (vals, target)


register("10-search-in-rotated-sorted-array", Oracle(slow_search_rotated, _rotated_search_cases))


def slow_find_min(nums: list[int]) -> int:
    """Linear scan for the minimum."""
    best = nums[0]
    for value in nums[1:]:
        if value < best:
            best = value
    return best


def _find_min_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        n = rng.randint(1, 7)
        vals = sorted({rng.randint(-8, 8) for _ in range(n)})
        if not vals:
            vals = [0]
        k = rng.randint(0, len(vals) - 1)
        yield (vals[k:] + vals[:k],)


register("11-find-minimum-in-rotated-sorted-array", Oracle(slow_find_min, _find_min_cases))


def slow_num_islands(grid: list[list[str]]) -> int:
    """For each land cell, DFS-mark the whole component; count starts."""
    if not grid or not grid[0]:
        return 0
    g = copy.deepcopy(grid)
    rows, cols = len(g), len(g[0])

    def sink(r: int, c: int) -> None:
        if r < 0 or c < 0 or r >= rows or c >= cols or g[r][c] != "1":
            return
        g[r][c] = "0"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sink(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == "1":
                count += 1
                sink(r, c)
    return count


def _islands_cases(rng: random.Random) -> Iterator[tuple[list[list[str]],]]:
    while True:
        rows, cols = rng.randint(0, 3), rng.randint(0, 3)
        grid = [[rng.choice("01") for _ in range(cols)] for _ in range(rows)]
        yield (grid,)


register("12-number-of-islands", Oracle(slow_num_islands, _islands_cases))


# --- problems 13–24 ---


def slow_reverse_list_values(vals: list[int]) -> list[int]:
    """Build a new list by walking the input backwards."""
    out: list[int] = []
    for i in range(len(vals) - 1, -1, -1):
        out.append(vals[i])
    return out


def _reverse_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 9) for _ in range(rng.randint(0, 6))],)


register("13-reverse-linked-list", Oracle(slow_reverse_list_values, _reverse_cases))


def slow_merge_two_lists(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists by always taking the smaller head."""
    i = j = 0
    out: list[int] = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def _merge_two_cases(rng: random.Random) -> Iterator[tuple[list[int], list[int]]]:
    while True:
        a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 5)))
        b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 5)))
        yield (a, b)


register("14-merge-two-sorted-lists", Oracle(slow_merge_two_lists, _merge_two_cases))


def slow_top_k(nums: list[int], k: int) -> list[int]:
    """Count naively, then pick the k largest counts by scanning."""
    if k <= 0:
        return []
    counts: dict[int, int] = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    chosen: list[int] = []
    remaining = dict(counts)
    for _ in range(min(k, len(remaining))):
        best_key = None
        best_count = -1
        for key, count in remaining.items():
            if count > best_count or (count == best_count and (best_key is None or key < best_key)):
                best_key, best_count = key, count
        chosen.append(best_key)  # type: ignore[arg-type]
        del remaining[best_key]
    return chosen


def _same_multiset(got, want) -> bool:
    return sorted(got) == sorted(want)


def _top_k_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    """Build counts so the top-k set is unique (no frequency ties at the cutoff)."""
    while True:
        k = rng.randint(1, 4)
        # value i appears (k - i + 3) times so frequencies are strictly decreasing
        nums: list[int] = []
        for i in range(k + rng.randint(0, 2)):
            nums.extend([i] * (k + 3 - i))
        rng.shuffle(nums)
        yield (nums, k)


register("15-top-k-frequent-elements", Oracle(slow_top_k, _top_k_cases, same=_same_multiset))


class SlowLRU:
    """List of (key, value) pairs; scan and reorder on every call."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.items: list[tuple[int, int]] = []

    def get(self, key: int) -> int:
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.append(self.items.pop(i))
                return v
        return -1

    def put(self, key: int, value: int) -> None:
        for i, (k, _) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                break
        self.items.append((key, value))
        if len(self.items) > self.capacity:
            self.items.pop(0)


def _lru_ops(rng: random.Random) -> Iterator[tuple[str, tuple]]:
    while True:
        capacity = rng.randint(1, 3)
        yield ("__init__", (capacity,))
        for _ in range(12):
            if rng.random() < 0.4:
                yield ("get", (rng.randint(0, 4),))
            else:
                yield ("put", (rng.randint(0, 4), rng.randint(0, 9)))


register_ops("16-lru-cache", OpsOracle(SlowLRU, _lru_ops))


def slow_climb_stairs(n: int) -> int:
    """Try every sequence of 1-steps and 2-steps."""
    if n <= 1:
        return 1

    def ways(left: int) -> int:
        if left == 0:
            return 1
        if left < 0:
            return 0
        return ways(left - 1) + ways(left - 2)

    return ways(n)


def _climb_cases(rng: random.Random) -> Iterator[tuple[int,]]:
    while True:
        yield (rng.randint(1, 12),)


register("17-climbing-stairs", Oracle(slow_climb_stairs, _climb_cases))


def slow_rob(nums: list[int]) -> int:
    """Try every subset with no two adjacent indexes."""
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        total = 0
        ok = True
        prev = False
        for i in range(n):
            if mask & (1 << i):
                if prev:
                    ok = False
                    break
                total += nums[i]
                prev = True
            else:
                prev = False
        if ok:
            best = max(best, total)
    return best


def _rob_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 9) for _ in range(rng.randint(0, 8))],)


register("18-house-robber", Oracle(slow_rob, _rob_cases))


def slow_coin_change(coins: list[int], amount: int) -> int:
    """Try every multiset of coins up to amount counts; exponential."""
    if amount == 0:
        return 0
    if not coins:
        return -1
    best = amount + 1

    def go(left: int, start: int, used: int) -> None:
        nonlocal best
        if left == 0:
            best = min(best, used)
            return
        if used >= best:
            return
        for i in range(start, len(coins)):
            coin = coins[i]
            if coin <= left:
                go(left - coin, i, used + 1)

    go(amount, 0, 0)
    return best if best <= amount else -1


def _coin_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        coins = sorted({rng.randint(1, 5) for _ in range(rng.randint(1, 3))})
        amount = rng.randint(0, 12)
        yield (coins, amount)


register("19-coin-change", Oracle(slow_coin_change, _coin_cases))


def slow_max_profit(prices: list[int]) -> int:
    """Every buy/sell pair."""
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


def _profit_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 9) for _ in range(rng.randint(0, 7))],)


register("20-best-time-to-buy-and-sell-stock", Oracle(slow_max_profit, _profit_cases))


def slow_max_subarray(nums: list[int]) -> int:
    """Every subarray sum."""
    if not nums:
        return 0
    best = nums[0]
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, total)
    return best


def _subarray_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(-5, 5) for _ in range(rng.randint(1, 7))],)


register("21-maximum-subarray", Oracle(slow_max_subarray, _subarray_cases))


def slow_trap(height: list[int]) -> int:
    """For each index, water is min(left_max, right_max) - height."""
    n = len(height)
    total = 0
    for i in range(n):
        left = max(height[: i + 1]) if i else height[i]
        right = max(height[i:]) if i < n else height[i]
        total += min(left, right) - height[i]
    return total


def _trap_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 5) for _ in range(rng.randint(0, 7))],)


register("22-trapping-rain-water", Oracle(slow_trap, _trap_cases))


def slow_daily_temperatures(temps: list[int]) -> list[int]:
    """For each day, scan forward for a warmer day."""
    n = len(temps)
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                out[i] = j - i
                break
    return out


def _daily_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(30, 40) for _ in range(rng.randint(0, 8))],)


register("23-daily-temperatures", Oracle(slow_daily_temperatures, _daily_cases))


def slow_has_cycle_from_list(vals: list[int], pos: int) -> bool:
    """Build links in a list model; pos is the cycle entry index or -1."""
    if not vals:
        return False
    nxt = {i: i + 1 for i in range(len(vals) - 1)}
    nxt[len(vals) - 1] = None
    if 0 <= pos < len(vals):
        nxt[len(vals) - 1] = pos
    seen: set[int] = set()
    cur: int | None = 0
    while cur is not None:
        if cur in seen:
            return True
        seen.add(cur)
        cur = nxt[cur]
    return False


def _cycle_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        n = rng.randint(0, 6)
        vals = [rng.randint(0, 9) for _ in range(n)]
        pos = -1 if n == 0 or rng.random() < 0.5 else rng.randint(0, n - 1)
        yield (vals, pos)


register("24-linked-list-cycle", Oracle(slow_has_cycle_from_list, _cycle_cases))


# --- problems 25–36 ---


def slow_insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """Append, sort, then merge every overlap from scratch."""
    merged = sorted([list(iv) for iv in intervals] + [list(new)], key=lambda iv: iv[0])
    out: list[list[int]] = []
    for start, end in merged:
        if not out or out[-1][1] < start:
            out.append([start, end])
        else:
            out[-1][1] = max(out[-1][1], end)
    return out


def _insert_cases(rng: random.Random) -> Iterator[tuple[list[list[int]], list[int]]]:
    while True:
        intervals: list[list[int]] = []
        cursor = 0
        for _ in range(rng.randint(0, 5)):
            start = cursor + rng.randint(0, 2)
            end = start + rng.randint(0, 3)
            intervals.append([start, end])
            cursor = end + 1
        a, b = rng.randint(0, 15), rng.randint(0, 15)
        new = [min(a, b), max(a, b)]
        yield (intervals, new)


register("25-insert-interval", Oracle(slow_insert_interval, _insert_cases))


def slow_kth_largest(nums: list[int], k: int) -> int:
    """Sort a copy and index from the end."""
    ordered = sorted(nums)
    return ordered[-k]


def _kth_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        nums = [rng.randint(-5, 10) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, len(nums))
        yield (nums, k)


register("26-kth-largest-element", Oracle(slow_kth_largest, _kth_cases))


def slow_max_depth(vals: list[int | None]) -> int:
    """Rebuild a tiny node graph from the list encoding, then recurse."""
    if not vals or vals[0] is None:
        return 0

    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = _N(vals[0])  # type: ignore[arg-type]
    q = [root]
    idx = 1
    while q and idx < len(vals):
        cur = q.pop(0)
        if idx < len(vals) and vals[idx] is not None:
            cur.l = _N(vals[idx])  # type: ignore[arg-type]
            q.append(cur.l)
        idx += 1
        if idx < len(vals) and vals[idx] is not None:
            cur.r = _N(vals[idx])  # type: ignore[arg-type]
            q.append(cur.r)
        idx += 1

    def h(node: _N | None) -> int:
        if node is None:
            return 0
        return 1 + max(h(node.l), h(node.r))

    return h(root)


def _random_tree_vals(rng: random.Random, n: int) -> list[int | None]:
    if n <= 0:
        return []
    vals: list[int | None] = [rng.randint(0, 20)]
    remaining = n - 1
    i = 0
    while remaining > 0 and i < len(vals):
        if vals[i] is None:
            i += 1
            continue
        for _ in range(2):
            if remaining <= 0:
                vals.append(None)
                continue
            if rng.random() < 0.25 and len(vals) > 1:
                vals.append(None)
            else:
                vals.append(rng.randint(0, 20))
                remaining -= 1
        i += 1
    while vals and vals[-1] is None:
        vals.pop()
    return vals


def _depth_cases(rng: random.Random) -> Iterator[tuple[list[int | None],]]:
    while True:
        yield (_random_tree_vals(rng, rng.randint(0, 8)),)


register("27-maximum-depth-of-binary-tree", Oracle(slow_max_depth, _depth_cases))


def slow_invert(vals: list[int | None]) -> list[int | None]:
    """Build a tiny node graph, swap every child pair, flatten again."""
    if not vals or vals[0] is None:
        return []

    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = _N(vals[0])  # type: ignore[arg-type]
    q = [root]
    idx = 1
    while q and idx < len(vals):
        cur = q.pop(0)
        if idx < len(vals) and vals[idx] is not None:
            cur.l = _N(vals[idx])  # type: ignore[arg-type]
            q.append(cur.l)
        idx += 1
        if idx < len(vals) and vals[idx] is not None:
            cur.r = _N(vals[idx])  # type: ignore[arg-type]
            q.append(cur.r)
        idx += 1

    def invert(node: _N | None) -> _N | None:
        if node is None:
            return None
        node.l, node.r = invert(node.r), invert(node.l)
        return node

    invert(root)
    out: list[int | None] = []
    queue: list[_N | None] = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.v)
        queue.append(node.l)
        queue.append(node.r)
    while out and out[-1] is None:
        out.pop()
    return out


def _invert_cases(rng: random.Random) -> Iterator[tuple[list[int | None],]]:
    while True:
        yield (_random_tree_vals(rng, rng.randint(0, 8)),)


register("28-invert-binary-tree", Oracle(slow_invert, _invert_cases))


def slow_is_valid_bst(vals: list[int | None]) -> bool:
    """Inorder collect every value; check strictly increasing."""
    if not vals or vals[0] is None:
        return True

    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = _N(vals[0])  # type: ignore[arg-type]
    q = [root]
    idx = 1
    while q and idx < len(vals):
        cur = q.pop(0)
        if idx < len(vals) and vals[idx] is not None:
            cur.l = _N(vals[idx])  # type: ignore[arg-type]
            q.append(cur.l)
        idx += 1
        if idx < len(vals) and vals[idx] is not None:
            cur.r = _N(vals[idx])  # type: ignore[arg-type]
            q.append(cur.r)
        idx += 1

    seen: list[int] = []

    def inorder(node: _N | None) -> None:
        if node is None:
            return
        inorder(node.l)
        seen.append(node.v)
        inorder(node.r)

    inorder(root)
    return all(seen[i] < seen[i + 1] for i in range(len(seen) - 1))


def _bst_cases(rng: random.Random) -> Iterator[tuple[list[int | None],]]:
    while True:
        if rng.random() < 0.5:
            # valid BST via successive insert
            values = list({rng.randint(0, 20) for _ in range(rng.randint(0, 7))})
            rng.shuffle(values)

            class _N:
                def __init__(self, v: int) -> None:
                    self.v = v
                    self.l = None
                    self.r = None

            root = None
            for v in values:
                if root is None:
                    root = _N(v)
                    continue
                cur = root
                while True:
                    if v < cur.v:
                        if cur.l is None:
                            cur.l = _N(v)
                            break
                        cur = cur.l
                    else:
                        if cur.r is None:
                            cur.r = _N(v)
                            break
                        cur = cur.r
            # flatten
            if root is None:
                yield ([],)
                continue
            out: list[int | None] = []
            queue: list[_N | None] = [root]
            while queue:
                node = queue.pop(0)
                if node is None:
                    out.append(None)
                    continue
                out.append(node.v)
                queue.append(node.l)
                queue.append(node.r)
            while out and out[-1] is None:
                out.pop()
            yield (out,)
        else:
            yield (_random_tree_vals(rng, rng.randint(0, 8)),)


register("29-validate-binary-search-tree", Oracle(slow_is_valid_bst, _bst_cases))


def slow_level_order(vals: list[int | None]) -> list[list[int]]:
    """Queue over a rebuilt node graph; one list per depth."""
    if not vals or vals[0] is None:
        return []

    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = _N(vals[0])  # type: ignore[arg-type]
    build_q = [root]
    idx = 1
    while build_q and idx < len(vals):
        cur = build_q.pop(0)
        if idx < len(vals) and vals[idx] is not None:
            cur.l = _N(vals[idx])  # type: ignore[arg-type]
            build_q.append(cur.l)
        idx += 1
        if idx < len(vals) and vals[idx] is not None:
            cur.r = _N(vals[idx])  # type: ignore[arg-type]
            build_q.append(cur.r)
        idx += 1

    levels: list[list[int]] = []
    queue = [root]
    while queue:
        levels.append([node.v for node in queue])
        queue = [child for node in queue for child in (node.l, node.r) if child]
    return levels


def _level_cases(rng: random.Random) -> Iterator[tuple[list[int | None],]]:
    while True:
        yield (_random_tree_vals(rng, rng.randint(0, 8)),)


register("30-binary-tree-level-order-traversal", Oracle(slow_level_order, _level_cases))


def _flatten_bst(root) -> list[int | None]:
    if root is None:
        return []
    out: list[int | None] = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.v)
        queue.append(node.l)
        queue.append(node.r)
    while out and out[-1] is None:
        out.pop()
    return out


def _build_bst(values: list[int]):
    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = None
    for v in values:
        if root is None:
            root = _N(v)
            continue
        cur = root
        while True:
            if v < cur.v:
                if cur.l is None:
                    cur.l = _N(v)
                    break
                cur = cur.l
            else:
                if cur.r is None:
                    cur.r = _N(v)
                    break
                cur = cur.r
    return root


def slow_lca(vals: list[int | None], p: int, q: int) -> int:
    """Record root-to-node paths by scanning the whole tree; last shared node."""
    if not vals or vals[0] is None:
        raise ValueError("empty")

    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = _N(vals[0])  # type: ignore[arg-type]
    bq = [root]
    idx = 1
    while bq and idx < len(vals):
        cur = bq.pop(0)
        if idx < len(vals) and vals[idx] is not None:
            cur.l = _N(vals[idx])  # type: ignore[arg-type]
            bq.append(cur.l)
        idx += 1
        if idx < len(vals) and vals[idx] is not None:
            cur.r = _N(vals[idx])  # type: ignore[arg-type]
            bq.append(cur.r)
        idx += 1

    def path_to(target: int) -> list[int]:
        path: list[int] = []

        def walk(node: _N | None) -> bool:
            if node is None:
                return False
            path.append(node.v)
            if node.v == target or walk(node.l) or walk(node.r):
                return True
            path.pop()
            return False

        walk(root)
        return path

    a = path_to(p)
    b = path_to(q)
    ans = a[0]
    for x, y in zip(a, b, strict=False):
        if x == y:
            ans = x
        else:
            break
    return ans


def _lca_cases(rng: random.Random) -> Iterator[tuple[list[int | None], int, int]]:
    while True:
        values = list({rng.randint(0, 20) for _ in range(rng.randint(2, 8))})
        rng.shuffle(values)
        root = _build_bst(values)
        vals = _flatten_bst(root)
        p, q = rng.sample(values, 2)
        yield (vals, p, q)


register("31-lowest-common-ancestor-of-a-bst", Oracle(slow_lca, _lca_cases))


def slow_oranges_rotting(grid: list[list[int]]) -> int:
    """Rescan the whole grid every minute until nothing changes."""
    g = [row[:] for row in grid]
    if not g:
        return 0
    rows, cols = len(g), len(g[0])
    minutes = 0
    while True:
        to_rot: list[tuple[int, int]] = []
        for r in range(rows):
            for c in range(cols):
                if g[r][c] != 1:
                    continue
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 2:
                        to_rot.append((r, c))
                        break
        if not to_rot:
            break
        for r, c in to_rot:
            g[r][c] = 2
        minutes += 1
    if any(cell == 1 for row in g for cell in row):
        return -1
    return minutes


def _orange_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        grid = [[rng.choice([0, 0, 1, 1, 2]) for _ in range(cols)] for _ in range(rows)]
        yield (grid,)


register("32-rotting-oranges", Oracle(slow_oranges_rotting, _orange_cases))


def slow_can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Try every course order; accept if one respects every edge."""
    import itertools

    edges = [(a, b) for a, b in prerequisites]
    for order in itertools.permutations(range(num_courses)):
        pos = {course: i for i, course in enumerate(order)}
        if all(pos[earlier] < pos[course] for course, earlier in edges):
            return True
    return False


def _course_cases(rng: random.Random) -> Iterator[tuple[int, list[list[int]]]]:
    while True:
        n = rng.randint(1, 6)
        edges: list[list[int]] = []
        for _ in range(rng.randint(0, n)):
            a, b = rng.randint(0, n - 1), rng.randint(0, n - 1)
            if a != b and [a, b] not in edges:
                edges.append([a, b])
        yield (n, edges)


register("33-course-schedule", Oracle(slow_can_finish, _course_cases))


def slow_combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Try every multiset count vector up to target // min(candidate)."""
    ordered = sorted(set(candidates))
    answers: list[list[int]] = []

    def walk(i: int, remain: int, choice: list[int]) -> None:
        if remain == 0:
            answers.append(choice.copy())
            return
        if i == len(ordered) or remain < 0:
            return
        value = ordered[i]
        max_take = remain // value
        for take in range(0, max_take + 1):
            walk(i + 1, remain - take * value, choice + [value] * take)

    walk(0, target, [])
    return answers


def _same_combos(got, want) -> bool:
    return sorted(sorted(c) for c in got) == sorted(sorted(c) for c in want)


def _combo_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        candidates = sorted({rng.randint(1, 6) for _ in range(rng.randint(1, 4))})
        target = rng.randint(1, 12)
        yield (candidates, target)


register(
    "34-combination-sum",
    Oracle(slow_combination_sum, _combo_cases, same=_same_combos),
)


def slow_generate_parenthesis(n: int) -> list[str]:
    """All strings with n opens and n closes; keep those with valid balance."""
    import itertools

    answers: list[str] = []
    for opens in itertools.combinations(range(2 * n), n):
        chars = [")"] * (2 * n)
        for i in opens:
            chars[i] = "("
        s = "".join(chars)
        bal = 0
        ok = True
        for ch in s:
            bal += 1 if ch == "(" else -1
            if bal < 0:
                ok = False
                break
        if ok and bal == 0:
            answers.append(s)
    return answers


def _same_set(got, want) -> bool:
    return sorted(got) == sorted(want)


def _paren_cases(rng: random.Random) -> Iterator[tuple[int,]]:
    while True:
        yield (rng.randint(1, 5),)


register(
    "35-generate-parentheses",
    Oracle(slow_generate_parenthesis, _paren_cases, same=_same_set),
)


def slow_exist(board: list[list[str]], word: str) -> bool:
    """Enumerate every simple path of the right length and compare letters."""
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])
    if len(word) > rows * cols:
        return False

    def walk(r: int, c: int, index: int, used: set[tuple[int, int]]) -> bool:
        if index == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if (r, c) in used or board[r][c] != word[index]:
            return False
        used.add((r, c))
        found = any(
            walk(r + dr, c + dc, index + 1, used) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
        )
        used.remove((r, c))
        return found

    return any(walk(r, c, 0, set()) for r in range(rows) for c in range(cols))


def _word_cases(rng: random.Random) -> Iterator[tuple[list[list[str]], str]]:
    letters = "abcdef"
    while True:
        rows, cols = rng.randint(1, 3), rng.randint(1, 3)
        board = [[rng.choice(letters) for _ in range(cols)] for _ in range(rows)]
        # word from a random walk or a random string
        if rng.random() < 0.5:
            r, c = rng.randint(0, rows - 1), rng.randint(0, cols - 1)
            word_chars = [board[r][c]]
            used = {(r, c)}
            for _ in range(rng.randint(0, rows * cols - 1)):
                opts = [
                    (r + dr, c + dc)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in used
                ]
                if not opts:
                    break
                r, c = rng.choice(opts)
                used.add((r, c))
                word_chars.append(board[r][c])
            word = "".join(word_chars)
        else:
            word = "".join(rng.choice(letters) for _ in range(rng.randint(1, 4)))
        yield (board, word)


register("36-word-search", Oracle(slow_exist, _word_cases))


# --- problems 37–48 ---


def slow_unique_paths(m: int, n: int) -> int:
    """Enumerate every right/down walk with recursion and no memo."""

    def walks(r: int, c: int) -> int:
        if r == m - 1 and c == n - 1:
            return 1
        if r >= m or c >= n:
            return 0
        return walks(r + 1, c) + walks(r, c + 1)

    return walks(0, 0)


def _paths_cases(rng: random.Random) -> Iterator[tuple[int, int]]:
    while True:
        yield (rng.randint(1, 7), rng.randint(1, 7))


register("37-unique-paths", Oracle(slow_unique_paths, _paths_cases))


def slow_lcs(text1: str, text2: str) -> int:
    """Recurse on suffixes with no memo."""

    def walk(i: int, j: int) -> int:
        if i == len(text1) or j == len(text2):
            return 0
        if text1[i] == text2[j]:
            return 1 + walk(i + 1, j + 1)
        return max(walk(i + 1, j), walk(i, j + 1))

    return walk(0, 0)


def _lcs_cases(rng: random.Random) -> Iterator[tuple[str, str]]:
    letters = "abcd"
    while True:
        a = "".join(rng.choice(letters) for _ in range(rng.randint(0, 8)))
        b = "".join(rng.choice(letters) for _ in range(rng.randint(0, 8)))
        yield (a, b)


register("38-longest-common-subsequence", Oracle(slow_lcs, _lcs_cases))


class SlowTrie:
    """Store every inserted word in a list; scan on every query."""

    def __init__(self) -> None:
        self.words: list[str] = []

    def insert(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        return word in self.words

    def starts_with(self, prefix: str) -> bool:
        return any(w.startswith(prefix) for w in self.words)


def _trie_ops(rng: random.Random) -> Iterator[tuple[str, tuple]]:
    words = ["a", "ap", "app", "apple", "apply", "b", "be", "bee", "cat", "dog"]
    while True:
        yield ("__init__", ())
        for _ in range(16):
            op = rng.choice(["insert", "search", "starts_with"])
            w = rng.choice(words)
            if op == "insert":
                yield ("insert", (w,))
            elif op == "search":
                yield ("search", (w,))
            else:
                yield ("starts_with", (w[: rng.randint(1, max(1, len(w)))],))


register_ops("39-implement-trie", OpsOracle(SlowTrie, _trie_ops))


def slow_merge_k(rows: list[list[int]]) -> list[int]:
    """Repeatedly pick the smallest current head by scanning all lists."""
    pointers = [0] * len(rows)
    out: list[int] = []
    while True:
        best_i = -1
        best_val = None
        for i, row in enumerate(rows):
            if pointers[i] < len(row):
                val = row[pointers[i]]
                if best_val is None or val < best_val:
                    best_val = val
                    best_i = i
        if best_i < 0:
            return out
        out.append(best_val)  # type: ignore[arg-type]
        pointers[best_i] += 1


def _merge_k_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        k = rng.randint(0, 4)
        rows = [sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 5))) for _ in range(k)]
        yield (rows,)


register("40-merge-k-sorted-lists", Oracle(slow_merge_k, _merge_k_cases))


def slow_min_window(s: str, t: str) -> str:
    """Check every substring; keep the shortest that covers t."""
    from collections import Counter

    if not t:
        return ""
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have: Counter[str] = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= n for c, n in need.items()):
                window = s[i : j + 1]
                if best == "" or len(window) < len(best):
                    best = window
                break
    return best


def _same_window(got: str, want: str) -> bool:
    return len(got) == len(want)


def _window_cases(rng: random.Random) -> Iterator[tuple[str, str]]:
    letters = "abcde"
    while True:
        s = "".join(rng.choice(letters) for _ in range(rng.randint(0, 10)))
        t = "".join(rng.choice(letters) for _ in range(rng.randint(0, 3)))
        yield (s, t)


register(
    "41-minimum-window-substring",
    Oracle(slow_min_window, _window_cases, same=_same_window),
)


class SlowMedianFinder:
    """Keep every number in a list; sort on every median read."""

    def __init__(self) -> None:
        self.nums: list[int] = []

    def add_num(self, num: int) -> None:
        self.nums.append(num)

    def find_median(self) -> float:
        ordered = sorted(self.nums)
        n = len(ordered)
        if n == 0:
            raise ValueError("empty")
        mid = n // 2
        if n % 2:
            return float(ordered[mid])
        return (ordered[mid - 1] + ordered[mid]) / 2


def _median_ops(rng: random.Random) -> Iterator[tuple[str, tuple]]:
    while True:
        yield ("__init__", ())
        yield ("add_num", (rng.randint(-5, 5),))
        for _ in range(12):
            if rng.random() < 0.7:
                yield ("add_num", (rng.randint(-5, 5),))
            else:
                yield ("find_median", ())


register_ops("42-find-median-from-data-stream", OpsOracle(SlowMedianFinder, _median_ops))


def slow_subarray_sum(nums: list[int], k: int) -> int:
    """Try every i..j inclusive sum."""
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count


def _subarray_k_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        nums = [rng.randint(-3, 4) for _ in range(rng.randint(0, 10))]
        k = rng.randint(-5, 5)
        yield (nums, k)


register("43-subarray-sum-equals-k", Oracle(slow_subarray_sum, _subarray_k_cases))


def slow_max_sliding_window(nums: list[int], k: int) -> list[int]:
    """Max of each window by scanning the window."""
    if not nums:
        return []
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]


def _slide_max_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        n = rng.randint(1, 12)
        k = rng.randint(1, n)
        nums = [rng.randint(-5, 10) for _ in range(n)]
        yield (nums, k)


register("44-sliding-window-maximum", Oracle(slow_max_sliding_window, _slide_max_cases))


def slow_character_replacement(s: str, k: int) -> int:
    """Try every substring; count replacements needed for its best letter."""
    from collections import Counter

    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i : j + 1]
            freq = Counter(window).most_common(1)[0][1] if window else 0
            if len(window) - freq <= k:
                best = max(best, len(window))
    return best


def _replace_cases(rng: random.Random) -> Iterator[tuple[str, int]]:
    letters = "ABCD"
    while True:
        s = "".join(rng.choice(letters) for _ in range(rng.randint(0, 10)))
        k = rng.randint(0, 4)
        yield (s, k)


register(
    "45-longest-repeating-character-replacement",
    Oracle(slow_character_replacement, _replace_cases),
)


def slow_min_eating_speed(piles: list[int], h: int) -> int:
    """Try every speed from 1 to max(piles)."""
    if not piles:
        return 1

    def hours(speed: int) -> int:
        return sum((p + speed - 1) // speed for p in piles)

    for speed in range(1, max(piles) + 1):
        if hours(speed) <= h:
            return speed
    return max(piles)


def _koko_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        piles = [rng.randint(1, 12) for _ in range(rng.randint(1, 5))]
        h = rng.randint(len(piles), len(piles) + 12)
        yield (piles, h)


register("46-koko-eating-bananas", Oracle(slow_min_eating_speed, _koko_cases))


def slow_can_jump(nums: list[int]) -> bool:
    """DFS every reachable index with an explicit stack; no fancy reach array."""
    n = len(nums)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        if i >= n - 1:
            return True
        for step in range(1, nums[i] + 1):
            j = i + step
            if j not in seen and j < n:
                seen.add(j)
                stack.append(j)
            elif j >= n - 1:
                return True
    return n <= 1


def _jump_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 4) for _ in range(rng.randint(1, 10))],)


register("47-jump-game", Oracle(slow_can_jump, _jump_cases))


def slow_clone_graph_values(adj: list[list[int]]) -> list[list[int]]:
    """Copy each row into a brand-new list object."""
    out: list[list[int]] = []
    for row in adj:
        copied: list[int] = []
        for value in row:
            copied.append(value)
        out.append(copied)
    return out


def _same_clone(got, want) -> bool:
    return got == want


def _clone_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        n = rng.randint(0, 6)
        adj = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.3:
                    adj[i].append(j)
                    adj[j].append(i)
        yield (adj,)


register("48-clone-graph", Oracle(slow_clone_graph_values, _clone_cases, same=_same_clone))


# --- problems 49–56, 58 ---


def slow_network_delay(times: list[list[int]], n: int, k: int) -> int:
    """Bellman-Ford over all edges repeatedly."""
    dist = [10**9] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    reachable = dist[1:]
    if any(d >= 10**9 for d in reachable):
        return -1
    return max(reachable)


def _delay_cases(rng: random.Random) -> Iterator[tuple[list[list[int]], int, int]]:
    while True:
        n = rng.randint(1, 6)
        edges = []
        for _ in range(rng.randint(0, n * 2)):
            u, v = rng.randint(1, n), rng.randint(1, n)
            if u != v:
                edges.append([u, v, rng.randint(1, 5)])
        k = rng.randint(1, n)
        yield (edges, n, k)


register("49-network-delay-time", Oracle(slow_network_delay, _delay_cases))


def slow_find_redundant(edges: list[list[int]]) -> list[int]:
    """For each edge in order, see if the graph without later edges already connects its ends."""
    from collections import defaultdict

    def connected(graph: dict[int, list[int]], a: int, b: int) -> bool:
        seen = {a}
        stack = [a]
        while stack:
            node = stack.pop()
            if node == b:
                return True
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return False

    graph: dict[int, list[int]] = defaultdict(list)
    for a, b in edges:
        if connected(graph, a, b):
            return [a, b]
        graph[a].append(b)
        graph[b].append(a)
    return []


def _redundant_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        n = rng.randint(3, 6)
        # build a path tree then add one extra edge that closes a cycle
        edges = [[i, i + 1] for i in range(1, n)]
        a, b = rng.sample(range(1, n + 1), 2)
        while abs(a - b) == 1 or [a, b] in edges or [b, a] in edges:
            a, b = rng.sample(range(1, n + 1), 2)
        edges.append([a, b])
        rng.shuffle(edges)
        yield (edges,)


register("50-redundant-connection", Oracle(slow_find_redundant, _redundant_cases))


def slow_diameter(values: list[int | None]) -> int:
    """Try every pair of non-null nodes; BFS distance; keep the max (edges)."""
    n = len(values)
    nodes = [i for i in range(n) if i < n and values[i] is not None]
    if len(nodes) <= 1:
        return 0

    def neighbors(i: int) -> list[int]:
        out = []
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and values[left] is not None:
            out.append(left)
        if right < n and values[right] is not None:
            out.append(right)
        if i > 0:
            parent = (i - 1) // 2
            if values[parent] is not None:
                out.append(parent)
        return out

    best = 0
    for start in nodes:
        dist = {start: 0}
        queue = [start]
        while queue:
            cur = queue.pop(0)
            for nxt in neighbors(cur):
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    queue.append(nxt)
        best = max(best, max(dist.values()))
    return best


def _diameter_cases(rng: random.Random) -> Iterator[tuple[list[int | None],]]:
    while True:
        size = rng.randint(0, 10)
        values: list[int | None] = []
        for i in range(size):
            if i == 0 or (values[(i - 1) // 2] is not None and rng.random() < 0.7):
                values.append(rng.randint(1, 9))
            else:
                values.append(None)
        while values and values[-1] is None:
            values.pop()
        yield (values,)


register("51-diameter-of-binary-tree", Oracle(slow_diameter, _diameter_cases))


def slow_kth_smallest(level: list[int | None], k: int) -> int:
    """Collect values and pick after sorting."""
    values = sorted(v for v in level if v is not None)
    return values[k - 1]


def _bst_level(rng: random.Random) -> list[int | None]:
    values = list({rng.randint(0, 20) for _ in range(rng.randint(1, 8))})
    rng.shuffle(values)

    class _N:
        def __init__(self, v: int) -> None:
            self.v = v
            self.l = None
            self.r = None

    root = None
    for v in values:
        if root is None:
            root = _N(v)
            continue
        cur = root
        while True:
            if v < cur.v:
                if cur.l is None:
                    cur.l = _N(v)
                    break
                cur = cur.l
            else:
                if cur.r is None:
                    cur.r = _N(v)
                    break
                cur = cur.r
    out: list[int | None] = []
    queue: list = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.v)
        queue.append(node.l)
        queue.append(node.r)
    while out and out[-1] is None:
        out.pop()
    return out


def _kth_bst_cases(rng: random.Random) -> Iterator[tuple[list[int | None], int]]:
    while True:
        level = _bst_level(rng)
        count = sum(1 for v in level if v is not None)
        k = rng.randint(1, max(1, count))
        yield (level, k)


register("52-kth-smallest-in-bst", Oracle(slow_kth_smallest, _kth_bst_cases))


def slow_word_break(s: str, words: list[str]) -> bool:
    """Try every split recursively with no memo."""
    wordset = set(words)

    def ok(i: int) -> bool:
        if i == len(s):
            return True
        return any(s[i:j] in wordset and ok(j) for j in range(i + 1, len(s) + 1))

    return ok(0)


def _word_break_cases(rng: random.Random) -> Iterator[tuple[str, list[str]]]:
    lexicon = ["a", "b", "ab", "ba", "abc", "cat", "cats", "and", "dog", "sand"]
    while True:
        words = list({rng.choice(lexicon) for _ in range(rng.randint(1, 5))})
        s = "".join(rng.choice(words) for _ in range(rng.randint(0, 4)))
        if rng.random() < 0.3:
            s += rng.choice("xyz")
        yield (s, words)


register("53-word-break", Oracle(slow_word_break, _word_break_cases))


def slow_lis(nums: list[int]) -> int:
    """O(n²) DP: best ending at each index."""
    if not nums:
        return 0
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)


def _lis_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(-5, 10) for _ in range(rng.randint(0, 10))],)


register("54-longest-increasing-subsequence", Oracle(slow_lis, _lis_cases))


def slow_permute(nums: list[int]) -> list[list[int]]:
    """Use itertools.permutations (enumerate every ordering)."""
    import itertools

    return [list(p) for p in itertools.permutations(nums)]


def _same_perms(got, want) -> bool:
    return sorted(got) == sorted(want)


def _perm_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        n = rng.randint(0, 4)
        nums = list(range(n))
        rng.shuffle(nums)
        yield (nums,)


register("55-permutations", Oracle(slow_permute, _perm_cases, same=_same_perms))


def slow_remove_nth(values: list[int], n: int) -> list[int]:
    """Two-pass: compute length, then drop index len-n."""
    length = len(values)
    index = length - n
    return values[:index] + values[index + 1 :]


def _remove_nth_cases(rng: random.Random) -> Iterator[tuple[list[int], int]]:
    while True:
        values = [rng.randint(0, 9) for _ in range(rng.randint(1, 10))]
        n = rng.randint(1, len(values))
        yield (values, n)


register("56-remove-nth-from-end", Oracle(slow_remove_nth, _remove_nth_cases))


def slow_num_decodings(s: str) -> int:
    """Recurse on the remaining suffix with no memo."""

    def ways(i: int) -> int:
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = ways(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i : i + 2]) <= 26:
            total += ways(i + 2)
        return total

    return ways(0) if s else 0


def _decode_cases(rng: random.Random) -> Iterator[tuple[str,]]:
    while True:
        s = "".join(str(rng.randint(0, 9)) for _ in range(rng.randint(0, 8)))
        yield (s,)


register("58-decode-ways", Oracle(slow_num_decodings, _decode_cases))


# --- problems 59–68 ---


def slow_serialize_level(values: list[int | None]) -> str:
    """Build the string with an explicit loop and concatenation."""
    if not values:
        return ""
    parts: list[str] = []
    for value in values:
        parts.append("null" if value is None else str(value))
    out = parts[0]
    for part in parts[1:]:
        out = out + "," + part
    return out


def _ser_cases(rng: random.Random) -> Iterator[tuple[list[int | None],]]:
    while True:
        n = rng.randint(0, 10)
        values: list[int | None] = [
            None if rng.random() < 0.25 else rng.randint(-3, 9) for _ in range(n)
        ]
        yield (values,)


register("59-serialize-binary-tree", Oracle(slow_serialize_level, _ser_cases))


def slow_reorder_values(values: list[int]) -> list[int]:
    """Split at mid, reverse the right piece, zip into a new list."""
    n = len(values)
    if n <= 2:
        return list(values)
    mid = (n + 1) // 2
    left_vals = values[:mid]
    right_vals = list(reversed(values[mid:]))
    out: list[int] = []
    for i, a in enumerate(left_vals):
        out.append(a)
        if i < len(right_vals):
            out.append(right_vals[i])
    return out


def _reorder_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        yield ([rng.randint(0, 9) for _ in range(rng.randint(0, 10))],)


register("60-reorder-list", Oracle(slow_reorder_values, _reorder_cases))


def slow_rotate_image(matrix: list[list[int]]) -> list[list[int]]:
    """Allocate a new matrix; map (i, j) → (j, n-1-i)."""
    n = len(matrix)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            out[j][n - 1 - i] = matrix[i][j]
    # copy back so in-place callers still work when they mutate input first
    for i in range(n):
        matrix[i][:] = out[i]
    return matrix


def _rotate_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        n = rng.randint(1, 5)
        matrix = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
        yield (matrix,)


register("61-rotate-image", Oracle(slow_rotate_image, _rotate_cases))


def slow_spiral_order(matrix: list[list[int]]) -> list[int]:
    """Peel layer by layer into a new list by scanning bounds."""
    if not matrix:
        return []
    out: list[int] = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out


def _spiral_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        rows, cols = rng.randint(0, 4), rng.randint(1, 4)
        if rows == 0:
            yield ([],)
            continue
        matrix = [[rng.randint(0, 9) for _ in range(cols)] for _ in range(rows)]
        yield (matrix,)


register("62-spiral-matrix", Oracle(slow_spiral_order, _spiral_cases))


def slow_longest_palindrome(s: str) -> str:
    """Check every substring; keep a longest palindrome (leftmost on ties)."""
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            chunk = s[i : j + 1]
            if chunk == chunk[::-1] and len(chunk) > len(best):
                best = chunk
    return best


def _same_pal(got: str, want: str) -> bool:
    return len(got) == len(want) and got == got[::-1]


def _pal_cases(rng: random.Random) -> Iterator[tuple[str,]]:
    letters = "abcr"
    while True:
        yield ("".join(rng.choice(letters) for _ in range(rng.randint(0, 12))),)


register(
    "63-longest-palindromic-substring",
    Oracle(slow_longest_palindrome, _pal_cases, same=_same_pal),
)


def slow_least_interval(tasks: list[str], n: int) -> int:
    """Simulate minute by minute with remaining counts (no heap)."""
    from collections import Counter

    if not tasks:
        return 0
    counts = Counter(tasks)
    time = 0
    while counts:
        # run up to n+1 distinct kinds this frame, most frequent first
        frame = sorted(counts.keys(), key=lambda k: counts[k], reverse=True)
        used = 0
        for key in frame[: n + 1]:
            counts[key] -= 1
            if counts[key] == 0:
                del counts[key]
            used += 1
            time += 1
            if not counts:
                break
        if counts:
            time += (n + 1) - used
    return time


def _task_cases(rng: random.Random) -> Iterator[tuple[list[str], int]]:
    letters = "ABCDE"
    while True:
        tasks = [rng.choice(letters) for _ in range(rng.randint(1, 12))]
        n = rng.randint(0, 4)
        yield (tasks, n)


register("64-task-scheduler", Oracle(slow_least_interval, _task_cases))


class SlowTimeMap:
    """Store every set; get scans the whole list each time."""

    def __init__(self) -> None:
        self.rows: list[tuple[str, str, int]] = []

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.rows.append((key, value, timestamp))

    def get(self, key: str, timestamp: int) -> str:
        best_t = -1
        best_v = ""
        for k, v, t in self.rows:
            if k == key and t <= timestamp and t >= best_t:
                best_t = t
                best_v = v
        return best_v


def _timemap_ops(rng: random.Random) -> Iterator[tuple[str, tuple]]:
    keys = ["foo", "bar", "x"]
    values = ["a", "b", "c", "bar", "bar2"]
    while True:
        yield ("__init__", ())
        t = 1
        yield ("set", (rng.choice(keys), rng.choice(values), t))
        t += 1
        for _ in range(14):
            if rng.random() < 0.55:
                yield ("set", (rng.choice(keys), rng.choice(values), t))
                t += rng.randint(1, 2)
            else:
                yield ("get", (rng.choice(keys), rng.randint(0, t)))


register_ops("65-time-based-key-value", OpsOracle(SlowTimeMap, _timemap_ops))


def slow_single_number(nums: list[int]) -> int:
    """Count with a dict; return the key with count 1."""
    counts: dict[int, int] = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    for value, count in counts.items():
        if count == 1:
            return value
    raise ValueError("no singleton")


def _single_cases(rng: random.Random) -> Iterator[tuple[list[int],]]:
    while True:
        pairs = [rng.randint(-5, 10) for _ in range(rng.randint(0, 5))]
        single = rng.randint(-5, 10)
        while single in pairs:
            single = rng.randint(-5, 10)
        nums = pairs + pairs + [single]
        rng.shuffle(nums)
        yield (nums,)


register("66-single-number", Oracle(slow_single_number, _single_cases))


def slow_count_bits(n: int) -> list[int]:
    """Per number, count bits by shifting."""
    out = []
    for i in range(n + 1):
        x = i
        bits = 0
        while x:
            bits += x & 1
            x >>= 1
        out.append(bits)
    return out


def _bits_cases(rng: random.Random) -> Iterator[tuple[int,]]:
    while True:
        yield (rng.randint(0, 40),)


register("67-counting-bits", Oracle(slow_count_bits, _bits_cases))


def slow_min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Sweep: +1 at start, -1 at end; track peak."""
    if not intervals:
        return 0
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    # ends before starts at the same time so touching can reuse
    events.sort(key=lambda e: (e[0], e[1]))
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best


def _meet_cases(rng: random.Random) -> Iterator[tuple[list[list[int]],]]:
    while True:
        intervals = []
        for _ in range(rng.randint(0, 8)):
            a = rng.randint(0, 20)
            b = a + rng.randint(1, 8)
            intervals.append([a, b])
        yield (intervals,)


register("68-meeting-rooms-ii", Oracle(slow_min_meeting_rooms, _meet_cases))
