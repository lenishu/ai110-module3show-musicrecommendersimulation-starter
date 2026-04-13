"""
Command line runner for the Music Recommender Simulation.

Runs four distinct taste profiles through the recommender and prints
the top 3 results for each, with score breakdowns.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from recommender import load_songs, recommend_songs


# ─── Taste Profiles ────────────────────────────────────────────────────────────
# Each profile is a dict whose keys match exactly what score_song() expects.
# Keys: favorite_genre, favorite_mood, target_energy, target_valence,
#       target_danceability, target_acousticness, preferred_language, preferred_era

PROFILES = {

    "chill_lofi": {
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":       0.40,   # low — background, unobtrusive
        "target_valence":      0.58,   # slightly melancholy but not dark
        "target_danceability": 0.60,   # gentle head-bob, not a dance floor
        "target_acousticness": 0.75,   # warm, organic texture
        "preferred_language":  "English",
        "preferred_era":       "2020-25",
    },

    "intense_rock": {
        "favorite_genre":      "rock",
        "favorite_mood":       "intense",
        "target_energy":       0.92,   # high — adrenaline
        "target_valence":      0.45,   # edge / aggression, not cheery
        "target_danceability": 0.65,   # driving rhythm but not club
        "target_acousticness": 0.10,   # electric, loud
        "preferred_language":  "English",
        "preferred_era":       "2010-20",
    },

    "nepali_pop_happy": {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":       0.82,
        "target_valence":      0.83,
        "target_danceability": 0.80,
        "target_acousticness": 0.25,
        "preferred_language":  "Nepali",
        "preferred_era":       "2026",
    },

    "romantic_rnb": {
        "favorite_genre":      "rnb",
        "favorite_mood":       "romantic",
        "target_energy":       0.70,
        "target_valence":      0.80,
        "target_danceability": 0.68,
        "target_acousticness": 0.33,
        "preferred_language":  "English",
        "preferred_era":       "2026",
    },

    # ─── EDGE CASE PROFILES (for adversarial testing) ───────────────────────────

    "conflicting_preferences": {
        "favorite_genre":      "ambient",
        "favorite_mood":       "sad",
        "target_energy":       0.90,   # CONFLICT: high energy but sad mood
        "target_valence":      0.20,   # very sad/dark (contradicts ambient genre)
        "target_danceability": 0.85,   # high danceability but wants sad/dark ambient
        "target_acousticness": 0.80,   # acoustic + ambient + high energy = unusual combo
        "preferred_language":  "English",
        "preferred_era":       "2026",
    },

    "niche_acoustic_fast": {
        "favorite_genre":      "folk",
        "favorite_mood":       "peaceful",
        "target_energy":       0.85,   # peaceful folk usually low energy - testing contradiction
        "target_valence":      0.72,   # slightly happy
        "target_danceability": 0.45,   # not very danceable
        "target_acousticness": 0.95,   # very acoustic (extreme)
        "preferred_language":  "Spanish",
        "preferred_era":       "2010-20",
    },

    "extreme_electronics": {
        "favorite_genre":      "electronic",
        "favorite_mood":       "euphoric",
        "target_energy":       0.98,   # near maximum energy
        "target_valence":      0.95,   # maximum happiness
        "target_danceability": 0.99,   # maximum danceability
        "target_acousticness": 0.02,   # nearly zero acoustic (pure electronic)
        "preferred_language":  "English",
        "preferred_era":       "2026",
    },

    "obscure_language_niche": {
        "favorite_genre":      "classical",
        "favorite_mood":       "meditative",
        "target_energy":       0.30,   # very low
        "target_valence":      0.65,   # slightly positive
        "target_danceability": 0.35,   # not danceable
        "target_acousticness": 0.95,   # very acoustic
        "preferred_language":  "Hindi",  # tests non-English, non-Nepali
        "preferred_era":       "2025",
    },

    "high_energy_sad": {
        "favorite_genre":      "hiphop",
        "favorite_mood":       "intense",
        "target_energy":       0.95,   # extremely high energy
        "target_valence":      0.25,   # very sad/dark despite high energy
        "target_danceability": 0.80,   # danceable but dark
        "target_acousticness": 0.05,   # very electronic
        "preferred_language":  "English",
        "preferred_era":       "2025",
    },
}


# ─── Formatting Helpers ───────────────────────────────────────────────────────

def format_score_output(rank: int, song: dict, score: float, explanation: str) -> str:
    """
    Formats a single recommendation into a clean, readable block.
    Shows rank, song metadata, total score, and detailed scoring reasons.
    """
    lines = []

    # Header: rank, title, artist
    lines.append(f"  #{rank}  {song['title']}")
    lines.append(f"       Artist: {song['artist']} | Genre: {song['genre']} | Era: {song['era']}")

    # Score
    lines.append(f"       Score: {score:.2f}/17.5")

    # Reasons (with better indentation and grouping)
    lines.append(f"")
    lines.append(f"       Why recommended:")
    for reason_line in explanation.split("\n"):
        # Indent and format each reason
        lines.append(f"         • {reason_line}")

    return "\n".join(lines)


def format_profile_header(profile_name: str, user_prefs: dict) -> str:
    """
    Formats the profile header showing the user's taste preferences.
    """
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append(f"  PROFILE: {profile_name.upper()}")
    lines.append("=" * 72)
    lines.append(f"  Genre: {user_prefs['favorite_genre']} | Mood: {user_prefs['favorite_mood']} | Language: {user_prefs['preferred_language']} | Era: {user_prefs['preferred_era']}")
    lines.append(f"  Energy: {user_prefs['target_energy']:.2f} | Valence: {user_prefs['target_valence']:.2f} | Danceability: {user_prefs['target_danceability']:.2f} | Acousticness: {user_prefs['target_acousticness']:.2f}")
    lines.append("")

    return "\n".join(lines)


# ─── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    csv_path = Path(__file__).parent.parent / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    print(f"\n{'=' * 72}")
    print(f"  MUSIC RECOMMENDER SIMULATION - Loaded {len(songs)} songs")
    print(f"{'=' * 72}\n")

    for profile_name, user_prefs in PROFILES.items():
        print(format_profile_header(profile_name, user_prefs))

        recommendations = recommend_songs(user_prefs, songs, k=3)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(format_score_output(rank, song, score, explanation))
            print()

    print("\n" + "=" * 72)
    print("  Analysis: Do the recommendations match the profile preferences?")
    print("=" * 72 + "\n")


if __name__ == "__main__":
    main()
