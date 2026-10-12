# 16. LRU Cache — walkthrough

## Recognize it
Design a fixed-capacity cache with `get(key)` and `put(key, value)`. Both operations must run in expected O(1). When the cache is full and you insert a new key, evict the least recently used entry. A successful `get` and an update via `put` both count as a use and must move that key to most-recent. Look-alike: LFU (evict least frequent, not least recent). Another look-alike: a plain dict with no eviction policy.

## Brute force
Store pairs in a list. On `get`, scan for the key (O(n)), then move that entry to the end. On `put`, scan to update or append, and if over capacity delete index 0. Correct, but every operation is O(capacity), which fails the O(1) requirement when capacity is large and the call sequence is long.

## Key insight
O(1) lookup needs a hash map. O(1) "move to most recent" and "pop least recent" need an ordered sequence with cheap moves at both ends. `OrderedDict` gives both: map semantics plus a doubly linked order. The front of the order is oldest; the end is newest. Manual design uses a dict from key to node plus a doubly linked list with sentinel head/tail.

## Algorithm
Using `OrderedDict`:
1. `__init__(capacity)`: store `capacity` and an empty `OrderedDict` as `data`.
2. `get(key)`: if missing, return `-1`. Else `move_to_end(key)` and return the value.
3. `put(key, value)`: if key exists, `move_to_end(key)` then assign the new value. If it is new, assign the value (lands at the end). While `len(data) > capacity`, `popitem(last=False)` to drop the oldest.

## Trace
Capacity 2. Sequence: `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)`, `get(2)`, `get(3)`.

| op | ordered keys (oldest→newest) | notes |
|---|---|---|
| put(1,1) | [1] | |
| put(2,2) | [1,2] | |
| get(1) → 1 | [2,1] | 1 becomes newest |
| put(3,3) | [1,3] | evict 2 (oldest) |
| get(2) → -1 | [1,3] | miss |
| get(3) → 3 | [1,3] | 3 already newest; still moves to end |

## Complexity
Each `get`/`put` does a constant number of hash and linked-list operations: O(1) amortized/expected time. Space is O(capacity) for keys and values stored. The list scan design is O(capacity) per call and is only acceptable for tiny caches.

## Edge cases
Capacity 1: every new key evicts the only resident. `put` on an existing key updates value and refreshes recency without growing size. `get` on a missing key must not change order. Capacity must be positive in normal prompts. Evict before or after insert carefully so you never hold capacity+1 after the operation finishes (`OrderedDict` pop after insert is the usual pattern).

## Alternatives and trade-offs
Hand-rolled doubly linked list + dict is what many reviewers want to hear: each node has `key`, `value`, `prev`, `next`; map points to nodes; sentinels simplify unlink/insert. `OrderedDict` (or Java `LinkedHashMap`) is production-smart and shorter. A heap keyed by timestamp fails O(1) updates unless you add lazy deletion. TTL caches add expiration on top of LRU—different problem.

## Common bugs
Evicting the newest key (`popitem(last=True)` by mistake). Forgetting that `get` counts as use, so a frequently read key never becomes cold. Updating a value in place without moving the key to most-recent. Checking capacity before updating an existing key and wrongly evicting when size did not grow.

## Follow-ups
LFU cache. LRU with TTL. Thread-safe cache under concurrent gets/puts. Return eviction victims for metrics.

## Related problems
LFU Cache, Design Hit Counter, Insert Delete GetRandom O(1) (hash + structure for O(1) ops), Time Based Key-Value Store.
