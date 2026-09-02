"""Command Line Interface (CLI) for ChileAtiende SDK."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .clients import SyncChileAtiendeClient
from .errors import ChileAtiendeError


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for ChileAtiende API operations."""
    parser = argparse.ArgumentParser(
        prog="chileatiende",
        description="ChileAtiende API Command Line Interface",
    )
    parser.add_argument(
        "--token",
        dest="token",
        help="ChileAtiende API access token (defaults to CHILEATIENDE_ACCESS_TOKEN env var).",
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Ficha commands
    ficha_parser = subparsers.add_parser("ficha", help="Get or search procedure sheets (Fichas).")
    ficha_sub = ficha_parser.add_subparsers(dest="subcommand")

    get_ficha_p = ficha_sub.add_parser("get", help="Get a single Ficha by ID.")
    get_ficha_p.add_argument("id", help="Ficha ID")

    search_ficha_p = ficha_sub.add_parser("search", help="Search Fichas by query.")
    search_ficha_p.add_argument("query", help="Search term")

    # Servicio commands
    servicio_parser = subparsers.add_parser("servicio", help="Get or list public services.")
    servicio_sub = servicio_parser.add_subparsers(dest="subcommand")

    servicio_sub.add_parser("list", help="List all public services.")
    get_serv_p = servicio_sub.add_parser("get", help="Get a public service by code.")
    get_serv_p.add_argument("code", help="Servicio code")

    # Sucursal commands
    sucursal_parser = subparsers.add_parser("sucursal", help="Get or list branch offices.")
    sucursal_sub = sucursal_parser.add_subparsers(dest="subcommand")

    sucursal_sub.add_parser("list", help="List branch offices.")
    get_suc_p = sucursal_sub.add_parser("get", help="Get a branch office by code.")
    get_suc_p.add_argument("code", help="Sucursal code")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    try:
        client = SyncChileAtiendeClient(access_token=args.token)
    except ChileAtiendeError as exc:
        print(f"Error initializing client: {exc}", file=sys.stderr)
        return 1

    try:
        if args.command == "ficha":
            if args.subcommand == "get":
                ficha = client.get_ficha(args.id)
                print(f"ID: {ficha.id}\nTitle: {ficha.titulo}\nService: {ficha.servicio or 'N/A'}\nObjective: {ficha.clean_objetivo or 'N/A'}")
            elif args.subcommand == "search":
                fichas_feed = client.list_fichas(query=args.query, max_results=10)
                print(f"Found {len(fichas_feed.items)} results for '{args.query}':")
                for item in fichas_feed.items:
                    print(f" - [{item.id}] {item.titulo}")
            else:
                ficha_parser.print_help()

        elif args.command == "servicio":
            if args.subcommand == "list":
                servicios_feed = client.list_servicios()
                print(f"Found {len(servicios_feed.items)} services:")
                for serv in servicios_feed.items:
                    print(f" - [{serv.codigo}] {serv.titulo} ({serv.sigla or 'N/A'})")
            elif args.subcommand == "get":
                servicio = client.get_servicio(args.code)
                print(f"Code: {servicio.codigo}\nTitle: {servicio.titulo}\nSigla: {servicio.sigla or 'N/A'}\nURL: {servicio.url or 'N/A'}")
            else:
                servicio_parser.print_help()

        elif args.command == "sucursal":
            if args.subcommand == "list":
                sucursales_feed = client.list_sucursales()
                print(f"Found {len(sucursales_feed.items)} branch offices:")
                for suc in sucursales_feed.items:
                    print(f" - [{suc.codigo}] {suc.nombre} - {suc.comuna or 'N/A'}")
            elif args.subcommand == "get":
                sucursal = client.get_sucursal(args.code)
                print(f"Code: {sucursal.codigo}\nName: {sucursal.nombre}\nAddress: {sucursal.direccion or 'N/A'}\nComuna: {sucursal.comuna or 'N/A'}")
            else:
                sucursal_parser.print_help()

    except ChileAtiendeError as exc:
        print(f"API Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
