
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """True when the prerequisite graph has no cycle.

    Approach: Kahn. Edges point from the prerequisite to the course.
    Time: O(courses + prerequisites)
    Space: O(courses + prerequisites)
    Alternative: depth-first search with three colors.
    Common bugs: pointing the edge from the course back to the prerequisite.
    """
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, earlier in prerequisites:
        graph[earlier].append(course)
        indegree[course] += 1
    ready = [course for course in range(num_courses) if indegree[course] == 0]
    finished = 0
    while ready:
        course = ready.pop()
        finished += 1
        for later in graph[course]:
            indegree[later] -= 1
            if indegree[later] == 0:
                ready.append(later)
    return finished == num_courses
