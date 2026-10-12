def three_sum(nums: list[int]) -> list[list[int]]:
    """Return every unique triplet that sums to 0.

    Approach: sort a copy, fix one value, and scan the rest with two pointers.
    Time: O(n^2)
    Space: O(1) extra, aside from the copy and the answer
    Alternative: a hash set for each pair, which uses more space.
    Common bugs: skipping duplicates on only one pointer, so the same triplet appears twice.
    """
    ordered = sorted(nums)
    found = []
    for index in range(len(ordered) - 2):
        if index > 0 and ordered[index] == ordered[index - 1]:
            continue
        left, right = index + 1, len(ordered) - 1
        while left < right:
            total = ordered[index] + ordered[left] + ordered[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                found.append([ordered[index], ordered[left], ordered[right]])
                left += 1
                right -= 1
                while left < right and ordered[left] == ordered[left - 1]:
                    left += 1
                while left < right and ordered[right] == ordered[right + 1]:
                    right -= 1
    return found
