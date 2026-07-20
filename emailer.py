"""
Client simple pour l'API JSON publique de bienici.com (utilisée par leur
propre site web, pas de clé/compte nécessaire).

Bases techniques vérifiées :
- https://www.bienici.com/realEstateAds.json?filters=<json>  -> résultats
- https://res.bienici.com/suggest.json?q=<ville>              -> zoneIds

Attention : ceci reste un usage non-officiel d'une API non documentée par
Bien'ici. Le format peut changer sans préavis. Reste dans un usage
raisonnable et personnel (quelques requêtes par jour), pas de revente
ou republication des données.
"""

import json
import requests

HEADERS = {
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9",
    "referer": "https://www.bienici.com/recherche/achat",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "x-requested-with": "XMLHttpRequest",
}

PROPERTY_TYPE_MAP = {
    "appartement": "flat",
    "maison": "house",
    "terrain": "terrain",
    "parking": "parking",
    "loft": "loft",
    "chateau": "castle",
}

TRANSACTION_MAP = {
    "achat": "buy",
    "location": "rent",
}


def get_zone_ids(location_query: str) -> list:
    """Convertit 'versailles-78000' en zoneIds internes Bien'ici."""
    # bienici veut juste le nom de ville ou code postal, sans le slug complet
    query = location_query.split("-")[0]
    resp = requests.get(
        f"https://res.bienici.com/suggest.json?q={query}",
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return []
    return data[0].get("zoneIds", [])


def search_listings(criteria: dict, max_pages: int = 3) -> list:
    """
    Interroge l'API Bien'ici selon les critères et retourne une liste
    d'annonces (dictionnaires).
    """
    property_types = [
        PROPERTY_TYPE_MAP.get(p, p) for p in criteria.get("property_types", ["appartement"])
    ]
    transaction = TRANSACTION_MAP.get(criteria.get("transaction", "achat"), "buy")
    zone_ids = get_zone_ids(criteria["location_query"])

    all_ads = []
    for page in range(1, max_pages + 1):
        filters = {
            "size": 24,
            "from": (page - 1) * 24,
            "page": page,
            "onTheMarket": [True],
            "filterType": transaction,
            "propertyType": property_types,
            "sortBy": "publicationDate",
            "sortOrder": "desc",
        }
        if zone_ids:
            filters["zoneIdsByTypes"] = {"zoneIds": zone_ids}
        if criteria.get("budget_max"):
            filters["maxPrice"] = criteria["budget_max"]
        if criteria.get("budget_min"):
            filters["minPrice"] = criteria["budget_min"]
        if criteria.get("surface_min"):
            filters["minArea"] = criteria["surface_min"]
        if criteria.get("rooms_min"):
            filters["minRooms"] = criteria["rooms_min"]

        params = {"filters": json.dumps(filters)}
        resp = requests.get(
            "https://www.bienici.com/realEstateAds.json",
            params=params,
            headers=HEADERS,
            timeout=20,
        )
        if resp.status_code != 200:
            break

        data = resp.json()
        ads = data.get("realEstateAds", [])
        if not ads:
            break
        all_ads.extend(ads)

        total = data.get("total", 0)
        if len(all_ads) >= total:
            break

    return all_ads
