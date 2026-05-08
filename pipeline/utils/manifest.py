"""
Manifest-Helper für die Pipeline.

Pro Snapshot wird ein _manifest.json geschrieben, das pro heruntergeladener
Datei die Provenance dokumentiert: URL, Grösse, SHA-256-Hash, Resource-ID.

Damit ist jeder Snapshot:
- Bit-exakt verifizierbar (Hash)
- Quellen-rückverfolgbar (URL + Resource-ID)
- Zeitpunkt-dokumentiert (extracted_at)

Diese Provenance-Schicht ist methodisches Kernstück der Frozen-Snapshot-Strategie
und Voraussetzung für reproduzierbare Eval-Ergebnisse.
"""

import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional


def compute_sha256(filepath: Path) -> str:
    """
    Berechnet den SHA-256-Hash einer Datei.
    Streamt in 8KB-Blöcken, damit auch grosse Files (z.B. GeoPackages) funktionieren.
    """
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit() -> Optional[str]:
    """
    Gibt den aktuellen git-Commit-Hash zurück (kurze Form),
    oder None falls kein git-Repo vorhanden / git nicht installiert.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def init_manifest(snapshot_date: str, extracted_by: str) -> dict:
    """
    Initialisiert ein neues Manifest mit Header-Metadaten.

    Args:
        snapshot_date: Snapshot-Datum als 'YYYY-MM-DD'
        extracted_by: Name des Extract-Skripts (z.B. 'extract_bfe.py')
    """
    return {
        "snapshot_date": snapshot_date,
        "extracted_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "extracted_by": extracted_by,
        "git_commit": get_git_commit(),
        "sources": {},
    }


def add_file_to_manifest(
    manifest: dict,
    source_family: str,
    dataset_id: str,
    format_key: str,
    filepath: Path,
    url: str,
    resource_id: Optional[str] = None,
) -> None:
    """
    Fügt eine heruntergeladene Datei zum Manifest hinzu.

    Args:
        manifest: Das Manifest-Dict (in-place modifiziert)
        source_family: z.B. 'bfe', 'swissgrid', 'open_meteo'
        dataset_id: z.B. 'pv_grossanlagen', 'bilanz_monatswerte'
        format_key: z.B. 'csv', 'gpkg', 'xlsx'
        filepath: Pfad zur heruntergeladenen Datei
        url: Download-URL der Datei
        resource_id: Optional die CKAN-Resource-UUID
    """
    if source_family not in manifest["sources"]:
        manifest["sources"][source_family] = {}
    if dataset_id not in manifest["sources"][source_family]:
        manifest["sources"][source_family][dataset_id] = {}

    entry = {
        "url": url,
        "filename": filepath.name,
        "size_bytes": filepath.stat().st_size,
        "sha256": compute_sha256(filepath),
    }
    if resource_id:
        entry["resource_id"] = resource_id

    manifest["sources"][source_family][dataset_id][format_key] = entry


def write_manifest(manifest: dict, snapshot_dir: Path) -> Path:
    """
    Schreibt das Manifest als _manifest.json ins Snapshot-Verzeichnis.
    Returns den Pfad zur geschriebenen Datei.
    """
    manifest_path = snapshot_dir / "_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest_path


def load_manifest(snapshot_dir: Path) -> Optional[dict]:
    """
    Lädt ein bestehendes Manifest, falls vorhanden.
    Returns None, wenn kein Manifest existiert.
    """
    manifest_path = snapshot_dir / "_manifest.json"
    if not manifest_path.exists():
        return None
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)
