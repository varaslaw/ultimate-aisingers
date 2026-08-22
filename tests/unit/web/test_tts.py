"""Tests for the TTS voice picker helpers."""

from ultimate_rvc.web import tts


def _catalog() -> tuple[tts.TTSVoice, ...]:
    return (
        tts.TTSVoice("en-US-AvaMultilingualNeural", "en-US", "Female"),
        tts.TTSVoice("en-US-ChristopherNeural", "en-US", "Male"),
        tts.TTSVoice("ru-RU-DmitryNeural", "ru-RU", "Male"),
        tts.TTSVoice("ru-RU-SvetlanaNeural", "ru-RU", "Female"),
    )


def test_russian_compatible_voices_are_prioritized(monkeypatch) -> None:
    monkeypatch.setattr(tts, "get_edge_tts_voice_catalog", _catalog)

    choices = tts.get_edge_tts_voice_choices()

    assert [value for _, value in choices] == [
        "ru-RU-SvetlanaNeural",
        "ru-RU-DmitryNeural",
        "en-US-AvaMultilingualNeural",
    ]


def test_voice_filters_keep_only_requested_gender(monkeypatch) -> None:
    monkeypatch.setattr(tts, "get_edge_tts_voice_catalog", _catalog)

    choices = tts.get_edge_tts_voice_choices(
        tts.RUSSIAN_AND_MULTILINGUAL,
        tts.FEMALE_VOICES,
    )

    assert [value for _, value in choices] == [
        "ru-RU-SvetlanaNeural",
        "en-US-AvaMultilingualNeural",
    ]


def test_tts_style_template() -> None:
    assert tts.apply_tts_style("Энергично") == (5, 12, 5)
