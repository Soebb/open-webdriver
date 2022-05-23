"""
Module to download the Chromium browser from the repo.
"""

import os
import subprocess
import sys
import zipfile

from download import download  # type: ignore

from open_webdriver.path import WDM_CHROMIUM_DIR


def _set_exe_permissions(start_dir: str) -> None:
    """Sets the permissions on the chromium executable."""
    if sys.platform == "win32":
        return
    for root, _, files in os.walk(start_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            os.chmod(path, 0o755)


def _unzip(zip_path: str) -> None:
    """Unzips a zip file."""

    if sys.platform == "linux":
        # sudo apt-get install p7zip-full
        print("Linux detected, using 7z tool")
        try:
            zip_name = os.path.basename(zip_path)
            cmd = f"7z x {zip_name}"
            print(f'Executing: "{cmd}"')
            stdout, stderr = subprocess.check_output(cmd, cwd=os.path.dirname(zip_path), shell=True)
            print(stdout)
        except subprocess.CalledProcessError:
            print("Failed to unzip with command line, falling back to python unzip")
    else:
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.testzip()
            zipf.extractall(os.path.dirname(zip_path))


def get_chromium_exe() -> str:
    """Fetches the chromium executable."""
    url_src = f"https://github.com/zackees/open-webdriver/raw/main/chromium/{sys.platform}.zip"
    platform_dir = os.path.join(WDM_CHROMIUM_DIR, sys.platform)
    print(f"WDM_CHROMIUM_DIR: {WDM_CHROMIUM_DIR}")
    finished_stamp = os.path.join(platform_dir, "finished")
    if not os.path.exists(finished_stamp):
        zip_dst = os.path.join(WDM_CHROMIUM_DIR, sys.platform + ".zip")
        print(f"Download {url_src} to {zip_dst}")
        download(url=url_src, path=zip_dst, kind="file", progressbar=True, replace=False)
        assert os.path.exists(zip_dst), f"{zip_dst} does not exist."
        print(f"Unzipping {zip_dst}")
        _unzip(zip_path=zip_dst)
        print(f"Fixing permissions {zip_dst}")
        _set_exe_permissions(platform_dir)
        # Touch file.
        print("Touching file.")
        with open(finished_stamp, encoding="utf-8", mode="w") as filed:
            filed.write("")
        print(f"Removing {zip_dst}")
        os.remove(zip_dst)
    exe_path = None
    if sys.platform == "win32":
        exe_path = os.path.join(platform_dir, "chrome.exe")
    elif sys.platform == "linux":
        exe_path = os.path.join(platform_dir, "chrome")
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")
    assert os.path.exists(exe_path), f"Chromium executable not found: {exe_path}"
    return exe_path


if __name__ == "__main__":
    print(get_chromium_exe())
