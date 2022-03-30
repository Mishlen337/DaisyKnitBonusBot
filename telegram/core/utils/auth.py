import os
import json
from typing import List

from aiogoogle.auth.creds import ServiceAccountCreds

# from app.utils.google.scopes import scopes
# from scopes import scopes
from .scopes import scopes


# from app.config import settings
async def make_creds(service_key: str, scopes: List[str] = scopes) -> ServiceAccountCreds:
    # TODO edit docsting
    """creates object with credentials which can further be used
    to create services and interact with google
    on behalf of the service account

    Args:
        scopes (List[str], optional): list with defined google scopes.
        Defaults to scopes.

    Returns:
        ServiceAccountCreds: object with credentials and scopes
    """
    # creds_env_name = 'google_auth_creds' if not creds_env_name else settings.GOOGLE_AUTH_CREDS
    service_account_key = json.loads(service_key)
    # service_account_key = json.loads(settings.GOOGLE_AUTH_CREDS)
    creds = ServiceAccountCreds(scopes=scopes, **service_account_key)
    return creds
