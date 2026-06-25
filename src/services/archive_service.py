import shutil
from pathlib import Path


ARCHIVE_DIR = Path(
    "data/archive"
)

ARCHIVE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def archive_resume(
        resume_path):

    resume_path = Path(
        resume_path
    )

    if not resume_path.exists():

        raise FileNotFoundError(
            f"Resume not found: {resume_path}"
        )

    destination = ARCHIVE_DIR / resume_path.name

    shutil.move(
        str(
            resume_path
        ),
        str(
            destination
        )
    )

    return destination