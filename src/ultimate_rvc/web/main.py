"""
Web application for the Ultimate RVC project.

Each tab of the application is defined in its own module in the
`web/tabs` directory. Components that are accessed across multiple
tabs are passed as arguments to the render functions in the respective
modules.
"""

from __future__ import annotations

from typing import Annotated

import os
from pathlib import Path

import gradio as gr

import typer

from ultimate_rvc.common import AUDIO_DIR, MODELS_DIR, TEMP_DIR
from ultimate_rvc.core.generate.song_cover import get_named_song_dirs
from ultimate_rvc.core.generate.speech import get_edge_tts_voice_names
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
    css = """
    :root {
        --ais-bg: #090b14;
        --ais-surface: rgba(18, 22, 38, .86);
        --ais-surface-raised: #191f33;
        --ais-input: rgba(7, 10, 21, .72);
        --ais-border: rgba(196, 206, 255, .13);
        --ais-text: #f6f7ff;
        --ais-muted: #aab2cd;
        --ais-accent: #a78bfa;
        --ais-accent-strong: #7c3aed;
        --ais-mint: #5eead4;
        --ais-hero: linear-gradient(120deg, rgba(167, 139, 250, .15), rgba(18, 22, 38, .92) 50%, rgba(45, 212, 191, .08));
    }
    :root, .gradio-container {
        --background-fill-primary: #070912 !important;
        --background-fill-secondary: #0d1322 !important;
        --body-background-fill: #070912 !important;
        --body-text-color: #f5f7ff !important;
        --body-text-color-subdued: #9ba9c7 !important;
        --block-background-fill: #10182a !important;
        --block-border-color: #293a5d !important;
        --block-label-text-color: #e6edff !important;
        --block-info-text-color: #9ba9c7 !important;
        --block-title-text-color: #f5f7ff !important;
        --border-color-primary: #293a5d !important;
        --border-color-accent: #40577f !important;
        --color-accent: #a855f7 !important;
        --color-accent-soft: #27204a !important;
        --input-background-fill: #080d19 !important;
        --input-background-fill-focus: #121c31 !important;
        --input-background-fill-hover: #10182a !important;
        --input-border-color: #2d4168 !important;
        --input-border-color-focus: #a855f7 !important;
        --input-text-color: #f5f7ff !important;
        --input-placeholder-color: #657493 !important;
        --panel-background-fill: #10182a !important;
        --checkbox-label-background-fill: #10182a !important;
        --checkbox-label-background-fill-hover: #17233b !important;
        --checkbox-label-background-fill-selected: #261b4a !important;
        --checkbox-label-border-color: #31476f !important;
        --checkbox-label-text-color: #dbe7ff !important;
        --checkbox-label-text-color-selected: #ffffff !important;
        --button-primary-background-fill: #7c3aed !important;
        --button-primary-background-fill-hover: #9333ea !important;
        --button-primary-border-color: #a855f7 !important;
        --button-primary-text-color: #ffffff !important;
        --button-secondary-background-fill: #18243b !important;
        --button-secondary-background-fill-hover: #243454 !important;
        --button-secondary-border-color: #3a527d !important;
        --button-secondary-text-color: #e6edff !important;
        --slider-color: #a855f7 !important;
    }
    html[data-ais-theme="light"] {
        --ais-bg: #f7f8ff;
        --ais-surface: rgba(255, 255, 255, .88);
        --ais-surface-raised: #ffffff;
        --ais-input: #ffffff;
        --ais-border: rgba(59, 70, 120, .16);
        --ais-text: #19213b;
        --ais-muted: #5c6682;
        --ais-accent: #7c3aed;
        --ais-accent-strong: #6d28d9;
        --ais-mint: #0f766e;
        --ais-hero: linear-gradient(120deg, rgba(167, 139, 250, .22), rgba(255, 255, 255, .95) 50%, rgba(45, 212, 191, .16));
    }
    html[data-ais-theme="light"] .gradio-container {
        --background-fill-primary: #f6f7ff !important;
        --background-fill-secondary: #edf0ff !important;
        --body-background-fill: #f6f7ff !important;
        --body-text-color: #17203b !important;
        --body-text-color-subdued: #5f6b87 !important;
        --block-background-fill: #ffffff !important;
        --block-border-color: #d7ddef !important;
        --block-label-text-color: #273451 !important;
        --block-info-text-color: #5f6b87 !important;
        --block-title-text-color: #17203b !important;
        --border-color-primary: #d7ddef !important;
        --border-color-accent: #adb8d5 !important;
        --input-background-fill: #ffffff !important;
        --input-background-fill-focus: #ffffff !important;
        --input-background-fill-hover: #f6f7ff !important;
        --input-border-color: #bdc7e1 !important;
        --input-text-color: #17203b !important;
        --panel-background-fill: #ffffff !important;
        --checkbox-label-background-fill: #ffffff !important;
        --checkbox-label-background-fill-hover: #f0edff !important;
        --checkbox-label-background-fill-selected: #ede9fe !important;
        --checkbox-label-border-color: #cbd4eb !important;
        --checkbox-label-text-color: #273451 !important;
        --checkbox-label-text-color-selected: #4c1d95 !important;
        --button-secondary-background-fill: #eef1fb !important;
        --button-secondary-background-fill-hover: #e0e6f6 !important;
        --button-secondary-border-color: #c5cfe7 !important;
        --button-secondary-text-color: #273451 !important;
    }

    .gradio-container {
        background:
            radial-gradient(circle at 16% -10%, rgba(124, 58, 237, .25), transparent 28rem),
            radial-gradient(circle at 88% 10%, rgba(45, 212, 191, .12), transparent 25rem),
            var(--ais-bg) !important;
        color: var(--ais-text) !important;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .gradio-container .prose, .gradio-container label, .gradio-container .wrap { color: var(--ais-text) !important; }
    .gradio-container .block, .gradio-container .form, .gradio-container .panel {
        border-color: var(--ais-border) !important;
    }
    .gradio-container .form, .gradio-container .block.gr-box, .gradio-container .accordion {
        background: var(--ais-surface) !important;
        border-radius: 16px !important;
    }
    .gradio-container input, .gradio-container textarea, .gradio-container .wrap-inner {
        background: var(--ais-input) !important;
        color: var(--ais-text) !important;
        border-color: var(--ais-border) !important;
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
        background: linear-gradient(135deg, var(--ais-accent-strong), #2563eb) !important;
        border: 0 !important; box-shadow: 0 12px 28px rgba(124, 58, 237, .28);
    }
    #aisingers-header { margin: 28px 0 22px; }
    .ais-hero {
        display: flex; justify-content: space-between; gap: 24px; align-items: end;
        padding: 30px; border: 1px solid var(--ais-border); border-radius: 22px;
        background: var(--ais-hero);
    }
    .ais-kicker { color: var(--ais-mint); font-size: .76rem; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
    .ais-hero h1 { margin: 8px 0; color: var(--ais-text) !important; font-size: clamp(2rem, 5vw, 3.6rem); line-height: 1; letter-spacing: -.055em; }
    .ais-hero p { max-width: 650px; margin: 0; color: var(--ais-muted); font-size: 1rem; }
    .ais-status { padding: 9px 12px; white-space: nowrap; border: 1px solid rgba(94, 234, 212, .24); border-radius: 999px; color: var(--ais-mint); font-size: .85rem; }
    #theme-bar { margin: -14px 0 20px; align-items: center; }
    #theme-selector { margin-left: auto; max-width: 230px; }
    #theme-selector label { color: var(--ais-muted) !important; font-size: .86rem; }
    #theme-selector .wrap { background: transparent !important; border: 0 !important; }
    .gradio-container .theme-toggle label { border-radius: 999px !important; }
    .ais-section-title { margin: 8px 0 16px; }
    .ais-section-title h2 { margin: 0 0 4px; font-size: 1.25rem; }
    .ais-section-title p { margin: 0; color: var(--ais-muted); }
    #generate-tab-button, #manage-tab-button, #audio-tab-button, #settings-tab-button { font-weight: 750 !important; }
    @media (max-width: 680px) {
        .ais-hero { padding: 22px; display: block; }
        .ais-status { display: inline-block; margin-top: 18px; }
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
        theme=gr.Theme.load(str(Path(__file__).parent / "config/theme.json")),
        css=css,
        delete_cache=(cache_delete_frequency, cache_delete_cutoff),
    ) as app:
        gr.HTML(
            """
            <section id="aisingers-header" class="ais-hero">
              <div>
                <div class="ais-kicker">AI voice studio</div>
                <h1>AISingers</h1>
                <p>Создавайте каверы и речь в понятном рабочем процессе — от источника до готового аудио.</p>
              </div>
              <div class="ais-status">● Локальная студия</div>
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
            with gr.Tab("Озвучка"):
                render_speech_one_click_tab(total_config)
                render_speech_multi_step_tab(total_config)
        with gr.Tab("Библиотека моделей", elem_id="manage-tab"):
            gr.HTML(
                """
                <div class="ais-section-title">
                  <h2>Голоса и эмбеддеры</h2>
                  <p>Скачивайте, добавляйте и очищайте модели. Новые голоса сразу появятся в генераторе.</p>
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
        get_edge_tts_voice_names,
        2,
        "en-US-ChristopherNeural",
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
