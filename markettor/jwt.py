from datetime import datetime, timedelta, UTC
from enum import Enum
from typing import Any

import jwt
from django.conf import settings


class MarkettorJwtAudience(Enum):
    UNSUBSCRIBE = "markettor:unsubscribe"
    EXPORTED_ASSET = "markettor:exported_asset"
    IMPERSONATED_USER = "markettor:impersonted_user"  # This is used by background jobs on behalf of the user e.g. exports
    LIVESTREAM = "markettor:livestream"


def encode_jwt(payload: dict, expiry_delta: timedelta, audience: MarkettorJwtAudience) -> str:
    """
    Create a JWT ensuring that the correct audience and signing token is used
    """
    if not isinstance(audience, MarkettorJwtAudience):
        raise Exception("Audience must be in the list of MarketTor-supported audiences")

    encoded_jwt = jwt.encode(
        {
            **payload,
            "exp": datetime.now(tz=UTC) + expiry_delta,
            "aud": audience.value,
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    return encoded_jwt


def decode_jwt(token: str, audience: MarkettorJwtAudience) -> dict[str, Any]:
    info = jwt.decode(token, settings.SECRET_KEY, audience=audience.value, algorithms=["HS256"])

    return info
