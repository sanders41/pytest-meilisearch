from __future__ import annotations

import shlex
import socket
import subprocess
from time import time
from types import TracebackType
from warnings import warn

import pytest
from meilisearch_python_sdk import Client
from meilisearch_python_sdk.errors import MeilisearchCommunicationError


class MeilisearchServer:  # pragma: no cover
    def __init__(
        self,
        url: str,
        port: int,
        meilisearch_version: str = "latest",
        start_timeout: int = 120,
        api_key: str | None = None,
    ) -> None:
        self.url = url
        self.port = port
        self.api_key = api_key
        self.meilisearch_version = meilisearch_version
        self.start_timeout = start_timeout
        self._container_id: str | None
        self._started = False

    def __enter__(self) -> MeilisearchServer:
        return self

    def __exit__(
        self,
        et: type[BaseException] | None,
        ev: type[BaseException] | None,
        traceback: TracebackType | None,
    ) -> None:
        self.stop()

    def start(self) -> None:
        """Start Meilisearch in a separate process."""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            split = self.url.split("//", 1)
            check_url = split[-1] if len(split) > 1 else split[0]
            check_url_split = check_url.split(":", 1)[0]
            if s.connect_ex((check_url_split, self.port)) == 0:
                warn(
                    f"Something already running on {check_url_split}:{self.port}. Skipping Meiliserch start"
                )
                return

        command = f"docker run --rm -d -p {self.port}:{self.port} getmeili/meilisearch:{self.meilisearch_version} meilisearch --no-analytics"
        if self.api_key:
            command = f"{command} --master-key={self.api_key}"

        try:
            process = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                check=True,
                timeout=self.start_timeout,
            )
            if process.returncode != 0:
                if process.stdout:
                    self._container_id = process.stdout
                    self.stop()
                if process.stderr:
                    pytest.fail(f"Failed to start Meilisearch: {process.stderr}")
                pytest.fail("Failed to start Meilisearch")
        except subprocess.TimeoutExpired:
            pytest.fail(
                f"Starting Meilisearch exceded the maximum allowed time of {self.start_timeout} seconds"
            )
        except Exception as e:
            pytest.fail(f"An error occurred while starting Meilisearch: {e}")

        self._container_id = process.stdout
        self._started = True

        start = time()
        while True:
            elapsed_time = time() - start
            if elapsed_time > self.start_timeout:
                pytest.fail(
                    f"Failed to start the Meilisearch server after {self.start_timeout} seconds"
                )
            if self._is_ready():
                break

    def _is_ready(self) -> bool:
        client = Client(self.url, self.api_key)
        try:
            status = client.health().status
            if status == "available":
                return True
        except MeilisearchCommunicationError:
            return False

        return False

    def stop(self) -> None:
        if self._started and self._container_id:
            command = f"docker stop {self._container_id}"
            process = subprocess.run(shlex.split(command), capture_output=True, text=True)
            if process.returncode != 0:
                if process.stderr:
                    print(f"Failed to start Meilisearch: {process.stderr}")  # noqa: T201
