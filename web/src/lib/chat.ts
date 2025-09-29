export const generateFakeResponse = (prompt: string): string => {
  return [
    "**Analyse rapide**",
    `- Demande : ${prompt}`,
    "- Ressource pressentie : _Base de connaissances interne_",
    "",
    "**Actions suggérées**",
    "1. Vérifier la fiche de procédure associée",
    "2. Préparer une réponse personnalisée pour l'utilisateur",
    "",
    "```sql",
    "-- Exemple de requête à valider",
    "SELECT * FROM documents_clef",
    "WHERE tags @> ARRAY['metier']",
    "LIMIT 5;",
    "```",
  ].join("\n");
};
