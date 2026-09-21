"""Compact student record model and deterministic synthetic data generation."""

import random
import struct
from typing import Iterator, List


# The packed data payload is 40 bytes: student_id (8), marks (8), age (1),
# branch_code (1), cgpa (8), student_code (12), and two alignment bytes.
# This is the approximate per-record data size used by the benchmark. A
# Python object wrapper and the bytes object's own interpreter overhead are
# separate, so this does not claim that sys.getsizeof(record) is 40 bytes.
COMPACT_DATA = struct.Struct("<QdBBd12s2x")


class StudentRecord:
    """Immutable student record backed by one fixed-width binary payload."""

    __slots__ = ("_data",)

    def __init__(
        self,
        student_id: int,
        marks: float,
        age: int,
        branch_code: int,
        cgpa: float,
        student_code: str,
    ) -> None:
        encoded_code = student_code.encode("ascii")
        if len(encoded_code) > 12:
            raise ValueError("student_code must fit in 12 ASCII bytes")
        self._data = COMPACT_DATA.pack(
            student_id,
            marks,
            age,
            branch_code,
            cgpa,
            encoded_code.ljust(12, b"\0"),
        )

    @property
    def student_id(self) -> int:
        return COMPACT_DATA.unpack(self._data)[0]

    @property
    def marks(self) -> float:
        return COMPACT_DATA.unpack(self._data)[1]

    @property
    def age(self) -> int:
        return COMPACT_DATA.unpack(self._data)[2]

    @property
    def branch_code(self) -> int:
        return COMPACT_DATA.unpack(self._data)[3]

    @property
    def cgpa(self) -> float:
        return COMPACT_DATA.unpack(self._data)[4]

    @property
    def student_code(self) -> str:
        return COMPACT_DATA.unpack(self._data)[5].rstrip(b"\0").decode("ascii")

    def compact_data(self) -> bytes:
        """Return the record's fixed-width 40-byte data payload."""
        return self._data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StudentRecord):
            return NotImplemented
        return self._data == other._data

    def __repr__(self) -> str:
        return f"StudentRecord(student_id={self.student_id}, marks={self.marks})"


BRANCHES = ["CSE", "ECE", "EEE", "ME", "CE", "IT"]


def generate_students(count: int, seed: int = 42) -> List[StudentRecord]:
    """Generate repeatable records without relying on external packages."""
    return list(iter_students(count, seed))


def iter_students(count: int, seed: int = 42) -> Iterator[StudentRecord]:
    """Yield records one at a time so large datasets need bounded memory."""
    if count < 0:
        raise ValueError("count must be non-negative")

    generator = random.Random(seed)

    for student_number in range(1, count + 1):
        marks = round(generator.uniform(35.0, 100.0), 2)
        yield StudentRecord(
            student_id=student_number,
            marks=marks,
            age=generator.randint(18, 24),
            branch_code=generator.randrange(len(BRANCHES)),
            cgpa=round(4.0 + (marks / 100.0) * 6.0, 2),
            student_code=f"ST{student_number:010d}",
        )
