# 33. Course Schedule — walkthrough

## Recognize it
`num_courses` nodes and prerequisite edges `[course, earlier]` meaning you must take `earlier` before `course`. Return whether you can finish all courses—equivalently, whether the directed graph is acyclic (a DAG). Look-alike: course schedule II (return a topological order). Another look-alike: detect a cycle in an undirected graph (different algorithm).

## Brute force
Try every permutation of courses and test prerequisites—factorial time. Slightly better: DFS from each node looking for a back edge without memoizing global state still repeats work. You need a linear graph algorithm.

## Key insight
Kahn's algorithm: repeatedly take nodes with indegree 0 (no unmet prereq). Each such course "finishes" and decrements indegrees of dependents. If you finish all courses, there was no cycle; if you get stuck with leftover positive indegrees, a cycle remains.

## Algorithm
1. Build `graph[earlier] → list of courses` and `indegree[course]`.
2. Seed `ready` with every course whose indegree is 0.
3. `finished = 0`. While `ready`: pop a course, `finished += 1`, decrement neighbors; when a neighbor hits 0, push it.
4. Return `finished == num_courses`.

## Trace
`num_courses = 4`, prereqs `[[1,0],[2,0],[3,1],[3,2]]` (edges 0→1, 0→2, 1→3, 2→3).

| ready | pop | indegree after | finished |
|---|---|---|---|
| [0] | 0 | 1:0, 2:0, 3:2 | 1 |
| [1,2] | 1 | 3:1 | 2 |
| [2] | 2 | 3:0 | 3 |
| [3] | 3 | — | 4 |

Return True. Add edge `[0,3]` and 3 never reaches indegree 0 while 0 waits on 3 → finished < 4 → False.

## Complexity
Each node and edge processed once: O(V+E) time and space. DFS three-color (white/gray/black) is the same asymptotics; gray hit means a back edge / cycle. Either is acceptable; Kahn naturally extends to producing an order.

## Edge cases
No prerequisites → True (all indegree 0). Self-loop → False. Disconnected parallel chains → still fine; all zeros start ready. Duplicate edges: indegree counts each (prompt usually unique). `num_courses = 1` with empty prereqs → True.

## Alternatives and trade-offs
DFS cycle detection with recursion stack set is common. Union-find does not apply cleanly to directed cycles. Returning the order (schedule II) is Kahn with an appended list—same loop. Prefer stating edge direction out loud: "edge from prereq toward course" so indegree means "waiting on prereqs."

## Common bugs
Reversing the edge (`graph[course].append(earlier)`). Comparing `finished == len(prerequisites)` instead of `num_courses`. Forgetting courses that never appear in the edge list (they must start in `ready`). Using BFS layering for shortest path when you only need acyclicity.

## Follow-ups
Course Schedule II (return order). Parallel courses with semester limits. Alien dictionary (topo on letter graph).

## Related problems
Course Schedule II, Alien Dictionary, Redundant Connection (undirected cycle), Clone Graph.
