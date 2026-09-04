import hashlib
import json
import argparse
from pathlib import Path
from datetime import datetime


# =========================
# Configuration
# =========================

MONITORED_DIR = Path("monitored")
BASELINE_FILE = Path("baseline.json")
LOG_FILE = Path("integrity.log")


# =========================
# Calcul du hash SHA-256
# =========================

def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


# =========================
# Récupération des fichiers
# =========================

def get_files():
    files = {}

    if not MONITORED_DIR.exists():
        print(f"❌ Le dossier '{MONITORED_DIR}' n'existe pas.")
        return files

    for filepath in MONITORED_DIR.rglob("*"):

        if filepath.is_file():

            relative_path = filepath.relative_to(MONITORED_DIR)

            files[str(relative_path)] = calculate_hash(filepath)

    return files


# =========================
# Création de la baseline
# =========================

def create_baseline():

    files = get_files()

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:

        json.dump(
            files,
            file,
            indent=4
        )

    print()
    print("================================")
    print("      BASELINE CRÉÉE")
    print("================================")
    print(f"Fichiers enregistrés : {len(files)}")
    print(f"Baseline : {BASELINE_FILE}")
    print()


# =========================
# Chargement de la baseline
# =========================

def load_baseline():

    if not BASELINE_FILE.exists():

        print("❌ Aucune baseline trouvée.")
        print()
        print("Créez-en une avec :")
        print("python monitor.py --init")

        return None

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


# =========================
# Journalisation
# =========================

def write_log(event_type, filepath):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as log:

        log.write(
            f"{timestamp} | {event_type} | {filepath}\n"
        )


# =========================
# Vérification de l'intégrité
# =========================

def check_integrity():

    baseline = load_baseline()

    if baseline is None:
        return

    current_files = get_files()

    modified = []
    deleted = []
    new_files = []


    # =========================
    # Recherche des fichiers
    # modifiés ou supprimés
    # =========================

    for filepath, old_hash in baseline.items():

        # Fichier supprimé
        if filepath not in current_files:

            deleted.append(filepath)

        # Fichier modifié
        elif current_files[filepath] != old_hash:

            modified.append(filepath)


    # =========================
    # Recherche des nouveaux fichiers
    # =========================

    for filepath in current_files:

        if filepath not in baseline:

            new_files.append(filepath)


    # =========================
    # Affichage du rapport
    # =========================

    print()
    print("================================")
    print("      RAPPORT D'INTÉGRITÉ")
    print("================================")


    # Aucun changement

    if not modified and not deleted and not new_files:

        print("✅ Aucun changement détecté.")


    # Fichiers modifiés

    for filepath in modified:

        print(f"⚠️  MODIFIÉ   : {filepath}")

        write_log(
            "MODIFIED",
            filepath
        )


    # Fichiers supprimés

    for filepath in deleted:

        print(f"🚨 SUPPRIMÉ  : {filepath}")

        write_log(
            "DELETED",
            filepath
        )


    # Nouveaux fichiers

    for filepath in new_files:

        print(f"🆕 NOUVEAU   : {filepath}")

        write_log(
            "NEW",
            filepath
        )


    print()


# =========================
# Programme principal
# =========================

def main():

    parser = argparse.ArgumentParser(
        description="File Integrity Monitor - Surveillance d'intégrité des fichiers"
    )


    parser.add_argument(
        "--init",
        action="store_true",
        help="Créer une nouvelle baseline"
    )


    parser.add_argument(
        "--check",
        action="store_true",
        help="Vérifier l'intégrité des fichiers"
    )


    args = parser.parse_args()


    if args.init:

        create_baseline()


    elif args.check:

        check_integrity()


    else:

        parser.print_help()


# =========================
# Lancement
# =========================

if __name__ == "__main__":

    main()
