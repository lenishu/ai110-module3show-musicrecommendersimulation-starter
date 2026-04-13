"""
Weight Sensitivity Test: Compare original vs. modified weights
Tests how doubling energy weight and halving genre weight affects recommendations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import List, Dict, Tuple
import csv

# Load songs (same as main.py)
def load_songs(csv_path: str) -> List[Dict]:
    songs = []
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "instrumentalness": float(row["instrumentalness"]),
                "language": row["language"],
                "era": row["era"],
            }
            songs.append(song)
    return songs

# ORIGINAL SCORING FUNCTION
def score_song_original(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Original weighting from recommender.py"""
    score = 0.0
    reasons = []

    # Language match
    if song["language"].lower() == user_prefs["preferred_language"].lower():
        score += 3.0
    else:
        score -= 0.5

    # Era match
    if song["era"] == user_prefs["preferred_era"]:
        score += 3.0
    else:
        score -= 0.3

    # Genre match
    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += 2.5
    else:
        score -= 0.2

    # Mood match
    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += 2.0
    else:
        score -= 0.1

    # Energy (weight: 2.0)
    energy_distance = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0, 2.0 * (1 - energy_distance))
    score += energy_score

    # Valence (weight: 1.5)
    valence_distance = abs(song["valence"] - user_prefs["target_valence"])
    valence_score = max(0, 1.5 * (1 - valence_distance))
    score += valence_score

    # Danceability (weight: 1.0)
    danceability_distance = abs(song["danceability"] - user_prefs["target_danceability"])
    danceability_score = max(0, 1.0 * (1 - danceability_distance))
    score += danceability_score

    # Acousticness (weight: 1.0)
    acousticness_distance = abs(song["acousticness"] - user_prefs["target_acousticness"])
    acousticness_score = max(0, 1.0 * (1 - acousticness_distance))
    score += acousticness_score

    return (score, reasons)

# MODIFIED SCORING FUNCTION (Double energy, halve genre)
def score_song_modified(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Modified weighting: energy weight doubled (2.0 -> 4.0), genre halved (2.5 -> 1.25)"""
    score = 0.0
    reasons = []

    # Language match (unchanged)
    if song["language"].lower() == user_prefs["preferred_language"].lower():
        score += 3.0
    else:
        score -= 0.5

    # Era match (unchanged)
    if song["era"] == user_prefs["preferred_era"]:
        score += 3.0
    else:
        score -= 0.3

    # Genre match (HALVED: 2.5 -> 1.25)
    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += 1.25  # CHANGED
    else:
        score -= 0.2

    # Mood match (unchanged)
    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += 2.0
    else:
        score -= 0.1

    # Energy (DOUBLED: 2.0 -> 4.0)
    energy_distance = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0, 4.0 * (1 - energy_distance))  # CHANGED
    score += energy_score

    # Valence (unchanged)
    valence_distance = abs(song["valence"] - user_prefs["target_valence"])
    valence_score = max(0, 1.5 * (1 - valence_distance))
    score += valence_score

    # Danceability (unchanged)
    danceability_distance = abs(song["danceability"] - user_prefs["target_danceability"])
    danceability_score = max(0, 1.0 * (1 - danceability_distance))
    score += danceability_score

    # Acousticness (unchanged)
    acousticness_distance = abs(song["acousticness"] - user_prefs["target_acousticness"])
    acousticness_score = max(0, 1.0 * (1 - acousticness_distance))
    score += acousticness_score

    return (score, reasons)

# Test profiles
TEST_PROFILES = {
    "chill_lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
        "preferred_language": "English",
        "preferred_era": "2020-25",
    },
    "intense_rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_danceability": 0.65,
        "target_acousticness": 0.10,
        "preferred_language": "English",
        "preferred_era": "2010-20",
    },
}

def main():
    csv_path = Path(__file__).parent.parent / "data" / "songs.csv"
    songs = load_songs(str(csv_path))

    print("\n" + "="*80)
    print("  WEIGHT SENSITIVITY TEST: Original vs. Modified Weights")
    print("="*80)
    print("\n  MODIFICATION: Double Energy weight (2.0 -> 4.0), Halve Genre weight (2.5 -> 1.25)")
    print("  NEW MAX SCORE: 19.0 (was 17.5)\n")

    for profile_name, user_prefs in TEST_PROFILES.items():
        print("\n" + "="*80)
        print(f"  PROFILE: {profile_name.upper()}")
        print("="*80)

        # Score with both methods
        original_scores = []
        modified_scores = []

        for song in songs:
            orig_score, _ = score_song_original(user_prefs, song)
            mod_score, _ = score_song_modified(user_prefs, song)
            original_scores.append((song, orig_score))
            modified_scores.append((song, mod_score))

        # Sort both
        original_scores.sort(key=lambda x: x[1], reverse=True)
        modified_scores.sort(key=lambda x: x[1], reverse=True)

        print("\n  TOP 5 WITH ORIGINAL WEIGHTS:")
        for rank, (song, score) in enumerate(original_scores[:5], 1):
            print(f"    #{rank} {song['title']} ({song['artist']}) - {score:.2f}/17.5")

        print("\n  TOP 5 WITH MODIFIED WEIGHTS (energy 2x, genre 0.5x):")
        for rank, (song, score) in enumerate(modified_scores[:5], 1):
            print(f"    #{rank} {song['title']} ({song['artist']}) - {score:.2f}/19.0")

        # Check if top 5 changed
        original_top5 = [s[0]['id'] for s in original_scores[:5]]
        modified_top5 = [s[0]['id'] for s in modified_scores[:5]]

        changed = set(original_top5) != set(modified_top5)
        print(f"\n  RESULT: {'[CHANGED]' if changed else '[UNCHANGED]'}")

        if changed:
            print("  - Energy weighting now dominates; genre mismatches are more acceptable.")
            print("  - Songs with high energy but different genre now rank higher.")
        else:
            print("  - Language and era matches are so strong that weight changes don't affect top 5.")

if __name__ == "__main__":
    main()
