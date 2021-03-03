from typing import Any
from typing import Dict
from typing import List
from uuid import UUID

from sqlalchemy.future import select

from app.db.base import async_session
from app.db.view.vehicle_entries import VehicleEntries


def _fetch_sub_groups_and_sets(entry_list: List[Any]) -> List[Dict[str, Any]]:
    """Combines all subgroups and sets to list"""

    tails_entries = []
    ids = {item.formation_id for item in entry_list}
    for item in entry_list:
        if item in ids:
            children = list(
                filter(lambda vehicle: vehicle.parent_id == item.formation_id, entry_list)
            )
            ids -= {item.formation_id for item in children}
            tails_entries.append(
                {
                    "formation_id": item.formation_id,
                    "formation_name": item.formation_name,
                    "formation_type": item.formation_type,
                    "features": item.features,
                    "entries": [
                        {
                            "formation_id": entry.formation_id,
                            "formation_name": entry.formation_name,
                            "formation_type": entry.formation_type,
                            "features": entry.features,
                            "entries": [],
                        }
                        for entry in children
                    ],
                }
            )
    return tails_entries


def _fetch_groups(
    groups_entities: List[Any], sub_groups_and_sets: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Combines all groups with their children to list"""

    ids = {item["formation_id"] for item in sub_groups_and_sets}
    groups = []
    for item in groups_entities:
        children = list(
            filter(lambda ch: ch["parent_id"] == item.formation_id, sub_groups_and_sets)
        )
        group = {
            "formation_id": item.formation_id,
            "formation_name": item.formation_name,
            "formation_type": item.formation_type,
            "features": item.features,
            "entries": [],
        }
        for child in children:
            if child["formation_id"] in ids:
                ids -= {child["formation_id"]}
                group["entries"].append(child)
        groups.append(group)
    return groups


async def get_vehicle_info(vehicle_id: UUID) -> Dict[str, Any]:
    """Retrieves vehicle name with all linked functions and components"""

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(VehicleEntries).filter_by(vehicle_id=str(vehicle_id))
            )
            vehicles = result.scalars().all()
            if vehicles:
                sub_groups_and_sets = _fetch_sub_groups_and_sets(
                    list(filter(lambda vehicle: vehicle.parent_id is not None, vehicles))
                )
                heads = list(filter(lambda vehicle: vehicle.parent_id is None, vehicles))
                groups = _fetch_groups(heads, sub_groups_and_sets)
                return {
                    "vehicle_name": vehicles[0].vehicle_name,
                    "vehicle_id": vehicles[0].vehicle_id,
                    "groups": groups,
                }
            return {}
