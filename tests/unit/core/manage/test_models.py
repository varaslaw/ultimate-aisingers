"""Unit tests for voice model management."""

from __future__ import annotations

from typing import TYPE_CHECKING

import zipfile
from pathlib import Path
from types import SimpleNamespace

from ultimate_rvc.core.manage.models import upload_voice_model

if TYPE_CHECKING:
    import pytest_mock


MODEL_BYTES = 2048


def _write_archive(path: Path, files: dict[str, bytes]) -> None:
    """Write a small zip archive with model files."""
    with zipfile.ZipFile(path, "w") as archive:
        for filename, payload in files.items():
            archive.writestr(filename, payload)


def _patch_voice_model_dir(
    mocker: pytest_mock.MockerFixture,
    voice_models_dir: Path,
) -> None:
    """Point voice model validation at a temporary directory."""
    mocker.patch("ultimate_rvc.core.common.VOICE_MODELS_DIR", voice_models_dir)
    mocker.patch("ultimate_rvc.core.manage.models.VOICE_MODELS_DIR", voice_models_dir)


def test_upload_voice_model_accepts_zip_with_model_files_in_root(
    tmp_path: Path,
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Upload a zip containing .pth and .index files at archive root."""
    voice_models_dir = tmp_path / "voice_models"
    _patch_voice_model_dir(mocker, voice_models_dir)
    archive_path = tmp_path / "singer.zip"
    _write_archive(
        archive_path,
        {
            "Singer.pth": b"p" * MODEL_BYTES,
            "Singer.index": b"i" * MODEL_BYTES,
        },
    )

    upload_voice_model([{"path": str(archive_path)}], "Singer")

    model_dir = voice_models_dir / "Singer"
    assert (model_dir / "Singer.pth").is_file()
    assert (model_dir / "Singer.index").is_file()


def test_upload_voice_model_flattens_nested_zip_model_files(
    tmp_path: Path,
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Upload a zip where model files are nested inside a folder."""
    voice_models_dir = tmp_path / "voice_models"
    _patch_voice_model_dir(mocker, voice_models_dir)
    archive_path = tmp_path / "nested.zip"
    _write_archive(
        archive_path,
        {
            "nested/Voice.pth": b"p" * MODEL_BYTES,
            "nested/Voice.index": b"i" * MODEL_BYTES,
            "nested/readme.txt": b"ignore me",
        },
    )

    upload_voice_model([SimpleNamespace(path=str(archive_path))], "Voice")

    model_dir = voice_models_dir / "Voice"
    assert (model_dir / "Voice.pth").is_file()
    assert (model_dir / "Voice.index").is_file()
    assert not (model_dir / "nested").exists()
