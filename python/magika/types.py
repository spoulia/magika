# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Type definitions for the Magika file type detection library."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class MagikaStatus(str, Enum):
    """Status codes for Magika detection results."""

    OK = "ok"
    EMPTY_FILE = "empty_file"
    FILE_TOO_SMALL = "file_too_small"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class ContentTypeLabel:
    """Represents a content type label with associated metadata."""

    name: str
    mime_type: str
    group: str
    description: str
    extensions: List[str] = field(default_factory=list)
    is_text: bool = False

    def __str__(self) -> str:
        return self.name


@dataclass
class MagikaResult:
    """Result of a Magika file type detection operation."""

    path: Path
    dl: "MagikaDlResult"
    output: "MagikaOutputResult"
    status: MagikaStatus

    @property
    def ok(self) -> bool:
        """Returns True if the detection was successful."""
        return self.status == MagikaStatus.OK


@dataclass
class MagikaDlResult:
    """Result from the deep learning model inference."""

    ct_label: str
    score: float
    is_text: bool
    magic_bytes_ct_label: Optional[str] = None


@dataclass
class MagikaOutputResult:
    """Final output result after post-processing and overrides."""

    ct_label: str
    score: float
    mime_type: str
    group: str
    description: str
    extensions: List[str] = field(default_factory=list)
    is_text: bool = False

    def __str__(self) -> str:
        return (
            f"MagikaOutputResult("
            f"ct_label={self.ct_label!r}, "
            f"score={self.score:.4f}, "
            f"mime_type={self.mime_type!r}, "
            f"is_text={self.is_text}"
            f")"
        )


@dataclass
class ModelFeatures:
    """Features extracted from a file for model inference."""

    beg: List[int]
    mid: List[int]
    end: List[int]

    def __post_init__(self) -> None:
        if not (len(self.beg) == len(self.mid) == len(self.end)):
            raise ValueError(
                "beg, mid, and end feature arrays must have the same length, "
                f"got {len(self.beg)}, {len(self.mid)}, {len(self.end)}"
            )

    @property
    def size(self) -> int:
        """Returns the number of features per segment."""
        return len(self.beg)
