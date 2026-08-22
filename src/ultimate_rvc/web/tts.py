"""Helpers for the user-facing Edge TTS voice picker."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass
from functools import lru_cache

import gradio as gr

from ultimate_rvc.core.generate.speech import list_edge_tts_voices

if TYPE_CHECKING:
    from ultimate_rvc.web.config.tab import SpeechGenerationConfig


RUSSIAN_VOICES = "🇷🇺 Только русские"
RUSSIAN_AND_MULTILINGUAL = "✨ Русские + многоязычные"
ALL_VOICES = "🌍 Все языки"
TTS_VOICE_GROUPS = [RUSSIAN_AND_MULTILINGUAL, RUSSIAN_VOICES, ALL_VOICES]

ALL_GENDERS = "Все"
FEMALE_VOICES = "Женские"
MALE_VOICES = "Мужские"
TTS_GENDERS = [ALL_GENDERS, FEMALE_VOICES, MALE_VOICES]

TTS_STYLE_TEMPLATES: dict[str, tuple[int, int, int]] = {
    "Естественно": (0, 0, 0),
    "Мягко": (-5, -8, -2),
    "Энергично": (5, 12, 5),
    "Диктор": (-3, -10, 6),
}

_RUSSIAN_NAMES = {
    "Dariya": "Дарья",
    "Daria": "Дарья",
    "Dmitry": "Дмитрий",
    "Lev": "Лев",
    "Masha": "Маша",
    "Svetlana": "Светлана",
}


@dataclass(frozen=True)
class TTSVoice:
    """Minimal information required by the TTS voice picker."""

    short_name: str
    locale: str
    gender: str

    @property
    def multilingual(self) -> bool:
        """Return whether this is a multilingual Edge voice."""
        return "Multilingual" in self.short_name


@lru_cache(maxsize=1)
def get_edge_tts_voice_catalog() -> tuple[TTSVoice, ...]:
    """Load and cache the current Edge TTS voice catalogue."""
    voices, keys = list_edge_tts_voices()
    short_name_index = keys.index("ShortName")
    locale_index = keys.index("Locale")
    gender_index = keys.index("Gender")
    return tuple(
        TTSVoice(
            short_name=voice[short_name_index],
            locale=voice[locale_index],
            gender=voice[gender_index],
        )
        for voice in voices
    )


def get_edge_tts_voice_choices(
    group: str = RUSSIAN_AND_MULTILINGUAL,
    gender: str = ALL_GENDERS,
) -> list[tuple[str, str]]:
    """Return labelled Edge TTS choices for the selected filters."""
    voices = [
        voice
        for voice in get_edge_tts_voice_catalog()
        if _matches_group(voice, group) and _matches_gender(voice, gender)
    ]
    voices.sort(key=_voice_sort_key)
    return [(_voice_label(voice), voice.short_name) for voice in voices]


def update_tts_voice_choices(
    group: str,
    gender: str,
    current_voice: str | None,
) -> dict[str, object]:
    """Update available TTS voices while retaining a valid selection."""
    choices = get_edge_tts_voice_choices(group, gender)
    values = {value for _, value in choices}
    selected = current_voice if current_voice in values else None
    if selected is None and choices:
        selected = choices[0][1]
    return gr.update(choices=choices, value=selected)


def render_tts_voice_picker(tab_config: SpeechGenerationConfig) -> None:
    """Render language and gender filters with the Edge TTS dropdown."""
    with gr.Group(elem_classes=["tts-voice-picker"]):
        gr.HTML(
            """
            <div class="tts-picker-heading">
              <strong>🎙 Исходный голос TTS</strong>
              <span>Русские голоса и многоязычные варианты собраны в начале.</span>
            </div>
            """,
        )
        with gr.Row():
            voice_group = gr.Radio(
                choices=TTS_VOICE_GROUPS,
                value=RUSSIAN_AND_MULTILINGUAL,
                label="Каталог голосов",
                scale=2,
            )
            voice_gender = gr.Radio(
                choices=TTS_GENDERS,
                value=ALL_GENDERS,
                label="Пол голоса",
                scale=1,
            )
        tab_config.edge_tts_voice.instance.render()
        gr.HTML(
            """
            <div class="tts-picker-note">
              🇷🇺 — русский голос · 🌍 — многоязычный голос, который можно
              использовать с русским текстом.
            </div>
            """,
        )

    for component in [voice_group, voice_gender]:
        component.input(
            update_tts_voice_choices,
            inputs=[voice_group, voice_gender, tab_config.edge_tts_voice.instance],
            outputs=tab_config.edge_tts_voice.instance,
            show_progress="hidden",
        )


def apply_tts_style(style: str) -> tuple[int, int, int]:
    """Return pitch, speed, and volume settings for a TTS style."""
    return TTS_STYLE_TEMPLATES.get(style, TTS_STYLE_TEMPLATES["Естественно"])


def _matches_group(voice: TTSVoice, group: str) -> bool:
    if group == RUSSIAN_VOICES:
        return voice.locale == "ru-RU"
    if group == RUSSIAN_AND_MULTILINGUAL:
        return voice.locale == "ru-RU" or voice.multilingual
    return True


def _matches_gender(voice: TTSVoice, gender: str) -> bool:
    if gender == FEMALE_VOICES:
        return voice.gender == "Female"
    if gender == MALE_VOICES:
        return voice.gender == "Male"
    return True


def _voice_sort_key(voice: TTSVoice) -> tuple[int, int, str, str]:
    if voice.locale == "ru-RU":
        priority = 0
    elif voice.multilingual:
        priority = 1
    else:
        priority = 2
    preferred = 0 if voice.short_name == "ru-RU-SvetlanaNeural" else 1
    return priority, preferred, voice.locale, _voice_name(voice.short_name)


def _voice_label(voice: TTSVoice) -> str:
    name = _voice_name(voice.short_name)
    gender = "женский" if voice.gender == "Female" else "мужской"
    if voice.locale == "ru-RU":
        return f"🇷🇺 Русский · {_RUSSIAN_NAMES.get(name, name)} · {gender}"
    if voice.multilingual:
        return f"🌍 Многоязычный · {name} · {gender}"
    return f"{voice.locale} · {name} · {gender}"


def _voice_name(short_name: str) -> str:
    name = short_name.split("-", 2)[-1]
    for suffix in [
        "MultilingualNeural",
        ":MAI-Voice-2-Flash",
        ":MAI-Voice-2",
        "Neural",
    ]:
        name = name.removesuffix(suffix)
    return name
