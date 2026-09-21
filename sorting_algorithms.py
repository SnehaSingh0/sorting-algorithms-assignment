"""Five sorting algorithms implemented without sorted() or list.sort()."""

from typing import Callable, List

from student_records import StudentRecord

RecordKey = Callable[[StudentRecord], float]


def bubble_sort(records: List[StudentRecord], key: RecordKey) -> List[StudentRecord]:
    """Repeatedly swap adjacent records that are out of order."""
    for end in range(len(records) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if key(records[index]) > key(records[index + 1]):
                records[index], records[index + 1] = records[index + 1], records[index]
                swapped = True
        if not swapped:
            break
    return records


def selection_sort(records: List[StudentRecord], key: RecordKey) -> List[StudentRecord]:
    """Repeatedly place the smallest remaining record at the next position."""
    for start in range(len(records) - 1):
        smallest = start
        for index in range(start + 1, len(records)):
            if key(records[index]) < key(records[smallest]):
                smallest = index
        if smallest != start:
            records[start], records[smallest] = records[smallest], records[start]
    return records


def insertion_sort(records: List[StudentRecord], key: RecordKey) -> List[StudentRecord]:
    """Insert each record into the sorted part on its left."""
    for index in range(1, len(records)):
        current = records[index]
        current_key = key(current)
        position = index - 1
        while position >= 0 and key(records[position]) > current_key:
            records[position + 1] = records[position]
            position -= 1
        records[position + 1] = current
    return records


def merge_sort(records: List[StudentRecord], key: RecordKey) -> List[StudentRecord]:
    """Divide the list and merge sorted halves back together."""
    if len(records) <= 1:
        return records

    middle = len(records) // 2
    left = merge_sort(records[:middle], key)
    right = merge_sort(records[middle:], key)
    merged: List[StudentRecord] = []
    left_index = right_index = 0

    while left_index < len(left) and right_index < len(right):
        if key(left[left_index]) <= key(right[right_index]):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


def quick_sort(records: List[StudentRecord], key: RecordKey) -> List[StudentRecord]:
    """Sort in place using Hoare partitioning and an explicit work stack."""
    if len(records) < 2:
        return records

    pending_ranges = [(0, len(records) - 1)]
    while pending_ranges:
        low, high = pending_ranges.pop()
        left, right = low, high
        pivot_value = key(records[(low + high) // 2])

        while left <= right:
            while key(records[left]) < pivot_value:
                left += 1
            while key(records[right]) > pivot_value:
                right -= 1
            if left <= right:
                records[left], records[right] = records[right], records[left]
                left += 1
                right -= 1

        if low < right:
            pending_ranges.append((low, right))
        if left < high:
            pending_ranges.append((left, high))

    return records


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}
