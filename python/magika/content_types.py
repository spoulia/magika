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

"""Content type definitions and metadata for Magika."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from magika.types import ContentTypeLabel


@dataclass
class ContentTypeInfo:
    """Metadata about a detected content type."""

    label: ContentTypeLabel
    mime_type: str
    group: str
    description: str
    extensions: List[str] = field(default_factory=list)
    is_text: bool = False
    tags: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.label} ({self.mime_type})"


# Registry of known content types with their metadata
CONTENT_TYPES_REGISTRY: Dict[ContentTypeLabel, ContentTypeInfo] = {
    ContentTypeLabel.TXT: ContentTypeInfo(
        label=ContentTypeLabel.TXT,
        mime_type="text/plain",
        group="text",
        description="Plain text",
        extensions=[".txt", ".text"],
        is_text=True,
        tags=["text"],
    ),
    ContentTypeLabel.HTML: ContentTypeInfo(
        label=ContentTypeLabel.HTML,
        mime_type="text/html",
        group="text",
        description="HTML document",
        extensions=[".html", ".htm"],
        is_text=True,
        tags=["text", "web"],
    ),
    ContentTypeLabel.PDF: ContentTypeInfo(
        label=ContentTypeLabel.PDF,
        mime_type="application/pdf",
        group="document",
        description="PDF document",
        extensions=[".pdf"],
        is_text=False,
        tags=["document"],
    ),
    ContentTypeLabel.PYTHON: ContentTypeInfo(
        label=ContentTypeLabel.PYTHON,
        mime_type="text/x-python",
        group="code",
        description="Python source code",
        extensions=[".py", ".pyw"],
        is_text=True,
        tags=["code", "script"],
    ),
    ContentTypeLabel.JAVASCRIPT: ContentTypeInfo(
        label=ContentTypeLabel.JAVASCRIPT,
        mime_type="application/javascript",
        group="code",
        description="JavaScript source code",
        extensions=[".js", ".mjs"],
        is_text=True,
        tags=["code", "web", "script"],
    ),
    ContentTypeLabel.JSON: ContentTypeInfo(
        label=ContentTypeLabel.JSON,
        mime_type="application/json",
        group="data",
        description="JSON data",
        extensions=[".json"],
        is_text=True,
        tags=["data", "structured"],
    ),
    ContentTypeLabel.UNKNOWN: ContentTypeInfo(
        label=ContentTypeLabel.UNKNOWN,
        mime_type="application/octet-stream",
        group="unknown",
        description="Unknown content type",
        extensions=[],
        is_text=False,
        tags=[],
    ),
}


def get_content_type_info(label: ContentTypeLabel) -> Optional[ContentTypeInfo]:
    """Retrieve metadata for a given content type label.

    Args:
        label: The ContentTypeLabel to look up.

    Returns:
        ContentTypeInfo if found, otherwise None.
    """
    return CONTENT_TYPES_REGISTRY.get(label)


def get_all_content_type_labels() -> List[ContentTypeLabel]:
    """Return all registered content type labels."""
    return list(CONTENT_TYPES_REGISTRY.keys())


def get_text_content_type_labels() -> List[ContentTypeLabel]:
    """Return labels for all content types classified as text."""
    return [
        label
        for label, info in CONTENT_TYPES_REGISTRY.items()
        if info.is_text
    ]
