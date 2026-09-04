# File-Integrity-Monitor
Un script qui me permet de surveiller un dossier et détecte :  ✅ fichiers inchangés 
⚠️ fichiers modifiés 
🚨 fichiers supprimés 
🆕 nouveaux fichiers 
🔐 comparaison via SHA-256 
💾 sauvegarde d'une baseline dans baseline.json

                 DOSSIER SURVEILLÉ
                        │
                        ▼
                Parcours des fichiers
                        │
                        ▼
                  SHA-256
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       baseline.json        état actuel
              │                   │
              └─────────┬─────────┘
                        ▼
                    COMPARAISON
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
     Modifié         Supprimé        Nouveau
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                      ALERTE
