from dataclasses import dataclass
from typing import Dict, Tuple, List, Set

from fastapi import FastAPI
from fastapi import APIRouter


@dataclass
class _ParsedRouter:
    pversion: str
    router: APIRouter
    prefix: str
    tags: List[str]


def parse_routers(
    tag: str, routers: Dict[Tuple[int], APIRouter]
) -> Dict[Tuple[int], _ParsedRouter]:
    """Parse routers in terms of prefix, tags and version"""
    parsed_routers = dict()

    major_routers = dict()
    major_versions = dict()
    for version, router in reversed(sorted(routers.items())):
        assert len(version) == 3, version
        major, minor, patch = version
        kversion = major, minor, patch, 0
        pversion = "v" + "_".join(map(str, version))
        sversion = "v" + ".".join(map(str, version))
        parsed_routers[kversion] = _ParsedRouter(
            pversion=pversion,
            router=router,
            prefix=f"/{pversion}",
            tags=[sversion],
        )
        mversion = version[0]
        if version > major_versions.get(mversion, (0, 0, 0)):
            major_versions[mversion] = version
            major_routers[mversion] = router

    for mversion, router in major_routers.items():
        pversion = f"v{mversion}"
        sversion = pversion
        version = major_versions[mversion]
        major, minor, patch = version
        kversion = major, minor, patch, 1
        parsed_routers[kversion] = _ParsedRouter(
            pversion=pversion,
            router=router,
            prefix=f"/{pversion}",
            tags=[sversion],
        )

    mversion = sorted(major_routers)[-1]
    router = major_routers[mversion]
    major, minor, patch = major_versions[mversion]
    kversion = major, minor, patch, 2
    parsed_routers[kversion] = _ParsedRouter(
        pversion="", router=router, prefix="", tags=[tag]
    )
    return parsed_routers


def extract_version_tags(
    all_parsed_routers: List[Dict[Tuple[int], _ParsedRouter]]
) -> Set[str]:
    """Extract all version tags"""
    tags = set()
    for parsed_routers in all_parsed_routers:
        for parsed_router in parsed_routers.values():
            if parsed_router.pversion:
                tags |= set(parsed_router.tags)
    return tags


def extract_version(
    all_parsed_routers: List[Dict[Tuple[int], _ParsedRouter]]
) -> Tuple[int]:
    """Extract the latest version"""
    return max(sorted(parsed_routers)[-1][:3] for parsed_routers in all_parsed_routers)


def add_routes(
    app: FastAPI, all_parsed_routers: List[Dict[Tuple[int], _ParsedRouter]]
) -> None:
    """Add router to an API"""
    kversions = set()
    for keys in all_parsed_routers:
        kversions |= set(keys)

    for kversion in reversed(sorted(kversions)):
        for parsed_routers in all_parsed_routers:
            parsed_router = parsed_routers.get(kversion)
            if parsed_router is not None:
                app.include_router(
                    parsed_router.router,
                    prefix=parsed_router.prefix,
                    tags=parsed_router.tags,
                )
