"""Module defining common component configurations for UI tabs."""

from __future__ import annotations

from pydantic import BaseModel

from ultimate_rvc.typing_extra import (
    AudioExt,
    EmbedderModel,
    F0Method,
    SampleRate,
)
from ultimate_rvc.web.config.component import (
    CheckboxConfig,
    DropdownConfig,
    NumberConfig,
    SliderConfig,
    TextboxConfig,
)
from ultimate_rvc.web.typing_extra import SongSourceType, SpeechSourceType


class BaseTabConfig(BaseModel):
    """
    Base model defining common component configuration settings for
    UI tabs.

    Attributes
    ----------
    embedder_model : DropdownConfig
        Configuration settings for an embedder model dropdown component.
    custom_embedder_model : DropdownConfig
        Configuration settings for a custom embedder model dropdown
        component.

    """

    embedder_model: DropdownConfig = DropdownConfig(
        label="Модель эмбеддера",
        info="Модель, которая используется для построения голосовых эмбеддингов.",
        value=EmbedderModel.CONTENTVEC,
        choices=list(EmbedderModel),
        exclude_value=True,
    )
    custom_embedder_model: DropdownConfig = DropdownConfig(
        label="Пользовательская модель эмбеддера",
        info="Выберите пользовательскую модель эмбеддера из списка.",
        value=None,
        visible=False,
        render=False,
        exclude_value=True,
    )


class GenerationConfig(BaseTabConfig):
    """
    Common component configuration settings for generation tabs.

    voice_model : DropdownConfig
        Configuration settings for a voice model dropdown component.
    f0_method : DropdownConfig
        Configuration settings for a pitch extraction algorithm
        dropdown component.
    index_rate : SliderConfig
        Configuration settings for an index rate slider component.
    rms_mix_rate : SliderConfig
        Configuration settings for a RMS mix rate slider component.
    protect_rate : SliderConfig
        Configuration settings for a protect rate slider component.
    split_voice : CheckboxConfig
        Configuration settings for a split voice checkbox component.
    autotune_voice: CheckboxConfig
        Configuration settings for an autotune voice checkbox component.
    autotune_strength: SliderConfig
        Configuration settings for an autotune strength slider
        component.
    proposed_pitch: CheckboxConfig
        Configuration settings for a proposed pitch checkbox component.
    proposed_pitch_threshold: SliderConfig
        Configuration settings for a proposed pitch threshold slider
        component.
    sid : NumberConfig
        Configuration settings for a speaker ID number component.
    output_sr : DropdownConfig
        Configuration settings for an output sample rate dropdown
        component.
    output_format : DropdownConfig
        Configuration settings for an output format dropdown
        component.
    output_name : TextboxConfig
        Configuration settings for an output name textbox component.

    See Also
    --------
    BaseTabConfig
        Parent model defining common component configuration settings
        for UI tabs.

    """

    voice_model: DropdownConfig = DropdownConfig(
        label="Голосовая модель",
        info="Выберите модель, которая будет использоваться для конверсии голоса.",
        value=None,
        render=False,
        exclude_value=True,
    )
    f0_method: DropdownConfig = DropdownConfig(
        label="Алгоритм извлечения высоты",
        info=(
            "RMVPE — надёжный выбор для финального вокала. FCPE — для быстрого"
            " предпросмотра. CREPE точнее на некоторых сложных партиях, но работает"
            " медленнее; CREPE Tiny — самый быстрый, но менее устойчивый."
        ),
        value=F0Method.RMVPE,
        choices=list(F0Method),
        multiselect=False,
    )
    index_rate: SliderConfig = SliderConfig(
        label="Сила индекса",
        info=(
            "Чем выше значение, тем сильнее конверсия стремится к акценту модели."
            " Уменьшение может снизить артефакты, приходящие из модели"
            " голоса.<br><br><br>"
        ),
        value=0.3,
        minimum=0.0,
        maximum=1.0,
    )
    rms_mix_rate: SliderConfig = SliderConfig(
        label="Смешивание RMS",
        info=(
            "Насколько сохранять громкость исходного голоса (0) или приводить её"
            " к фиксированной громкости (1). Значение 1 рекомендовано в большинстве"
            " случаев.<br><br>"
        ),
        value=1.0,
        minimum=0.0,
        maximum=1.0,
    )
    protect_rate: SliderConfig = SliderConfig(
        label="Степень защиты",
        info=(
            "Определяет, насколько активно защищать согласные и дыхание от артефактов."
            " Чем выше значение, тем больше защита, но может ухудшиться эффект"
            " индексации.<br><br>"
        ),
        value=0.33,
        minimum=0.0,
        maximum=0.5,
    )

    split_voice: CheckboxConfig = CheckboxConfig(
        label="Делить входной голос",
        info=(
            "Разделять ли входную дорожку на мелкие сегменты перед конверсией."
            " Это может улучшить качество для длинных треков."
        ),
        value=False,
    )
    autotune_voice: CheckboxConfig = CheckboxConfig(
        label="Автотюн для конвертированного голоса",
        info="Применять ли автотюн к сконвертированному голосу.",
        value=False,
        exclude_value=True,
    )
    autotune_strength: SliderConfig = SliderConfig(
        label="Интенсивность автотюна",
        info=(
            "Высокие значения сильнее привязывают ноты к хроматической сетке и"
            " могут добавить артефакты."
        ),
        value=1.0,
        minimum=0.0,
        maximum=1.0,
        visible=False,
    )
    proposed_pitch: CheckboxConfig = CheckboxConfig(
        label="Предложенная высота",
        info=(
            "Настраивать ли высоту конвертированного голоса под диапазон выбранной"
            " модели."
        ),
        value=False,
        exclude_value=True,
    )
    proposed_pitch_threshold: SliderConfig = SliderConfig(
        label="Порог предложенной высоты",
        info=(
            "Для мужских моделей обычно 155.0, для женских — примерно 255.0."
        ),
        value=155.0,
        minimum=50.0,
        maximum=1200.0,
        visible=False,
    )
    sid: NumberConfig = NumberConfig(
        label="ID спикера",
        info="Идентификатор спикера для многоголосовых моделей.",
        value=0,
        precision=0,
    )
    output_sr: DropdownConfig = DropdownConfig(
        label="Частота дискретизации вывода",
        info="Частота дискретизации итоговой смешанной дорожки.",
        value=SampleRate.HZ_44K,
        choices=list(SampleRate),
    )
    output_format: DropdownConfig = DropdownConfig(
        label="Формат вывода",
        info="Аудиоформат итоговой дорожки.",
        value=AudioExt.MP3,
        choices=list(AudioExt),
    )
    output_name: TextboxConfig = TextboxConfig(
        label="Имя файла",
        info="Если имя не указано, подходящее название будет создано автоматически.",
        value=None,
        placeholder="Выходной файл AISingers",
        exclude_value=True,
    )


class SongGenerationConfig(GenerationConfig):
    """
    Common component configuration settings for song generation tabs.

    Attributes
    ----------
    source_type : DropdownConfig
        Configuration settings for a source type dropdown component.
    source : TextboxConfig
        Configuration settings for an input source textbox component.
    cached_song : DropdownConfig
        Configuration settings for a cached song dropdown component.
    clean_strength : SliderConfig
        Configuration settings for a clean strength slider component.
    clean_voice : CheckboxConfig
        Configuration settings for a clean voice checkbox component.
    room_size : SliderConfig
        Configuration settings for a room size slider component.
    wet_level : SliderConfig
        Configuration settings for a wetness level slider component.
    dry_level : SliderConfig
        Configuration settings for a dryness level slider component.
    damping : SliderConfig
        Configuration settings for a damping level slider component.
    main_gain : SliderConfig
        Configuration settings for a main gain slider component.
    inst_gain : SliderConfig
        Configuration settings for an instrumentals gain slider
        component.
    backup_gain : SliderConfig
        Configuration settings for a backup vocals gain slider
        component.

    See Also
    --------
    GenerationConfig
        Parent model defining common component configuration settings
        for song generation tabs.

    """

    source_type: DropdownConfig = DropdownConfig(
        label="Тип источника",
        info="Откуда брать трек для кавера.",
        value=SongSourceType.PATH,
        choices=list(SongSourceType),
        type="index",
        exclude_value=True,
    )
    source: TextboxConfig = TextboxConfig(
        label="Источник",
        info="Ссылка на трек в YouTube или полный путь к локальному аудиофайлу.",
        value=None,
        exclude_value=True,
    )
    cached_song: DropdownConfig = DropdownConfig(
        label="Источник",
        info="Выберите трек из списка уже загруженных.",
        value=None,
        visible=False,
        render=False,
        exclude_value=True,
    )
    clean_voice: CheckboxConfig = CheckboxConfig(
        label="Очистка конвертированного голоса",
        info="Применять ли шумоподавление к сконвертированному голосу.",
        value=False,
        exclude_value=True,
    )
    clean_strength: SliderConfig = SliderConfig.clean_strength(visible=False)
    room_size: SliderConfig = SliderConfig(
        label="Размер пространства",
        info=(
            "Определяет длину и объём хвоста реверберации. Небольшие значения "
            "звучат ближе и суше, большие дают ощущение зала."
        ),
        value=0.15,
        minimum=0.0,
        maximum=1.0,
    )
    wet_level: SliderConfig = SliderConfig(
        label="Реверберация",
        info="Сколько обработанного реверберацией сигнала добавить к голосу.",
        value=0.2,
        minimum=0.0,
        maximum=1.0,
    )
    dry_level: SliderConfig = SliderConfig(
        label="Чистый голос",
        info="Сколько исходного сухого голоса оставить в результате.",
        value=0.8,
        minimum=0.0,
        maximum=1.0,
    )
    damping: SliderConfig = SliderConfig(
        label="Мягкость хвоста",
        info="Насколько сильно приглушать высокие частоты в хвосте реверберации.",
        value=0.7,
        minimum=0.0,
        maximum=1.0,
    )
    main_gain: SliderConfig = SliderConfig.gain(
        label="Громкость основного голоса",
        info="Усиление для основной вокальной партии.",
    )
    inst_gain: SliderConfig = SliderConfig.gain(
        label="Громкость инструментала",
        info="Усиление для инструментала.",
    )
    backup_gain: SliderConfig = SliderConfig.gain(
        label="Громкость бэков",
        info="Усиление для бэк-вокала.",
    )


class SpeechGenerationConfig(GenerationConfig):
    """
    Common component configuration settings for speech generation tabs.

    Attributes
    ----------
    source_type : DropdownConfig
        Configuration settings for a source type dropdown component.
    source : TextboxConfig
        Configuration settings for an input source textbox component.
    edge_tts_voice : DropdownConfig
        Configuration settings for an Edge TTS voice dropdown
        component.
    n_octaves : SliderConfig
        Configuration settings for an octave pitch shift slider
        component.
    n_semitones : SliderConfig
        Configuration settings for a semitone pitch shift slider
        component.
    tts_pitch_shift : SliderConfig
        Configuration settings for a TTS pitch shift slider
        component.
    tts_speed_change : SliderConfig
        Configuration settings for a TTS speed change slider
        component.
    tts_volume_change : SliderConfig
        Configuration settings for a TTS volume change slider
        component.
    clean_voice : CheckboxConfig
        Configuration settings for a clean voice checkbox
        component.
    clean_strength : SliderConfig
        Configuration settings for a clean strength slider
        component.
    output_gain : GainSliderConfig
        Configuration settings for an output gain slider component.

    See Also
    --------
    GenerationConfig
        Parent model defining common component configuration settings
        for generation tabs.

    """

    source_type: DropdownConfig = DropdownConfig(
        label="Тип источника",
        info="Откуда брать текст или аудио для генерации речи.",
        value=SpeechSourceType.TEXT,
        choices=list(SpeechSourceType),
        type="index",
        exclude_value=True,
    )
    source: TextboxConfig = TextboxConfig(
        label="Текст для озвучки",
        info="Введите текст вручную или переключитесь на загрузку TXT-файла.",
        placeholder="Напишите здесь текст, который должен произнести голос…",
        lines=5,
        max_lines=12,
        value=None,
        exclude_value=True,
    )
    edge_tts_voice: DropdownConfig = DropdownConfig(
        label="Голос для исходной речи",
        info=(
            "Сначала этот голос прочитает текст, затем выбранная модель RVC "
            "преобразует его тембр. Начните со Светланы или Дмитрия."
        ),
        value=None,
        render=False,
        exclude_value=True,
    )
    n_octaves: SliderConfig = SliderConfig.octave_shift(
        label="Сдвиг по октавам",
        info=(
            "Количество октав, на которое смещается высота конвертированной речи."
            " 1 — мужской → женский, -1 — наоборот."
        ),
    )
    n_semitones: SliderConfig = SliderConfig.semitone_shift(
        label="Сдвиг по полутонам",
        info="Количество полутонов для смещения высоты конвертированной речи.",
    )
    tts_pitch_shift: SliderConfig = SliderConfig(
        label="Высота исходной TTS-речи",
        info=(
            "На сколько герц смещать высоту речи, созданной Edge TTS, ещё до"
            " конверсии."
        ),
        value=0,
        minimum=-100,
        maximum=100,
        step=1,
    )
    tts_speed_change: SliderConfig = SliderConfig(
        label="Темп исходной речи",
        info="Изменение скорости речи Edge TTS в процентах.",
        value=0,
        minimum=-50,
        maximum=100,
        step=1,
    )
    tts_volume_change: SliderConfig = SliderConfig(
        label="Громкость исходной речи",
        info="Процентное изменение громкости речи, сгенерированной Edge TTS.",
        value=0,
        minimum=-100,
        maximum=100,
        step=1,
    )
    clean_voice: CheckboxConfig = CheckboxConfig(
        label="Очистка конвертированного голоса",
        info="Применять ли шумоподавление к сконвертированной речи.",
        value=True,
        exclude_value=True,
    )
    clean_strength: SliderConfig = SliderConfig.clean_strength(visible=True)
    output_gain: SliderConfig = SliderConfig.gain(
        label="Громкость вывода",
        info="Усиление, применяемое к итоговой речи.<br><br>",
    )
