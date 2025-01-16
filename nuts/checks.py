from django.core.checks import Warning, register
from pathlib import Path
from django.conf import settings


@register()
def check_env_file(app_configs, **kwargs):
    errors = []
    env_file = Path(settings.BASE_DIR) / ".env"

    if not env_file.exists():
        errors.append(
            Warning(
                "No .env file found",
                hint="Create a .env file based on .env.development.example",
                obj=settings,
                id="nuts.W001",
            )
        )
        return errors

    with open(env_file) as f:
        env_content = f.read()
        required_vars = ["DEBUG", "SECRET_KEY", "ALLOWED_HOSTS", "DATABASE_URL"]
        missing_vars = []

        for var in required_vars:
            if var + "=" not in env_content:
                missing_vars.append(var)

        if missing_vars:
            errors.append(
                Warning(
                    f"Missing required environment variables: {', '.join(missing_vars)}",
                    hint="Add these variables to your .env file",
                    obj=settings,
                    id="nuts.W002",
                )
            )

    return errors
