"""
Web application for the Ultimate RVC project.

Each tab of the application is defined in its own module in the
`web/tabs` directory. Components that are accessed across multiple
tabs are passed as arguments to the render functions in the respective
modules.
"""

from __future__ import annotations

from typing import Annotated

import base64
import os
from pathlib import Path

import gradio as gr

import typer

from ultimate_rvc.common import AUDIO_DIR, MODELS_DIR, TEMP_DIR
from ultimate_rvc.core.generate.song_cover import get_named_song_dirs
from ultimate_rvc.core.manage.audio import (
    get_saved_output_audio,
    get_saved_speech_audio,
)
from ultimate_rvc.core.manage.config import get_config_names, load_config
from ultimate_rvc.core.manage.models import (
    get_custom_embedder_model_names,
    get_voice_model_names,
)
from ultimate_rvc.web.common import initialize_dropdowns
from ultimate_rvc.web.config.main import TotalConfig
from ultimate_rvc.web.tabs.generate.song_cover.multi_step_generation import (
    render as render_song_cover_multi_step_tab,
)
from ultimate_rvc.web.tabs.generate.song_cover.one_click_generation import (
    render as render_song_cover_one_click_tab,
)
from ultimate_rvc.web.tabs.generate.speech.multi_step_generation import (
    render as render_speech_multi_step_tab,
)
from ultimate_rvc.web.tabs.generate.speech.one_click_generation import (
    render as render_speech_one_click_tab,
)
from ultimate_rvc.web.tabs.manage.audio import render as render_audio_tab
from ultimate_rvc.web.tabs.manage.models import render as render_models_tab
from ultimate_rvc.web.tabs.manage.settings import render as render_settings_tab
from ultimate_rvc.web.tts import get_edge_tts_voice_choices

config_name = os.environ.get("URVC_CONFIG")
cookiefile = os.environ.get("YT_COOKIEFILE")
total_config = load_config(config_name, TotalConfig) if config_name else TotalConfig()


def render_app() -> gr.Blocks:
    """
    Render the AISingers web application.

    Returns
    -------
    gr.Blocks
        The rendered web application.

    """
    hero_path = Path(__file__).parent / "assets" / "aisingers-hero.png"
    hero_image = base64.b64encode(hero_path.read_bytes()).decode("ascii")

    css = """
    :root {
        --ais-bg: #0e0b12;
        --ais-surface: rgba(24, 19, 29, .94);
        --ais-surface-raised: #211925;
        --ais-input: #100c14;
        --ais-border: rgba(226, 181, 206, .16);
        --ais-text: #fff7fb;
        --ais-muted: #c8adbc;
        --ais-accent: #d875a8;
        --ais-accent-strong: #ad4f7e;
        --ais-mint: #8bc8bb;
        --ais-hero: linear-gradient(120deg, #251824, #18121d 58%, #15121b);
    }
    :root, .gradio-container {
        --background-fill-primary: #0e0b12 !important;
        --background-fill-secondary: #17111b !important;
        --body-background-fill: #0e0b12 !important;
        --body-text-color: #fff7fb !important;
        --body-text-color-subdued: #c8adbc !important;
        --block-background-fill: #18131d !important;
        --block-border-color: #433040 !important;
        --block-label-text-color: #f8eaf2 !important;
        --block-info-text-color: #c8adbc !important;
        --block-title-text-color: #fff7fb !important;
        --border-color-primary: #433040 !important;
        --border-color-accent: #765168 !important;
        --color-accent: #d875a8 !important;
        --color-accent-soft: #3a2030 !important;
        --input-background-fill: #100c14 !important;
        --input-background-fill-focus: #1d1521 !important;
        --input-background-fill-hover: #1d1621 !important;
        --input-border-color: #4b3446 !important;
        --input-border-color-focus: #d875a8 !important;
        --input-text-color: #fff7fb !important;
        --input-placeholder-color: #896f7e !important;
        --panel-background-fill: #18131d !important;
        --checkbox-label-background-fill: #17121c !important;
        --checkbox-label-background-fill-hover: #251a27 !important;
        --checkbox-label-background-fill-selected: #4a2238 !important;
        --checkbox-label-border-color: #533a4e !important;
        --checkbox-label-text-color: #f4e3ec !important;
        --checkbox-label-text-color-selected: #ffffff !important;
        --button-primary-background-fill: #ad4f7e !important;
        --button-primary-background-fill-hover: #c15d8d !important;
        --button-primary-border-color: #d875a8 !important;
        --button-primary-text-color: #ffffff !important;
        --button-secondary-background-fill: #251b28 !important;
        --button-secondary-background-fill-hover: #352436 !important;
        --button-secondary-border-color: #63445d !important;
        --button-secondary-text-color: #fff3f8 !important;
        --slider-color: #d875a8 !important;
    }
    html[data-ais-theme="light"] {
        --ais-bg: #f4e8ee;
        --ais-surface: rgba(255, 248, 251, .92);
        --ais-surface-raised: #fff8fb;
        --ais-input: #fffafc;
        --ais-border: rgba(126, 68, 101, .19);
        --ais-text: #33222d;
        --ais-muted: #765d6b;
        --ais-accent: #b94f82;
        --ais-accent-strong: #963b69;
        --ais-mint: #0f766e;
        --ais-hero: linear-gradient(120deg, #efd3df, #faedf3 58%, #eee5f2);
    }
    html[data-ais-theme="light"] .gradio-container {
        --background-fill-primary: #f4e8ee !important;
        --background-fill-secondary: #ecdae3 !important;
        --body-background-fill: #f4e8ee !important;
        --body-text-color: #33222d !important;
        --body-text-color-subdued: #765d6b !important;
        --block-background-fill: #fff8fb !important;
        --block-border-color: #dbc1ce !important;
        --block-label-text-color: #48313e !important;
        --block-info-text-color: #765d6b !important;
        --block-title-text-color: #33222d !important;
        --border-color-primary: #dbc1ce !important;
        --border-color-accent: #c18aa5 !important;
        --input-background-fill: #fffafc !important;
        --input-background-fill-focus: #fff5f9 !important;
        --input-background-fill-hover: #f9edf3 !important;
        --input-border-color: #d2afc0 !important;
        --input-text-color: #33222d !important;
        --panel-background-fill: #fff8fb !important;
        --checkbox-label-background-fill: #fff8fb !important;
        --checkbox-label-background-fill-hover: #f8e7ef !important;
        --checkbox-label-background-fill-selected: #efd2df !important;
        --checkbox-label-border-color: #d8b6c6 !important;
        --checkbox-label-text-color: #48313e !important;
        --checkbox-label-text-color-selected: #702b50 !important;
        --button-secondary-background-fill: #f6e4ec !important;
        --button-secondary-background-fill-hover: #efd3df !important;
        --button-secondary-border-color: #d2a7bb !important;
        --button-secondary-text-color: #4b2f3e !important;
    }

    .gradio-container {
        background:
            radial-gradient(circle at 16% -10%, rgba(173, 79, 126, .18), transparent 28rem),
            radial-gradient(circle at 88% 10%, rgba(111, 87, 146, .10), transparent 25rem),
            var(--ais-bg) !important;
        color: var(--ais-text) !important;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .gradio-container .main { max-width: 1480px !important; padding: 0 24px 42px !important; }
    .gradio-container .prose, .gradio-container label, .gradio-container .wrap,
    .gradio-container .block-title, .gradio-container .label-wrap,
    .gradio-container .label-wrap span, .gradio-container .accordion .label-wrap span,
    .gradio-container .accordion .label-wrap button, .gradio-container .info,
    .gradio-container .description, .gradio-container .description p,
    .gradio-container .prose p, .gradio-container .prose strong {
        color: var(--ais-text) !important;
    }
    .gradio-container .info, .gradio-container .description, .gradio-container .description p {
        color: var(--ais-muted) !important;
    }
    .gradio-container .block, .gradio-container .form, .gradio-container .panel {
        border-color: var(--ais-border) !important;
    }
    .gradio-container .form, .gradio-container .block.gr-box, .gradio-container .accordion,
    .gradio-container .group, .gradio-container .block {
        background: var(--ais-surface) !important;
        border-radius: 18px !important;
    }
    .gradio-container input, .gradio-container textarea, .gradio-container .wrap-inner,
    .gradio-container .wrap, .gradio-container .block input,
    .gradio-container .block textarea {
        background: var(--ais-input) !important;
        color: var(--ais-text) !important;
        border-color: var(--ais-border) !important;
        border-radius: 12px !important;
    }
    .gradio-container .accordion > .label-wrap { padding: 12px 16px !important; }
    .gradio-container .accordion > .label-wrap span { font-weight: 700 !important; }
    .gradio-container .checkbox-group label, .gradio-container .radio-group label,
    .gradio-container .gradio-radio label, .gradio-container .gradio-checkbox label {
        border-radius: 12px !important;
    }
    .gradio-container .wrap:has(input[type="radio"]) {
        background: transparent !important; border: 0 !important; gap: 8px !important;
    }
    .gradio-container label:has(input[type="radio"]) {
        position: relative; min-height: 44px; padding: 10px 42px 10px 14px !important;
        border: 1px solid var(--ais-border) !important;
        background: var(--ais-input) !important; transition: .18s ease;
    }
    .gradio-container label:has(input[type="radio"]) input { opacity: 0 !important; position: absolute !important; }
    .gradio-container label:has(input[type="radio"]:checked) {
        border-color: var(--ais-accent) !important;
        background: color-mix(in srgb, var(--ais-accent) 22%, var(--ais-surface)) !important;
        box-shadow: 0 0 0 2px color-mix(in srgb, var(--ais-accent) 18%, transparent);
    }
    .gradio-container label:has(input[type="radio"]:checked)::after {
        content: "✓"; position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
        display: grid; place-items: center; width: 22px; height: 22px; border-radius: 999px;
        background: var(--ais-accent-strong); color: #fff; font-weight: 900; font-size: 13px;
    }
    .gradio-container input, .gradio-container textarea { caret-color: var(--ais-mint); }
    .gradio-container .tab-nav { gap: 8px; border: 0 !important; margin: 0 0 20px; }
    .gradio-container .tab-nav button {
        border: 1px solid transparent !important; border-radius: 12px !important;
        color: var(--ais-muted) !important; font-weight: 650 !important; padding: 10px 16px !important;
    }
    .gradio-container .tab-nav button.selected {
        background: rgba(167, 139, 250, .15) !important;
        border-color: rgba(167, 139, 250, .45) !important; color: var(--ais-text) !important;
    }
    .gradio-container button.primary {
        background: linear-gradient(135deg, var(--ais-accent-strong), #75528f) !important;
        border: 0 !important; box-shadow: 0 10px 24px rgba(104, 46, 77, .22);
    }
    .advanced-settings-button, .advanced-settings-button button {
        min-height: 58px !important; width: 100% !important; font-size: 1rem !important;
        font-weight: 800 !important; border: 1px solid var(--ais-accent) !important;
        border-radius: 15px !important;
        background: color-mix(in srgb, var(--ais-accent) 15%, var(--ais-surface)) !important;
        color: var(--ais-text) !important;
        box-shadow: 0 8px 22px rgba(80, 37, 61, .16) !important;
    }
    .advanced-settings-button:hover, .advanced-settings-button button:hover {
        transform: translateY(-1px); background: color-mix(in srgb, var(--ais-accent) 24%, var(--ais-surface)) !important;
    }
    #aisingers-header { margin: 28px 0 22px; }
    .ais-hero {
        position: relative; overflow: hidden; min-height: 280px;
        display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(280px, .85fr);
        gap: 20px; align-items: center; padding: 32px;
        border: 1px solid var(--ais-border); border-radius: 26px; background: var(--ais-hero);
    }
    .ais-hero-copy { position: relative; z-index: 2; }
    .ais-hero-art { width: 100%; max-height: 265px; object-fit: contain; filter: drop-shadow(0 18px 34px rgba(44, 19, 34, .28)); }
    .ais-kicker { color: var(--ais-mint); font-size: .76rem; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
    .ais-hero h1 { margin: 8px 0; color: var(--ais-text) !important; font-size: clamp(2rem, 5vw, 3.6rem); line-height: 1; letter-spacing: -.055em; }
    .ais-hero p { max-width: 650px; margin: 0; color: var(--ais-muted); font-size: 1rem; }
    .ais-community { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
    .ais-community a {
        display: flex; align-items: center; gap: 10px; min-width: 220px; padding: 11px 14px;
        border: 1px solid var(--ais-border); border-radius: 14px;
        background: color-mix(in srgb, var(--ais-surface) 84%, transparent);
        color: var(--ais-text) !important; text-decoration: none !important;
    }
    .ais-community a:hover { border-color: var(--ais-accent) !important; transform: translateY(-1px); }
    .ais-community strong { display: block; color: var(--ais-text); font-size: .9rem; }
    .ais-community small { display: block; color: var(--ais-muted); font-size: .76rem; }
    .ais-community-icon { font-size: 1.25rem; }
    #theme-bar { margin: 0 0 20px; align-items: center; min-height: 42px; }
    #theme-selector { margin-left: auto; max-width: 230px; }
    #theme-selector label { color: var(--ais-muted) !important; font-size: .86rem; }
    #theme-selector .wrap { background: transparent !important; border: 0 !important; }
    .gradio-container .theme-toggle label { border-radius: 999px !important; }
    .ais-section-title { margin: 8px 0 16px; }
    .ais-section-title h2 { margin: 0 0 4px; font-size: 1.25rem; }
    .ais-section-title p { margin: 0; color: var(--ais-muted); }
    .tts-voice-picker {
        padding: 18px !important; border: 1px solid color-mix(in srgb, var(--ais-accent) 42%, var(--ais-border)) !important;
        border-radius: 18px !important;
        background: linear-gradient(135deg, color-mix(in srgb, var(--ais-accent) 10%, var(--ais-surface)), var(--ais-surface)) !important;
    }
    .tts-picker-heading { display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 14px; margin-bottom: 12px; }
    .tts-picker-heading strong { color: var(--ais-text); font-size: 1rem; }
    .tts-picker-heading span, .tts-picker-note { color: var(--ais-muted); font-size: .82rem; }
    .tts-picker-note { margin-top: 8px; line-height: 1.5; }
    #generate-tab-button, #manage-tab-button, #audio-tab-button, #settings-tab-button { font-weight: 750 !important; }
    @media (max-width: 680px) {
        .ais-hero { padding: 22px; display: block; }
        .ais-hero-art { display: none; }
        .ais-community a { min-width: 100%; }
        .gradio-container .tab-nav { overflow-x: auto; }
    }
    """
    cache_delete_frequency = 86400  # every 24 hours check for files to delete
    cache_delete_cutoff = 86400  # and delete files older than 24 hours

    theme_switch_js = """
    (theme) => {
        document.documentElement.dataset.aisTheme = theme === "Светлая" ? "light" : "dark";
        return [];
    }
    """
    with gr.Blocks(
        title="AISingers",
        # The bundled theme is intentionally neutral; all visual tokens are
        # defined above so the dark/light switch does not inherit the former
        # pink theme's low-contrast text colours.
        theme=gr.themes.Base(),
        css=css,
        delete_cache=(cache_delete_frequency, cache_delete_cutoff),
    ) as app:
        gr.HTML(
            f"""
            <section id="aisingers-header" class="ais-hero">
              <div class="ais-hero-copy">
                <div class="ais-kicker">AI voice studio</div>
                <h1>AISingers</h1>
                <p>Создавайте каверы и речь в понятном рабочем процессе — от источника до готового аудио.</p>
                <div class="ais-community">
                  <a href="https://t.me/aisingers" target="_blank" rel="noopener noreferrer">
                    <span class="ais-community-icon">✦</span>
                    <span><strong>Наш Telegram-канал</strong><small>Новости и обновления AISingers</small></span>
                  </a>
                  <a href="https://t.me/AIsingers_bot" target="_blank" rel="noopener noreferrer">
                    <span class="ais-community-icon">◉</span>
                    <span><strong>Создать голосового бота</strong><small>Попробуйте в @AIsingers_bot</small></span>
                  </a>
                </div>
              </div>
              <img class="ais-hero-art" src="data:image/png;base64,{hero_image}" alt="Микрофон и звуковые волны AISingers" />
            </section>
            """,
        )
        with gr.Row(elem_id="theme-bar"):
            gr.HTML("<span class='ais-kicker'>Рабочее пространство</span>")
            theme_switch = gr.Radio(
                choices=["Тёмная", "Светлая"],
                value="Тёмная",
                label="Оформление",
                container=False,
                elem_id="theme-selector",
                elem_classes=["theme-toggle"],
            )
        theme_switch.input(
            fn=None,
            inputs=theme_switch,
            outputs=None,
            js=theme_switch_js,
            show_progress="hidden",
        )
        for component_config in [
            total_config.song.one_click.voice_model,
            total_config.song.one_click.cached_song,
            total_config.song.one_click.custom_embedder_model,
            total_config.song.multi_step.voice_model,
            total_config.song.multi_step.cached_song,
            total_config.song.multi_step.custom_embedder_model,
            total_config.song.multi_step.song_dirs.separate_audio,
            total_config.song.multi_step.song_dirs.convert_vocals,
            total_config.song.multi_step.song_dirs.postprocess_vocals,
            total_config.song.multi_step.song_dirs.pitch_shift_background,
            total_config.song.multi_step.song_dirs.mix,
            total_config.speech.one_click.edge_tts_voice,
            total_config.speech.one_click.voice_model,
            total_config.speech.one_click.custom_embedder_model,
            total_config.speech.multi_step.edge_tts_voice,
            total_config.speech.multi_step.voice_model,
            total_config.speech.multi_step.custom_embedder_model,
            total_config.management.audio.intermediate,
            total_config.management.audio.speech,
            total_config.management.audio.output,
            total_config.management.model.voices,
            total_config.management.model.embedders,
            total_config.management.settings.load_config_name,
            total_config.management.settings.delete_config_names,
        ]:
            component_config.instantiate()
        # main tab
        with gr.Tab("Создать", elem_id="generate-tab"):
            gr.HTML(
                """
                <div class="ais-section-title">
                  <h2>Создание</h2>
                  <p>Быстрый режим — для результата сразу. Режим по шагам — для полного контроля над дорожками.</p>
                </div>
                """,
            )
            with gr.Tab("Каверы"):
                render_song_cover_one_click_tab(total_config, cookiefile)
                render_song_cover_multi_step_tab(total_config, cookiefile)
            with gr.Tab("Озвучка TTS"):
                render_speech_one_click_tab(total_config)
                render_speech_multi_step_tab(total_config)
        with gr.Tab("Загрузить модель", elem_id="manage-tab"):
            gr.HTML(
                """
                <div class="ais-section-title">
                  <h2>Загрузить модель</h2>
                  <p>Добавьте голос в формате ZIP или файлами .pth + .index. После загрузки он сразу появится в генераторе.</p>
                </div>
                """,
            )
            render_models_tab(total_config)
        with gr.Tab("Мои файлы", elem_id="audio-tab"):
            gr.HTML(
                """
                <div class="ais-section-title">
                  <h2>Аудиотека</h2>
                  <p>Управляйте промежуточными дорожками, озвучкой и готовыми результатами.</p>
                </div>
                """,
            )
            render_audio_tab(total_config)
        with gr.Tab("Параметры", elem_id="settings-tab"):
            gr.HTML(
                """
                <div class="ais-section-title">
                  <h2>Рабочее пространство</h2>
                  <p>Сохраняйте удачные настройки в конфигурации и очищайте временные файлы при необходимости.</p>
                </div>
                """,
            )
            render_settings_tab(total_config)

        app.load(
            _init_dropdowns,
            outputs=[
                total_config.speech.one_click.edge_tts_voice.instance,
                total_config.speech.multi_step.edge_tts_voice.instance,
                total_config.song.one_click.voice_model.instance,
                total_config.song.multi_step.voice_model.instance,
                total_config.speech.one_click.voice_model.instance,
                total_config.speech.multi_step.voice_model.instance,
                total_config.management.model.voices.instance,
                total_config.song.one_click.custom_embedder_model.instance,
                total_config.song.multi_step.custom_embedder_model.instance,
                total_config.speech.one_click.custom_embedder_model.instance,
                total_config.speech.multi_step.custom_embedder_model.instance,
                total_config.management.model.embedders.instance,
                total_config.song.one_click.cached_song.instance,
                total_config.song.multi_step.cached_song.instance,
                total_config.song.multi_step.song_dirs.separate_audio.instance,
                total_config.song.multi_step.song_dirs.convert_vocals.instance,
                total_config.song.multi_step.song_dirs.postprocess_vocals.instance,
                total_config.song.multi_step.song_dirs.pitch_shift_background.instance,
                total_config.song.multi_step.song_dirs.mix.instance,
                total_config.management.audio.intermediate.instance,
                total_config.management.audio.speech.instance,
                total_config.management.audio.output.instance,
                total_config.management.settings.load_config_name.instance,
                total_config.management.settings.delete_config_names.instance,
            ],
            show_progress="hidden",
        )
    return app


def _init_dropdowns() -> list[gr.Dropdown]:
    """
    Initialize the AISingers web application by updating the choices
    and default values of non-static dropdown components.

    Returns
    -------
    tuple[gr.Dropdown, ...]
        A tuple of gr.Dropdown components with updated choices and
        default values.

    """
    # Initialize model dropdowns
    edge_tts_models = initialize_dropdowns(
        get_edge_tts_voice_choices,
        2,
        "ru-RU-SvetlanaNeural",
        range(2),
    )
    voice_models = initialize_dropdowns(
        get_voice_model_names,
        5,
        value_indices=range(4),
    )
    custom_embedder_models = initialize_dropdowns(
        get_custom_embedder_model_names,
        5,
        value_indices=range(4),
    )
    song_dirs = initialize_dropdowns(
        get_named_song_dirs,
        8,
        value_indices=range(7),
    )
    speech_delete = gr.Dropdown(get_saved_speech_audio())
    output_delete = gr.Dropdown(get_saved_output_audio())
    configs = initialize_dropdowns(get_config_names, 2, value_indices=range(1))
    return [
        *edge_tts_models,
        *voice_models,
        *custom_embedder_models,
        *song_dirs,
        speech_delete,
        output_delete,
        *configs,
    ]


app = render_app()
app_wrapper = typer.Typer()


@app_wrapper.command()
def start_app(
    share: Annotated[
        bool,
        typer.Option("--share", "-s", help="Enable sharing"),
    ] = False,
    listen: Annotated[
        bool,
        typer.Option(
            "--listen",
            "-l",
            help="Make the web application reachable from your local network.",
        ),
    ] = False,
    listen_host: Annotated[
        str | None,
        typer.Option(
            "--listen-host",
            "-h",
            help="The hostname that the server will use.",
        ),
    ] = None,
    listen_port: Annotated[
        int | None,
        typer.Option(
            "--listen-port",
            "-p",
            help="The listening port that the server will use.",
        ),
    ] = None,
    ssr_mode: Annotated[
        bool,
        typer.Option(
            "--ssr-mode",
            help="Enable server-side rendering mode.",
        ),
    ] = False,
) -> None:
    """Run the AISingers web application."""
    os.environ["GRADIO_TEMP_DIR"] = str(TEMP_DIR)
    gr.set_static_paths([MODELS_DIR, AUDIO_DIR])
    app.queue()
    app.launch(
        share=share,
        server_name=(None if not listen else (listen_host or "0.0.0.0")),  # noqa: S104
        server_port=listen_port,
        ssr_mode=ssr_mode,
    )


if __name__ == "__main__":
    app_wrapper()
