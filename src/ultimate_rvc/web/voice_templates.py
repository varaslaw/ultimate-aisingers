"""Ready-to-use RVC conversion settings for the web interface."""

from __future__ import annotations

from typing import Any

import gradio as gr

from ultimate_rvc.typing_extra import F0Method

VOICE_TEMPLATE_FIELDS = (
    "f0_method",
    "index_rate",
    "rms_mix_rate",
    "protect_rate",
    "split_voice",
    "autotune_voice",
    "autotune_strength",
    "clean_voice",
    "clean_strength",
)

VOICE_TEMPLATES: dict[str, dict[str, Any]] = {
    "Натуральный вокал": {
        "f0_method": F0Method.RMVPE,
        "index_rate": 0.35,
        "rms_mix_rate": 1.0,
        "protect_rate": 0.33,
        "split_voice": False,
        "autotune_voice": False,
        "autotune_strength": 1.0,
        "clean_voice": False,
        "clean_strength": 0.7,
    },
    "Чистый сложный вокал": {
        "f0_method": F0Method.RMVPE,
        "index_rate": 0.25,
        "rms_mix_rate": 1.0,
        "protect_rate": 0.45,
        "split_voice": True,
        "autotune_voice": False,
        "autotune_strength": 1.0,
        "clean_voice": True,
        "clean_strength": 0.5,
    },
    "Выразительный тембр": {
        "f0_method": F0Method.RMVPE,
        "index_rate": 0.65,
        "rms_mix_rate": 0.9,
        "protect_rate": 0.25,
        "split_voice": False,
        "autotune_voice": False,
        "autotune_strength": 1.0,
        "clean_voice": False,
        "clean_strength": 0.7,
    },
    "Быстрый предпросмотр": {
        "f0_method": F0Method.FCPE,
        "index_rate": 0.3,
        "rms_mix_rate": 1.0,
        "protect_rate": 0.33,
        "split_voice": False,
        "autotune_voice": False,
        "autotune_strength": 1.0,
        "clean_voice": False,
        "clean_strength": 0.7,
    },
}


def apply_voice_template(template: str) -> list[dict[str, Any]]:
    """Return Gradio updates for the RVC controls in a voice template."""
    settings = VOICE_TEMPLATES[template]
    return [gr.update(value=settings[field]) for field in VOICE_TEMPLATE_FIELDS]
