"""Test configuration and fixtures for ChileAtiende SDK."""

import pytest

TEST_ACCESS_TOKEN = "test_token_12345"


@pytest.fixture
def test_token() -> str:
    return TEST_ACCESS_TOKEN


@pytest.fixture
def mock_ficha_data() -> dict:
    return {
        "ficha": {
            "id": "1",
            "fecha": "2023-09-22 10:00:00",
            "servicio": "Dirección de Previsión de Carabineros de Chile",
            "codigo_servicio": "AD001",
            "titulo": "Pago Complementario del Reintegro Médico",
            "objetivo": "Solicitar el pago complementario.",
            "beneficiarios": "Personal activo de Carabineros.",
            "costo": "Ninguno.",
            "vigencia": "Anual.",
            "plazo": "27 días hábiles.",
            "temas": {"tema": ["Salud"]},
            "tags": {"tag": ["DIPRECA", "Carabineros"]},
            "url": "https://www.chileatiende.gob.cl/fichas/1",
        }
    }


@pytest.fixture
def mock_fichas_feed_data() -> dict:
    return {
        "fichas": {
            "titulo": "Listado de Fichas",
            "tipo": "chileatiende#fichasFeed",
            "nextPageToken": "token_next_123",
            "items": [
                {
                    "id": "1",
                    "titulo": "Ficha 1",
                    "servicio": "Servicio 1",
                },
                {
                    "id": "2",
                    "titulo": "Ficha 2",
                    "servicio": "Servicio 2",
                },
            ],
        }
    }


@pytest.fixture
def mock_servicio_data() -> dict:
    return {
        "servicio": {
            "codigo": "AD001",
            "titulo": "Dirección de Previsión de Carabineros de Chile",
            "sigla": "DIPRECA",
            "url": "https://www.dipreca.cl",
        }
    }


@pytest.fixture
def mock_servicios_feed_data() -> dict:
    return {
        "fichas": {
            "titulo": "Listado de Servicios",
            "tipo": "chileatiende#serviciosFeed",
            "items": [
                {
                    "codigo": "AD001",
                    "titulo": "DIPRECA",
                    "sigla": "DIPRECA",
                    "url": "https://www.dipreca.cl",
                }
            ],
        }
    }


@pytest.fixture
def mock_sucursal_data() -> dict:
    return {
        "sucursal": {
            "codigo": "SUC001",
            "nombre": "Oficina Central Santiago",
            "direccion": "Moneda 1137",
            "comuna": "Santiago",
            "region": "Región Metropolitana",
            "horario": "Lunes a Viernes 08:30 a 14:00",
            "telefono": "101",
            "oficina_movil": False,
            "latitud": -33.441,
            "longitud": -70.654,
        }
    }


@pytest.fixture
def mock_sucursales_feed_data() -> dict:
    return {
        "sucursales": {
            "titulo": "Listado de Sucursales",
            "tipo": "chileatiende#sucursalesFeed",
            "total": 1,
            "items": [
                {
                    "codigo": "SUC001",
                    "nombre": "Oficina Central Santiago",
                    "direccion": "Moneda 1137",
                    "comuna": "Santiago",
                    "mobileOffice": False,
                }
            ],
        }
    }
