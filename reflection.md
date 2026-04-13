# Music Recommender Evaluation & Reflection

## Overview
This document tracks the evaluation of the music recommender system through stress testing with diverse and adversarial user profiles. The system uses a weighted scoring approach that combines exact matches (language, era) with distance-based scoring for numeric features (energy, valence, danceability, acousticness).

---

## Test Results Summary

### Standard Profiles (Expected Strong Performance)

**1. chill_lofi vs. intense_rock: Complete Differentiation**
- **chill_lofi top result:** Midnight Coding (15.87/17.5) — lofi, 0.40 energy, 0.75 acousticness
- **intense_rock top result:** Storm Runner (15.93/17.5) — rock, 0.91 energy, 0.10 acousticness
- **Analysis:** The system successfully separates these completely different tastes. Users preferring low-energy acoustic music get fundamentally different recommendations than users seeking high-energy electric music. The energy gap (0.52 difference) and acousticness gap (0.65 difference) ensure no overlap.

**2. nepali_pop_happy: Language as Hard Constraint Works**
- **Top 3 all score 15.86–15.93/17.5** (nearly identical)
- All recommend Nepali pop songs from 2026
- **Analysis:** The language requirement (+3.0 for match, -0.5 for mismatch) effectively filters the catalog. Only Nepali songs dominate because the language bonus is so strong. This is intentional design but raises questions about language diversity (see Bias section).

**3. romantic_rnb: Mood Mismatch Detected Accurately**
- Top pick: Heartbeat (15.95/17.5) — perfect match (romantic mood, rnb genre, 2026)
- Second pick: Midnight Vibes (13.26/17.5) — mood mismatch (moody vs romantic) causes -0.1 penalty, plus lower valence (0.52 vs 0.80 target) = -0.72 compared to top pick
- **Analysis:** The system correctly identifies that emotional tone (mood + valence) matters. Mood is a soft category that allows substitution but still penalizes distance.

---

### Edge Case Profiles (System Challenges)

**4. conflicting_preferences: Ambiguous Preferences → Lower Scores**
- **Target:** ambient genre, sad mood (0.20 valence), HIGH energy (0.90), HIGH danceability (0.85), very acoustic (0.80)
- **Top result:** Metal Storm (9.91/17.5) — only 57% of max score
- **Why it struggles:** 
  - Energy + valence mismatch: wants 0.90 energy but 0.20 valence. High energy songs are typically happy (high valence). Metal Storm has 0.94 energy and 0.35 valence—better but not aligned.
  - Acousticness contradiction: wants 0.80 acoustic but high energy (0.90). Acoustic instruments are usually soft/low energy. Best match (Metal Storm) has only 0.05 acousticness.
  - No "sad ambient + danceable" songs exist in the dataset.
- **Insight:** The recommender cannot resolve inherent contradictions in user preferences. It picks the best available compromise but scores are mediocre.

**5. niche_acoustic_fast: Rare Language + Energy Contradiction**
- **Target:** folk, peaceful mood, Spanish language, 2010-20 era, HIGH energy (0.85)
- **Top result:** Coffee Shop Stories (10.07/17.5) — 57.5% of max score
- **Why it struggles:**
  - Only 2 Spanish songs in dataset (Coffee Shop Stories, Baila Fuego). Neither is folk or peaceful.
  - Energy-mood mismatch: peaceful mood usually has low energy (0.3-0.5), but this user wants 0.85 energy.
  - Era mismatch: Only one folk song matches the era (Spanish one doesn't); the folk matches are in 2020-25, not 2010-20.
- **Insight:** Rare language + rare mood + era combo = limited catalog support. The system defaults to language match over mood match, revealing the weighting hierarchy.

**6. extreme_electronics: Feature Extremes Possible but Imperfect**
- **Target:** electronic, euphoric, 0.98 energy, 0.95 valence, 0.99 danceability, 0.02 acousticness
- **Top result:** Cyberpunk (13.10/17.5) — 75% of max score
- **Why it's decent but not perfect:**
  - Energy (0.89 vs 0.98), valence (0.68 vs 0.95), danceability (0.83 vs 0.99) all miss extremes.
  - No song in the dataset perfectly matches "euphoric" mood + electronic (Cyberpunk is "futuristic" not "euphoric").
  - Acousticness is far off (0.08 vs 0.02 target) because electronic songs in the data still have some acoustic elements.
- **Insight:** The dataset doesn't have songs with extreme feature values in all dimensions simultaneously.

**7. obscure_language_niche: Perfect Niche Match Exists!**
- **Target:** classical, meditative, Hindi, 2025, 0.30 energy, 0.95 acousticness
- **Top result:** Raag Nights (15.73/17.5) — 90% of max score
- **Why it succeeds:**
  - Exact match on language (Hindi), era (2025), genre (classical), mood (meditative).
  - All numeric features align: 0.35 energy (vs 0.30 target), 0.88 acousticness (vs 0.95 target).
- **Insight:** When a perfect niche exists in the catalog, the recommender finds it. This validates that the system works for minority tastes *if the data supports them*.

**8. high_energy_sad: Emotion-Energy Contradiction Partially Resolved**
- **Target:** hiphop, intense mood, 0.95 energy, 0.25 valence (very sad/dark)
- **Top result:** Anxiety (15.32/17.5) — 88% of max score
- **Why it works better than conflicting_preferences:**
  - "Intense" mood is less inherently contradictory with high energy than "sad ambient + danceable."
  - HipHop genre supports dark themes (unlike ambient, which is usually peaceful).
  - Anxiety's 0.48 valence is closer to 0.25 target than most songs in dataset.
- **Insight:** Some contradictions are less severe than others. Genre choice can mediate energy-emotion mismatches.

---

## Key Findings: What the System Gets Right & Wrong

### ✅ Strengths

1. **Exact Category Matching Works Reliably**
   - Language and era exact matches provide a strong filtering mechanism.
   - Users with specific language preferences consistently get relevant results.

2. **Clear Differentiation Between Opposites**
   - chill_lofi and intense_rock recommendations are completely different.
   - The system respects large gaps in numeric features (energy, acousticness).

3. **Transparent Explanations**
   - Every recommendation includes a detailed breakdown of why it scored highly.
   - Users can immediately understand if genre, mood, or numeric features drove the choice.

4. **Distance-Based Scoring Captures Nuance**
   - Mood mismatches (romantic vs moody) are detected and penalized.
   - Numeric features reward proximity, not exact matching, which is realistic.

### ❌ Limitations & Biases

1. **Language Dominates: Creates "Filter Bubbles"**
   - Language weighting (+3.0 match, -0.5 mismatch) is so strong that it overrides all other preferences.
   - niche_acoustic_fast's top recommendation is Spanish (matching language) but neither folk nor peaceful—it's jazz.
   - **Impact:** Non-English speakers get very limited results. If their language has few songs in the dataset, recommendations are generic.
   - **Unfairness:** Two users with identical music tastes but different languages get completely different recommendations.

2. **Contradictory Preferences Aren't Well-Handled**
   - The system cannot recognize that "high energy + sad" or "peaceful + fast" are contradictions.
   - It picks the best compromise but scores are ~50-60% of maximum, leaving users unsatisfied.
   - **Impact:** Users with non-standard taste combinations see poor recommendations.

3. **Limited Dataset Reveals Gaps**
   - No Spanish folk songs (niche_acoustic_fast gets jazz as closest).
   - Only 2 Hindi songs total (obscure_language_niche gets lucky with one perfect match).
   - No "euphoric electronic" song exists (extreme_electronics gets "futuristic" instead).
   - **Impact:** Users from underrepresented languages/genres get lower-quality recommendations.

4. **Mood Weight Might Be Too Low (2.0 vs Genre 2.5)**
   - Mood is subjective and important but scores less than genre.
   - In some results, genre mismatch is acceptable if era/language/energy align, which feels wrong.
   - **Example:** Storm Runner (intense, rock, high energy) might be recommended to someone who said "intense hiphop" if the language/era matched strongly enough.

5. **No Diversity Mechanism**
   - Top 3 recommendations for nepali_pop_happy are nearly identical (15.86-15.93/17.5) scores.
   - All three are Nepali pop songs from 2026. There's no encouragement to show variety.
   - **Impact:** Users see repetitive recommendations instead of exploring breadth within their taste.

---

## Surprising Discoveries

1. **Language Is a Super-Weight:** I expected genre to be most important, but language dominance caught me off guard. A Spanish-language jazz song beats an English-language folk song for a Spanish-speaker looking for folk. This suggests the weighting should be configurable by region.

2. **"Intense" Works Across Genres:** high_energy_sad succeeds partly because "intense" is flexible enough to work in hiphop, rock, and metal. Other moods (peaceful, romantic) are more genre-specific, making the system less universal.

3. **Extreme Values Are Rare:** conflicting_preferences and extreme_electronics reveal that no song has 0.98 energy + 0.99 danceability + 0.02 acousticness. Real datasets have tradeoffs. Recommendations score lower when users want impossible combinations.

4. **Niche Recommendations Can Be Perfect:** When a perfect match exists (Raag Nights for classical_hindi_meditative), the system finds it reliably. The problem isn't the algorithm—it's that the dataset is small and skewed toward pop/English.

---

## Bias & Fairness Issues

### Issue 1: Language-Based Segregation
- Nepali speakers only see Nepali songs (12 in dataset).
- Spanish speakers only see 2 Spanish songs.
- English speakers see the full catalog (most songs).
- **Fairness concern:** This system disadvantages minority-language speakers with fewer catalog options. A real system should recommend high-quality songs across languages based on audio features, not just language match.

### Issue 2: Genre Overrepresentation
- Pop songs dominate the dataset (~25 songs out of 60).
- Rock, hiphop, electronic each ~5-8 songs.
- Classical, folk, jazz each <5 songs.
- **Fairness concern:** Pop users get more variety and better matches. Classical users get generic recommendations because there's only 1 classical song (Raag Nights).

### Issue 3: Contradictory Profiles Aren't Supported
- The system assumes users have "consistent" tastes (e.g., high energy + happy, or low energy + peaceful).
- Users who want "high energy but dark" (metal fans, for example) get suboptimal recommendations.
- **Fairness concern:** Niche emotional expressions are treated as bugs instead of valid user types.

### Issue 4: Numeric Feature Extremes Are Unrealistic
- Users who want 0.99 danceability or 0.02 acousticness will be disappointed because no songs exist at those extremes.
- This isn't the recommender's fault, but the system doesn't gracefully degrade to "here's the closest match, but it's not perfect."
- **Fairness concern:** Users don't know if low scores mean poor taste compatibility or dataset limitations.

---

## Weight Sensitivity Experiment Results

**Test:** Doubled energy weight (2.0 → 4.0) and halved genre weight (2.5 → 1.25)

**chill_lofi Profile:**
- Original top 5: Midnight Coding, Spacewalk Thoughts, Library Rain, Winter Walk, Slow Motion
- Modified top 5: Midnight Coding, Spacewalk Thoughts, Library Rain, Winter Walk, **Gentle Breeze**
- **Result:** Rankings CHANGED - songs matching target energy (0.40) more aggressively ranked higher
- **Insight:** The weight experiment proves energy sensitivity works. Gentle Breeze (0.45 energy) entered top 5 because energy reward nearly doubled.

**intense_rock Profile:**
- Original top 5: Storm Runner, Warrior, Rooftop Lights, Metal Storm, Anxiety
- Modified top 5: Storm Runner, Warrior, Metal Storm, Rooftop Lights, Anxiety
- **Result:** Top 5 unchanged, but Metal Storm moved up (position 3→5) because it has higher energy (0.94 vs 0.92 target)
- **Insight:** Genre, language, and era matches are SO STRONG that doubling energy weight doesn't change top 3. Language/era bonuses (+6.0) dominate energy bonus (max +4.0).

**Key Finding:** The weighting hierarchy is robust for language/era, but sensitive to energy. If you want to shift preferences (e.g., "prioritize energy over genre"), the math works—but language/era are hard constraints that override almost everything else.

---

## Recommendations for Improvement

1. **Make Language Weighting Configurable:** Allow users to opt out of strict language matching or weight it lower than other preferences.
2. **Add Diversity Sampling:** Don't just return top-k by score; sample from top 20% to increase variety.
3. **Detect and Flag Contradictions:** If a user requests conflicting preferences, explain the tradeoff.
4. **Expand Dataset:** Especially non-English, non-pop genres.
5. **Add a Confidence Score:** Tell users "this is a good match (90%)" vs. "this is the best available, but your preferences are rare (55%)."
6. **Reconsider Language Weight:** +3.0 for language match may be too strong. Consider dropping to +2.0 to allow genre/mood to compete.

---

## Conclusion

The recommender system excels at matching users with clear, aligned preferences. It fails gracefully for contradictory preferences but doesn't explain why. The biggest risk is **bias toward majority languages and genres**—the system treats language and genre as hard filters rather than soft signals, which disadvantages users from underrepresented groups. For a classroom project, this is acceptable. For a real product, it would need to balance precision (exact matches) with equity (supporting diverse users).
