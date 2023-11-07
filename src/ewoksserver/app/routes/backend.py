from dataclasses import dataclass
from typing import Dict, Tuple, List, Set, Union, Callable

from fastapi import APIRouter
from fastapi import FastAPI
from starlette.types import ASGIApp

from . import BACKEND_PREFIX

AppGenerator = Callable[[FastAPI], ASGIApp]
RouteType = Union[APIRouter, AppGenerator]


def assert_route_versions(*all_routes: Dict[Tuple[int], RouteType]) -> None:
    versions = {tuple(sorted(routes)) for routes in all_routes}
    assert len(versions) == 1, "Not all routes have the same versions"


@dataclass
class _ParsedRoute:
    pversion: str
    route: RouteType
    prefix: str
    tag: str


def parse_routes(
    tag: str,
    routes: Dict[Tuple[int], RouteType],
    prefix: str = "",
) -> Dict[Tuple[int], _ParsedRoute]:
    """Parse routes in terms of prefix, tag and version"""
    parsed_routes = dict()

    major_routes = dict()
    major_versions = dict()
    for version, route in reversed(sorted(routes.items())):
        assert len(version) == 3, version
        major, minor, patch = version
        kversion = major, minor, patch, 0
        pversion = "v" + "_".join(map(str, version))
        sversion = "v" + ".".join(map(str, version))
        parsed_routes[kversion] = _ParsedRoute(
            pversion=pversion,
            route=route,
            prefix=f"{BACKEND_PREFIX}/{pversion}/{prefix}"
            if prefix
            else f"{BACKEND_PREFIX}/{pversion}",
            tag=sversion,
        )
        mversion = version[0]
        if version > major_versions.get(mversion, (0, 0, 0)):
            major_versions[mversion] = version
            major_routes[mversion] = route

    for mversion, route in major_routes.items():
        pversion = f"v{mversion}"
        sversion = pversion
        version = major_versions[mversion]
        major, minor, patch = version
        kversion = major, minor, patch, 1
        parsed_routes[kversion] = _ParsedRoute(
            pversion=pversion,
            route=route,
            prefix=f"{BACKEND_PREFIX}/{pversion}/{prefix}"
            if prefix
            else f"{BACKEND_PREFIX}/{pversion}",
            tag=sversion,
        )

    mversion = sorted(major_routes)[-1]
    route = major_routes[mversion]
    major, minor, patch = major_versions[mversion]
    kversion = major, minor, patch, 2
    parsed_routes[kversion] = _ParsedRoute(
        pversion="",
        route=route,
        prefix=f"{BACKEND_PREFIX}/{prefix}" if prefix else f"{BACKEND_PREFIX}",
        tag=tag,
    )
    return parsed_routes


def extract_version_tags(
    all_parsed_routes: List[Dict[Tuple[int], _ParsedRoute]]
) -> Set[str]:
    """Extract all version tags"""
    tags = set()
    for parsed_routes in all_parsed_routes:
        for parsed_route in parsed_routes.values():
            if parsed_route.pversion:
                tags.add(parsed_route.tag)
    return tags


def extract_lastest_version(
    all_parsed_routes: List[Dict[Tuple[int], _ParsedRoute]]
) -> Tuple[int]:
    """Extract the latest version"""
    return max(sorted(parsed_routes)[-1][:3] for parsed_routes in all_parsed_routes)


def add_routes(
    app: FastAPI,
    all_parsed_routes: List[Dict[Tuple[int], _ParsedRoute]],
    skip_older_versions: bool = False,
) -> None:
    """Add routes to an API"""
    kversions = set()
    for keys in all_parsed_routes:
        kversions |= set(keys)

    for kversion in reversed(sorted(kversions)):
        for parsed_routes in all_parsed_routes:
            parsed_route = parsed_routes.get(kversion)
            if parsed_route is not None:
                if skip_older_versions and parsed_route.pversion:
                    continue
                if isinstance(parsed_route.route, APIRouter):
                    app.include_router(
                        parsed_route.route,
                        prefix=parsed_route.prefix,
                        tags=[parsed_route.tag],
                    )
                elif isinstance(parsed_route.route, Callable):
                    subapp = parsed_route.route(app)
                    app.mount(parsed_route.prefix, subapp)
                else:
                    raise TypeError(str(type(parsed_route)))
