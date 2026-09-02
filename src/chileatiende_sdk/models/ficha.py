"""Pydantic models for Ficha and FichasFeed API responses."""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _strip_html(raw_html: str | None) -> str | None:
    """Remove HTML tags from a text string and collapse extra whitespace."""
    if not raw_html:
        return None
    cleaned = re.sub(r"<[^>]+>", " ", raw_html)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned if cleaned else None


class Ficha(BaseModel):
    """Represents a ChileAtiende procedure/information sheet (Ficha)."""

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str = Field(description="Unique identifier of the Ficha.")
    fecha: str | None = Field(default=None, description="Last update timestamp.")
    servicio: str | None = Field(default=None, description="Institution providing the service.")
    codigo_servicio: str | None = Field(default=None, description="Institution code.")
    titulo: str = Field(default="", description="Title of the Ficha.")
    objetivo: str | None = Field(default=None, description="Objective description.")
    beneficiarios: str | None = Field(default=None, description="Target audience/beneficiaries.")
    costo: str | None = Field(default=None, description="Cost of the procedure.")
    vigencia: str | None = Field(default=None, description="Validity period.")
    plazo: str | None = Field(default=None, description="Processing timeframe.")
    marco_legal: str | None = Field(default=None, description="Legal framework.")
    guia_online: str | None = Field(default=None, description="Online guide instructions.")
    guia_oficina: str | None = Field(default=None, description="In-person office guide instructions.")
    guia_consulado: str | None = Field(default=None, description="Consulate guide instructions.")
    guia_correo: str | None = Field(default=None, description="Mail guide instructions.")
    temas: list[str] = Field(default_factory=list, description="Associated categories/topics.")
    tags: list[str] = Field(default_factory=list, description="Associated tags.")
    url: str | None = Field(default=None, description="Direct URL to the Ficha in ChileAtiende.")

    @property
    def clean_objetivo(self) -> str | None:
        """Plaintext objective with HTML tags removed."""
        return _strip_html(self.objetivo)

    @property
    def clean_beneficiarios(self) -> str | None:
        """Plaintext beneficiaries description with HTML tags removed."""
        return _strip_html(self.beneficiarios)

    @property
    def clean_costo(self) -> str | None:
        """Plaintext cost description with HTML tags removed."""
        return _strip_html(self.costo)

    @property
    def clean_vigencia(self) -> str | None:
        """Plaintext validity timeframe with HTML tags removed."""
        return _strip_html(self.vigencia)

    @property
    def clean_plazo(self) -> str | None:
        """Plaintext processing timeframe with HTML tags removed."""
        return _strip_html(self.plazo)

    @field_validator("temas", mode="before")
    @classmethod
    def _parse_temas(cls, v: Any) -> list[str]:
        if not v:
            return []
        if isinstance(v, dict):
            raw = v.get("tema", [])
            if isinstance(raw, str):
                return [raw]
            if isinstance(raw, list):
                return [str(x) for x in raw if x]
        if isinstance(v, list):
            return [str(x) for x in v if x]
        if isinstance(v, str):
            return [v]
        return []

    @field_validator("tags", mode="before")
    @classmethod
    def _parse_tags(cls, v: Any) -> list[str]:
        if not v:
            return []
        if isinstance(v, dict):
            raw = v.get("tag", [])
            if isinstance(raw, str):
                return [raw]
            if isinstance(raw, list):
                return [str(x) for x in raw if x]
        if isinstance(v, list):
            return [str(x) for x in v if x]
        if isinstance(v, str):
            return [v]
        return []


class FichasFeed(BaseModel):
    """Represents a paginated list feed of Fichas."""

    model_config = ConfigDict(populate_by_name=True)

    titulo: str = Field(default="Listado de Fichas", description="Feed title.")
    tipo: str = Field(default="chileatiende#fichasFeed", description="Resource type descriptor.")
    next_page_token: str | None = Field(
        default=None, alias="nextPageToken", description="Pagination continuation token."
    )
    items: list[Ficha] = Field(default_factory=list, description="List of Fichas returned.")


class SingleFichaResponse(BaseModel):
    """Wrapper envelope for single Ficha API response."""

    ficha: Ficha


class FichasFeedEnvelope(BaseModel):
    """Wrapper envelope for FichasFeed API response."""

    fichas: FichasFeed
