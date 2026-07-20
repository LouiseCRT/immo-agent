# ============================================================
# CONFIG DES CRITÈRES - modifie ce fichier autant de fois que tu veux
# Chaque exécution quotidienne relit ce fichier avant de chercher.
# ============================================================

criteria:
  location_query: "versailles-78000"   # ville-code_postal
  transaction: "achat"                  # achat ou location
  property_types:
    - "appartement"                     # appartement, maison, terrain, parking, loft
  budget_max: 200000
  budget_min: 0
  surface_min: 0                        # 0 = ignoré
  rooms_min: 0                          # 0 = ignoré

  # Mots-clés qui EXCLUENT une annonce si présents dans le titre
  keywords_exclude:
    - "viager"
    - "colocation"

# ============================================================
# EMAIL DE DESTINATION
# ============================================================
email:
  to: "ton.email@example.com"
  subject_prefix: "🏠 Annonces du jour"
