"""Pydantic models for Servicio and ServiciosFeed API responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Servicio(BaseModel):
    """Represents a public institution or service (Servicio)."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str = Field(alias="codigo", description="Unique institution code.")
    titulo: str = Field(default="", alias="titulo", description="Official title of the institution.")
    sigla: str | None = Field(default=None, alias="sigla", description="Abbreviation or acronym.")
    url: str | None = Field(default=None, alias="url", description="Official website URL.")

    @model_validator(mode="before")
    @classmethod
    def _coerce_id(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Fallback for 'id' or 'nombre' if present in variations of API responses
            if "codigo" not in data and "id" in data:
                data["codigo"] = str(data["id"])
            if "titulo" not in data and "nombre" in data:
                data["titulo"] = str(data["nombre"])
        return data


class ServiciosFeed(BaseModel):
    """Represents a list feed of public services/institutions."""

    model_config = ConfigDict(populate_by_name=True)

    titulo: str = Field(default="Listado de Servicios", description="Feed title.")
    tipo: str = Field(default="chileatiende#serviciosFeed", description="Resource type descriptor.")
    items: list[Servicio] = Field(default_factory=list, description="List of Servicios returned.")

    def to_pandas(self) -> Any:
        """Export feed items to a pandas DataFrame."""
        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError("pandas is required for to_pandas(). Install it with `pip install pandas`.") from exc
        return pd.DataFrame([item.model_dump() for item in self.items])

    def to_polars(self) -> Any:
        """Export feed items to a polars DataFrame."""
        try:
            import polars as pl  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ImportError("polars is required for to_polars(). Install it with `pip install polars`.") from exc
        return pl.DataFrame([item.model_dump() for item in self.items])


class SingleServicioResponse(BaseModel):
    """Wrapper envelope for single Servicio API response."""

    servicio: Servicio


class ServiciosFeedEnvelope(BaseModel):
    """Wrapper envelope for ServiciosFeed API response."""

    feed: ServiciosFeed = Field(alias="fichas")

    @model_validator(mode="before")
    @classmethod
    def _coerce_envelope(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "servicios" in data and "fichas" not in data:
                data["fichas"] = data["servicios"]
        return data
