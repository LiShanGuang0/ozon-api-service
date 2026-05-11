from app.db.redis import redis_client
from app.services.credential_store import CredentialStore


def store_credentials(credentials):
    return CredentialStore().store(credentials)


def load_credentials(ref: str):
    return CredentialStore().load(ref)


__all__ = ["redis_client", "store_credentials", "load_credentials"]
