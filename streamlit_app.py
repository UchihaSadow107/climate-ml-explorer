import os
import runpy
import sys
import tempfile
import zipfile
from pathlib import Path

import streamlit as st


@st.cache_resource
def extract_project():
    archive_path = Path(__file__).resolve().parent / "climate-ml-project.zip"
    project_root = Path(tempfile.mkdtemp(prefix="climate-ml-explorer-")).resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            destination = (project_root / member.filename).resolve()
            if os.path.commonpath((project_root, destination)) != str(project_root):
                raise ValueError("Project archive contains an invalid file path.")
        archive.extractall(project_root)

    app_path = project_root / "app.py"
    if not app_path.is_file():
        raise FileNotFoundError("The project archive does not contain app.py.")
    return project_root


project_root = extract_project()
sys.path.insert(0, str(project_root))
runpy.run_path(str(project_root / "app.py"), run_name="__main__")
