# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatcher 2.0** — A transparent, rule-based music recommender that prioritizes exact matches on language and era, combined with distance-based scoring on audio features.

---

## 2. Intended Use  

**What it does:** This system recommends 3-5 songs from a 60-song catalog based on an explicit user taste profile (preferred genre, mood, energy level, etc.). Every recommendation includes a breakdown of why it was chosen.

**Who it's for:** Primarily educational exploration and classroom discussion of how recommender systems work. Not intended for real users—the catalog is too small and skewed toward English and pop music.

**Key assumptions:**
- Users can articulate their preferences (genre, mood, energy target, etc.)
- Music is best characterized by discrete audio features (energy, valence, danceability, etc.)
- Exact matches on language and era are the highest priority
- Recommendations should be fully explainable

---

## 3. How the Model Works  

**The Basic Idea:** The recommender asks a user "What's your favorite genre, mood, energy level?" Then it scores every song by how closely it matches those preferences, and returns the top 5.

**Scoring System (in order of importance):**

1. **Language (3.0 points if match, -0.5 if mismatch):** A strong filter. The system heavily favors songs in the user's preferred language.
2. **Era (3.0 points if match, -0.3 if mismatch):** Another strong filter. Users who want 1970s rock won't see 2020s pop.
3. **Genre (2.5 points if match, -0.2 if mismatch):** Categorical preference. Rock fans see rock, but if no rock songs match other criteria, jazz is a weak backup.
4. **Mood (2.0 points if match, -0.1 if mismatch):** Emotional tone. A happy pop song and a sad pop song are both pop, but they're different moods.
5. **Energy, Valence (happiness), Danceability, Acousticness:** Distance-based scoring. If a user wants 0.40 energy, a song with 0.42 energy scores better than one with 0.80 energy. The closer, the better.

**Total possible score:** 17.5 points

**Example:** A song gets +3 for matching language (English), +3 for matching era (2026), +2.5 for matching genre (pop), +2.0 for matching mood (happy), and then up to +2.0 + 1.5 + 1.0 + 1.0 = 5.5 for numeric features. If energy is 0.82 and the user wants 0.82, they get +2.0 for energy. If danceability is 0.80 and the user wants 0.80, they get +1.0 for danceability. Etc.

**What changed from starter:** No changes—we used the exact scoring provided in the starter code.

---

## 4. Data  

**Dataset Size:** 60 songs

**Language Breakdown:**
- English: 48 songs (80%)
- Nepali: 8 songs (13%)
- Spanish: 2 songs (3%)
- Hindi: 2 songs (3%)

**Genre Breakdown:**
- Pop: ~25 songs (42%)
- Rock: ~4 songs
- HipHop: ~4 songs
- Electronic/EDM: ~4 songs
- Lofi/Ambient/Jazz: ~4 songs
- Classical, Folk, RnB, Soul, Funk, etc.: <5 songs each

**Era Breakdown:**
- 2020-25: ~20 songs
- 2026: ~22 songs
- 2025: ~10 songs
- 2010-20: ~8 songs

**Mood/Emotional Range:** The dataset includes "happy," "chill," "intense," "moody," "romantic," "peaceful," "euphoric," etc. But some emotions are rare (only 1 song is "meditative," only 1 is "futuristic").

**Did we add/remove data?** No modifications to the starter dataset.

**What's missing?**
- Non-English music (only 12 non-English songs vs. 48 English)
- Niche genres (classical, jazz, folk have <5 examples)
- Rare moods (euphoric, meditative, futuristic each have 1-3 examples)
- Extreme feature values (no song has 0.98 energy AND 0.99 danceability AND 0.02 acousticness simultaneously)

---

## 5. Strengths  

1. **Clear Differentiation Between Opposite Tastes:** A user who wants low-energy, high-acousticness music (chill_lofi) gets completely different recommendations than a user who wants high-energy, low-acousticness music (intense_rock). The system correctly separates them.

2. **Language Filtering Works:** Hindi speakers interested in classical music get Raag Nights (classical, Hindi, meditative) as their top pick with a 15.73/17.5 score. When preferences align, the system finds near-perfect matches.

3. **Transparent Explanations:** Every recommendation includes a detailed breakdown: "You got +3.0 for language match, +2.5 for genre match, +1.96 for energy closeness." Users understand *why* they saw a song.

4. **Accurate Mood Detection:** The system correctly identifies mood mismatches. A user who wants "romantic" RnB will score a "moody" RnB song lower (13.26 vs 15.95) because the mood doesn't match (+2.0 vs -0.1).

5. **Numeric Sensitivity:** Doubling the energy weight causes observable ranking changes (Gentle Breeze enters the top 5 for chill_lofi). The math is sound.

---

## 6. Limitations and Bias 

### Critical Bias: Language-Based Segregation

**The Problem:** Language weighting (+3.0) is so strong that it completely overrides genre and mood preferences. A Nepali speaker loses access to 48 English songs, even if a high-quality English folk song matches their taste better than any available Nepali song.

**Evidence:** In the niche_acoustic_fast profile, we asked for Spanish folk and got Spanish jazz (Coffee Shop Stories, 10.07/17.5) instead of English folk (Acoustic Sunrise, 8.30/17.5). The system chose language match over genre/mood match.

**Real-World Impact:** Non-English speakers see fewer recommendations because the catalog is 80% English. If a user's language has only 2 songs (like Spanish), they get poor variety even if those 2 songs are decent matches.

### Critical Bias: Genre Overrepresentation

**The Problem:** Pop music dominates (42% of catalog) while classical, folk, and jazz are underrepresented (<5 songs each). Users who like pop see more variety; users who like classical get mediocre recommendations because few options exist.

**Evidence:** The extreme_electronics profile wanted "euphoric" electronic music. No song in the dataset is tagged "euphoric" in the electronic genre. The best match (Cyberpunk) is "futuristic," not "euphoric," and scores only 75% of max (13.10/19.0).

### Limitation: Contradictory Preferences Aren't Handled

**The Problem:** The system doesn't recognize when preferences are contradictory (e.g., high energy + sad/dark mood, or peaceful + fast tempo). It picks the best compromise but scores are low (~50-60% of max).

**Evidence:** The conflicting_preferences profile (wants high energy + low valence/sad) gets Metal Storm with only 9.91/17.5 (57% of max). The system picked high energy but sacrificed valence matching.

### Limitation: No Diversity Mechanism

**The Problem:** The top 3 recommendations for nepali_pop_happy are nearly identical (15.86–15.93 scores). All three are Nepali pop songs from 2026. There's no mechanism to suggest variety within a user's taste.

**Real-World Impact:** Users see repetitive recommendations instead of exploring breadth. If someone likes Nepali pop, showing 3 nearly-identical songs is less useful than showing the best Nepali pop plus a high-quality alternative (e.g., a Nepali indie song, or English pop with Nepali vocals).

### Limitation: Small & Skewed Dataset

**The Problem:** 60 songs is tiny. Real Spotify has millions. Our dataset is skewed: 80% English, 42% pop, 2020-26 eras dominate.

**Real-World Impact:** Niche tastes (Spanish folk, classical music, 1990s rock) can't be well-served. Users in minority language groups will be disappointed.

---

## 7. Evaluation  

### Profiles Tested

We ran the recommender against **8 distinct user profiles:**

1. **chill_lofi** (baseline) - lofi, low energy, high acousticness, English, 2020-25
2. **intense_rock** (baseline) - rock, high energy, low acousticness, English, 2010-20
3. **nepali_pop_happy** (baseline) - pop, happy, Nepali, 2026
4. **romantic_rnb** (baseline) - RnB, romantic, English, 2026
5. **conflicting_preferences** (edge case) - wants high energy BUT sad mood + very acoustic (contradictory)
6. **niche_acoustic_fast** (edge case) - wants peaceful folk but high energy (contradictory) + rare Spanish + 2010-20 era
7. **extreme_electronics** (edge case) - wants extreme feature values (0.98 energy, 0.99 danceability, 0.02 acousticness)
8. **high_energy_sad** (edge case) - wants high energy but dark mood (tested how well system handles emotional contradictions)

### What We Looked For

- **Accuracy:** Do the recommendations match the profile's stated preferences? (e.g., does intense_rock get rock songs, and chill_lofi get low-energy songs?)
- **Surprises:** Are there cases where the system picks songs that seem wrong? Or cases where language/era override more important preferences?
- **Robustness:** Does doubling energy weight change recommendations? (Yes, it does for chill_lofi but not for intense_rock.)
- **Bias:** Do different languages/genres get equal treatment? (No—English and pop are favored.)

### Key Findings

| Profile | Top Score | Finding |
|---------|-----------|---------|
| chill_lofi | 15.87/17.5 | Perfect match (lofi, chill, low energy) |
| intense_rock | 15.93/17.5 | Perfect match (rock, intense, high energy) |
| nepali_pop_happy | 15.93/17.5 | Excellent but repetitive (all 3 top results are nearly identical) |
| romantic_rnb | 15.95/17.5 | Excellent; mood mismatch in #2 correctly penalized |
| conflicting_preferences | 9.91/17.5 (57%) | Poor—system can't reconcile "sad ambient with high energy" |
| niche_acoustic_fast | 10.07/17.5 (57%) | Weak—language + era + mood + genre combo too rare in data |
| extreme_electronics | 13.10/19.0 (75%) | Decent but not perfect—no "euphoric electronic" song exists |
| high_energy_sad | 15.32/17.5 (88%) | Works better than conflicting_preferences—"intense" emotion bridges the gap |

### Weight Sensitivity Test

We doubled energy weight (2.0 → 4.0) and halved genre weight (2.5 → 1.25). Results:
- **chill_lofi:** Rankings CHANGED (Gentle Breeze entered top 5 due to better energy match)
- **intense_rock:** Rankings UNCHANGED (language/era bonuses were too strong to override)

**Conclusion:** The weighting system is mathematically sound and responsive to changes, but language/era are overwhelming hard constraints.

### Surprising Discoveries

1. **Language Weight Dominates:** We expected genre to be most important. Instead, language (+3.0) is equally weighted with era, making it nearly impossible for a Spanish speaker to get English recommendations even if they're objectively better matches.

2. **Contradictions Matter:** high_energy_sad (0.95 energy, 0.25 valence) performed better than conflicting_preferences (0.90 energy, 0.20 valence) because HipHop culture accepts dark themes. Ambient music typically doesn't. Genre context affects how contradictory a profile is.

3. **Niche Matches Can Be Perfect:** When a profile matches available data (like Hindi+classical+meditative), the system finds it reliably and scores 90% of max. The problem isn't the algorithm—it's that the dataset is small and skewed.

---

## 8. Future Work  

1. **Configurable Language Weight:** Let users opt into cross-language recommendations. Some users might prefer "best quality regardless of language" over strict language matching.

2. **Add Diversity Sampling:** Instead of returning top-k by score, sample from the top 20-30% to increase variety.

3. **Expand Dataset:** Especially non-English, non-pop music. Include more classical, folk, jazz, and regional music.

4. **Detect & Explain Contradictions:** If a user requests incompatible preferences, say "You want high energy but sad mood—these are unusual together. Here's the best compromise, but consider this alternative."

5. **Add Confidence Intervals:** "This is a 92% match" vs. "This is the best available, but your preferences are rare (54% match)." Help users understand if low scores mean poor taste fit or dataset limitations.

6. **Support Multi-Language Preference:** "I want songs in English, Spanish, or Nepali" instead of forcing a single language.

7. **Implement Diversity Rewards:** Penalize repetitive top-k results. If two songs are very similar, boost the underrepresented one.

---

## 9. Personal Reflection  

**What I Learned About Recommender Systems:**

Building this system revealed that recommendation is fundamentally a *trade-off* problem. You can't optimize for language specificity, genre accuracy, mood matching, AND numeric feature precision simultaneously. Real systems like Spotify make these choices implicitly—they might prioritize song quality over language match, or diversity over perfect personalization. This system made them explicit, which helps explain why real recommenders sometimes suggest something unexpected.

**What Surprised Me:**

I was surprised by how powerfully language weighting dominates the system. A Nepali speaker can't escape Nepali songs because the language bonus (+3.0) is as large as the era bonus, and both combine to outweigh genre entirely. In a real system, I'd expect language to be a soft preference, not a hard filter. This revealed a design choice: *do you optimize for the user's stated language, or for the quality of the recommendation?* There's no single right answer, but it matters enormously.

I was also surprised that contradictory preferences (high energy + sad mood) could be partially salvaged by choosing the right genre (HipHop works; ambient doesn't). This suggests that *genre itself encodes emotional norms*. The system doesn't explicitly model that, but it emerges from the data.

**How This Changed My View of Music Recommenders:**

Before building this, I thought music recommenders were "black boxes" that somehow understood taste. Now I see they're *explicit trade-offs* between many competing signals: language, genre, mood, and numeric features all fighting for weight. The system's biases are legible here—language dominates—but in Spotify or YouTube Music's million-parameter neural nets, the biases are hidden. That's scary. A hidden bias is worse than an explicit one, because you can't even question it. Building this transparent system made me appreciate why explainability matters. Users should know *why* they saw a song, so they can push back if the system is wrong for them.

Also, I realized how much bias comes from *dataset composition*, not the algorithm. The algorithm is fair—it applies the same math to every song. But because the dataset is 80% English and 42% pop, the algorithm inevitably favors those. A real Spotify would have the same problem if their training data is skewed. The bias isn't a bug; it's a *data quality* problem.

**How AI Tools Helped (and When to Double-Check):**

*What worked well:*
- **Code generation:** Claude helped scaffold the data loading, scoring functions, and CLI formatting quickly. The functions Claude generated were correct and followed good Python patterns.
- **Documentation:** Claude helped structure the README, model card, and this reflection. Having an AI review and organize findings saved hours.
- **Testing strategy:** Claude suggested the 8-profile approach (4 baseline + 4 edge cases) which revealed biases I might have missed.
- **Data generation:** Claude generated 50 realistic songs from web search results about 2026 music trends.

*Where I needed to double-check:*
- **Feature values:** Claude sometimes generated audio features (energy, valence, etc.) that seemed plausible but might not match real songs. I spot-checked by running scenarios and adjusting outliers.
- **Weights and scores:** The scoring algorithm was provided in the starter code, not generated by Claude, so I verified it matched the logic.
- **Bias identification:** Claude suggested language bias as a problem. I tested this manually by running the niche_acoustic_fast profile to confirm the hypothesis was correct.
- **Contradictory profiles:** Claude suggested testing conflicting preferences (high energy + sad mood). I verified by running it and checking scores (9.91/17.5 confirmed the issue).

*Key lesson:* AI tools excel at structure, scaling, and documentation. But domain-specific validation (does this feature value match reality? is this bias actually a problem?) requires human judgment. I trusted the overall approach but verified critical findings manually.

**What Would I Try Next?**

If I extended this project, I'd:
1. **Test with user studies** — Show recommendations to real people and ask "Does this feel right?" The score alone doesn't prove the system is *good*.
2. **Implement filtering options** — Let users disable the language filter or increase diversity. Give them control over the trade-offs.
3. **Build a larger, more balanced dataset** — The current 60 songs is a proof-of-concept. A realistic version would have thousands of songs across all genres and languages.
4. **Add listening context** — Real recommenders know the time of day (morning ≠ late night), whether you're working, exercising, or socializing. This system ignores context.
5. **Track what users actually listen to** — So far, we only scored based on stated preferences. Real systems learn from behavior (clicks, skips, repeat plays). That feedback loop is crucial.

---

## Summary

**VibeMatcher 2.0** successfully demonstrates how a simple, rule-based recommender can:
- ✅ Provide transparent, explainable recommendations
- ✅ Differentiate between different user tastes
- ✅ Scale a scoring function across a full catalog
- ✅ Reveal hidden biases in both data and design choices

**But it also shows the limits:**
- ❌ Language weighting is too aggressive and segregates users
- ❌ Small datasets make it hard to serve niche tastes
- ❌ No diversity mechanism leads to repetitive suggestions
- ❌ No way to handle contradictory preferences gracefully

The biggest insight: **recommendation systems are exercises in explicit trade-off design**. Every weight, every parameter is a human choice. Those choices reveal assumptions about what matters and who the system is optimized for. In this case, the choices optimized for English speakers and pop music fans. A fair system would be aware of that and either balance the dataset or give users control over the weights.

This is why explainability and transparency matter. Users deserve to know *why* they saw what they saw, so they can question it.
