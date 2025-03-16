from pathlib import Path
from dynaconf import Dynaconf

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent

settings = Dynaconf(
    envvar_prefix="JUTIX",
    root_path=ROOT_DIR,
    settings_files=[
        # Load default settings
        f"{ROOT_DIR}/jutix/config/default_settings.toml",  # Always load default settings first
        "settings.toml",  # Then load user settings
        "settings.{env}.toml",  # Then environment specific
        ".secrets.toml",  # Finally load secrets
    ],
    environments=["default", "development", "production"],
    env="default",  # Set default environment
    load_dotenv=True,
    dotenv_path=f"{ROOT_DIR}/.env",
    merge_enabled=True
) 