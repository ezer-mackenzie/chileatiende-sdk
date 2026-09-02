"""Pydantic models for Sucursal and SucursalesFeed API responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Sucursal(BaseModel):
    """Represents a ChileAtiende branch office (Sucursal)."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str = Field(description="Unique branch identifier code.")
    nombre: str = Field(default="", description="Branch office name.")
    direccion: str | None = Field(default=None, description="Physical street address.")
    comuna: str | None = Field(default=None, description="Municipality (Comuna).")
    region: str | None = Field(default=None, description="Region.")
    horario: str | None = Field(default=None, description="Operating hours.")
    telefono: str | None = Field(default=None, description="Contact phone number.")
    oficina_movil: bool = Field(default=False, alias="mobileOffice", description="Whether this is a mobile office.")
    latitud: float | None = Field(default=None, description="Latitude coordinate.")
    longitud: float | None = Field(default=None, description="Longitude coordinate.")

    @model_validator(mode="before")
    @classmethod
    def _coerce_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "codigo" not in data and "id" in data:
                data["codigo"] = str(data["id"])
            if "oficina_movil" not in data and "mobileOffice" in data:
                data["oficina_movil"] = bool(data["mobileOffice"])
        return data


class SucursalesFeed(BaseModel):
    """Represents a list feed of branch offices."""

    model_config = ConfigDict(populate_by_name=True)

    titulo: str = Field(default="Listado de Sucursales", description="Feed title.")
    tipo: str = Field(default="chileatiende#sucursalesFeed", description="Resource type descriptor.")
    items: list[Sucursal] = Field(default_factory=list, description="List of Sucursales returned.")
    total: int | None = Field(default=None, description="Total number of sucursales matching filter.")


class SingleSucursalResponse(BaseModel):
    """Wrapper envelope for single Sucursal API response."""

    sucursal: Sucursal


class SucursalesFeedEnvelope(BaseModel):
    """Wrapper envelope for SucursalesFeed API response."""

    sucursales: SucursalesFeed
