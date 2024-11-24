"""
Inspired by https://github.com/4ms/4ms-kicad-lib/blob/master/PCM/make_archive.sh
"""
import re
import os
import json

import shutil
import hashlib
import datetime

from pathlib import Path

# from git import Repo

import logging

logging.basicConfig(level=logging.INFO)

# repo = Repo(self.rorepo.working_tree_dir)

def iterate_minor_version(last_version: str) -> str:
    dotted_version = last_version.split(".")
    dotted_version[-1] = str(int(dotted_version[-1]) + 1)
    next_version = ".".join(dotted_version)
    logging.info(f"Upgrading {last_version}->{next_version}")
    return next_version

def get_metadata(path):
    metadata = {}
    metadata_path = os.path.join(path, "metadata.json")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"No metadata.json found at {path}")
    
    with open(metadata_path, 'r') as file:
        return json.load(file)

def save_metadata(path, metadata):
    metadata_path = os.path.join(path, "metadata.json")

    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)

def package_path(path) -> dict:
    # with ZipFile(os.path.join(".", f"{os.path.basename(path)}.zip"), 'w') as zip_object:
    shutil.make_archive(os.path.join("packages", os.path.basename(path)), 'zip', path)
    return os.path.join("packages", f"{path}.zip")

def sha256sum(filename) -> str:
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def package_library_submodule(path, download_url: str) -> dict:
    logging.info(f"Analysing {path}")

    metadata = get_metadata(path)

    # Just update it in place, assume it's a quick rebuild. Check the tags for the 
    # major version... maybe, thinking about the code later :O
    metadata["versions"][0]["version"] = iterate_minor_version(metadata["versions"][0]["version"])
    
    # save the package relevant metadata without the download information.
    save_metadata(path, metadata)

    packaged_path = package_path(path)
    metadata["versions"][0]["install_size"] = sum(file.stat().st_size for file in Path(path).rglob('*'))
    metadata["versions"][0]["download_size"] = os.path.getsize(packaged_path)
    metadata["versions"][0]['sha256'] = sha256sum(packaged_path)
    metadata["versions"][0]["download_url"] = f"{download_url}"
    
    return metadata

def update_packages(packages_json_path: str):
    packages = {
        "packages" : [
            package_library_submodule("PartyWagon112-KiCad-Library", "https://github.com/partywagon112/PartyWagon112-KiCad-PCM-Repository/raw/refs/heads/main/packages/PartyWagon112-KiCad-Library.zip")
        ]
    }

    with open(packages_json_path, 'w') as file:
        json.dump(packages, file, indent=4)

    os.stat(packages_json_path)

def update_repository(repository_json_path, packages_json_path):
    update_packages(packages_json_path)

    repository = {}
    
    with open(repository_json_path, 'r') as file:
        repository = json.load(file)

    timestamp = int(os.stat(packages_json_path).st_mtime)
    # repository["packages"]["sha256"] = sha256sum(packages_json_path)
    repository["packages"]["update_timestamp"] = int(timestamp)
    repository["packages"]["update_time_utc"] = str(datetime.datetime.fromtimestamp(timestamp))

    with open(repository_json_path, 'w') as file:
        json.dump(repository, file, indent=4)

update_repository("partywagon112_repository.json", "partywagon112_packages.json")