"""
Module which defines extra types for the web application of the Ultimate
RVC project.
"""

from __future__ import annotations

from typing import Any, TypedDict

from collections.abc import Callable, Sequence
from enum import StrEnum, auto

type AnyCallable = Callable[..., Any]

type BaseDropdownChoices = Sequence[str | int | float | tuple[str, str | int | float]]
type DropdownChoices = BaseDropdownChoices | None
type BaseDropdownValue = str | int | float | Sequence[str | int | float] | None
type DropdownValue = BaseDropdownValue | AnyCallable

type RadioChoices = DropdownChoices
type BaseRadioValue = str | int | float | None
type RadioValue = BaseRadioValue | AnyCallable


class ConcurrencyId(StrEnum):
    """Enumeration of possible concurrency identifiers."""

    GPU = auto()


class SongSourceType(StrEnum):
    """The type of source providing the song to generate a cover of."""

    PATH = "YouTube или путь к файлу"
    LOCAL_FILE = "Локальный файл"
    CACHED_SONG = "Загруженный трек"


class SpeechSourceType(StrEnum):
    """The type of source providing the text to generate speech from."""

    TEXT = "Текст"
    LOCAL_FILE = "Текстовый файл"


class SongTransferOption(StrEnum):
    """Enumeration of possible song transfer options."""

    STEP_1_AUDIO = "Шаг 1: трек"
    STEP_2_VOCALS = "Шаг 2: вокал"
    STEP_3_VOCALS = "Шаг 3: вокал"
    STEP_4_INSTRUMENTALS = "Шаг 4: инструментал"
    STEP_4_BACKUP_VOCALS = "Шаг 4: бэк-вокал"
    STEP_5_MAIN_VOCALS = "Шаг 5: основной вокал"
    STEP_5_INSTRUMENTALS = "Шаг 5: инструментал"
    STEP_5_BACKUP_VOCALS = "Шаг 5: бэк-вокал"


class SpeechTransferOption(StrEnum):
    """Enumeration of possible speech transfer options."""

    STEP_2_SPEECH = "Шаг 2: речь"
    STEP_3_SPEECH = "Шаг 3: речь"


class ComponentVisibilityKwArgs(TypedDict, total=False):
    """
    Keyword arguments for setting component visibility.

    Attributes
    ----------
    visible : bool
        Whether the component should be visible.
    value : Any
        The value of the component.

    """

    visible: bool
    value: Any


class UpdateDropdownKwArgs(TypedDict, total=False):
    """
    Keyword arguments for updating a dropdown component.

    Attributes
    ----------
    choices : DropdownChoices
        The updated choices for the dropdown component.
    value : DropdownValue
        The updated value for the dropdown component.

    """

    choices: DropdownChoices
    value: DropdownValue


class TextBoxKwArgs(TypedDict, total=False):
    """
    Keyword arguments for updating a textbox component.

    Attributes
    ----------
    value : str | None
        The updated value for the textbox component.
    placeholder : str | None
        The updated placeholder for the textbox component.

    """

    value: str | None
    placeholder: str | None


class UpdateAudioKwArgs(TypedDict, total=False):
    """
    Keyword arguments for updating an audio component.

    Attributes
    ----------
    value : str | None
        The updated value for the audio component.

    """

    value: str | None
