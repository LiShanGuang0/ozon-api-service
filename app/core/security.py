import hashlib
from dataclasses import dataclass
from typing import Annotated

from fastapi import Header, HTTPException, status


@dataclass(frozen=True)
class OzonCredentials:
    client_id: str
    api_key: str

    @property
    def api_key_fingerprint(self) -> str:
        return hashlib.sha256(self.api_key.encode("utf-8")).hexdigest()


def get_ozon_credentials(
    client_id: Annotated[str | None, Header(alias="Client-Id")] = None,
    api_key: Annotated[str | None, Header(alias="Api-Key")] = None,
) -> OzonCredentials:
    if not client_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required header: Client-Id")
    if not api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required header: Api-Key")
    return OzonCredentials(client_id=client_id, api_key=api_key)
