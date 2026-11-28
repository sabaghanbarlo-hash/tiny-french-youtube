# Tiny French - YouTube plan (Nov 2026 start)

Goal for month 1: get a clean, consistent beginner channel on the air, then learn from real numbers.

## Weekly rhythm (7 uploads a week)

| Day | Time (UTC / US Eastern) | What |
|---|---|---|
| Sunday | 15:00 / 10:00 | **Story** (Adrien and Marinette act out a scene, then vocab, grammar, quiz) |
| Tuesday | 15:00 / 10:00 | **Lesson** (core beginner topic, 4-6 min) |
| Monday | 23:00 / 18:00 | **Short** |
| Wednesday | 23:00 / 18:00 | **Short** |
| Thursday | 23:00 / 18:00 | **Short** |
| Friday | 22:00 / 17:00 | **Short** |
| Saturday | 16:00 / 11:00 | **Short** |

So per week: 5 Shorts, 1 Story, 1 Lesson. (Tiny Japanese runs Mon/Wed/Fri long plus a daily Short. Tiny French starts lighter on purpose: 2 long videos a week is enough until there is data, and every video stays beginner level.)

## Why these choices

- **Shorts do the discovering, long videos keep people.** On Tiny Japanese after about two weeks, the one "Stop saying just Arigatou, say thank you politely" Short has about 1,000 views; the story and hiragana videos have 0-10. In the French niche the biggest 2026 breakouts are also 8-30 second Shorts with a "polite vs rude" or "say it correctly" hook (e.g. Talk in French "Sorry from polite to rude", about 10.8M views against a normal 4.9K).
- **Long videos that work for beginners** are A1 stories with subtitles (Easy French Mastery's A1 story videos run about 4-16x their channel median) and "how to introduce yourself" style lessons (Comme une Francaise, about 21x).
- **Times.** Buffer's analysis of 1.8M YouTube videos puts the best long-form slot on Sunday around 10:00 and weekday mornings, and Shorts on Friday late afternoon/evening and Saturday 11:00. Times above are anchored to US Eastern because that is where most English-speaking French learners are. These are starting guesses, not facts about your audience: after 3-4 weeks check YouTube Studio > Analytics > Audience > "When your viewers are on YouTube" and move the times.

## Short hook formulas (the pattern behind the winners)

1. "Stop saying X! Say this instead" (thank you, goodbye, hello)
2. "Polite vs rude" (je veux vs je voudrais)
3. "How to say ___" for a situation (no, I don't understand, where is the toilet)
4. "French you'll hear at ___" (cafes)
5. "Don't say ___" for a classic mistake (je suis chaud)

Every Short: 4-6 lines of dialogue, 2-3 phrases, one quiz question, about 30-45 seconds.

## Calendar: November 2026

| Date | Time | Type | Video |
|---|---|---|---|
| Sun Nov 01 | 15:00 UTC / 10:00 ET | Story | Ep.1 A Rainy Day in Paris (already uploaded) |
| Mon Nov 02 | 23:00 UTC / 18:00 ET | Short | 3 French Phrases for the Bakery (already uploaded) |
| Tue Nov 03 | 15:00 UTC / 10:00 ET | Lesson | Greetings Through the Day |
| Wed Nov 04 | 23:00 UTC / 18:00 ET | Short | Stop Saying Just “Merci”! 3 Ways to Say Thank You in French |
| Thu Nov 05 | 23:00 UTC / 18:00 ET | Short | How to Say “I Don't Understand” in French (3 Useful Phrases) |
| Fri Nov 06 | 22:00 UTC / 17:00 ET | Short | Polite vs Rude: How to Say “I Want” in French (Not Je Veux!) |
| Sat Nov 07 | 16:00 UTC / 11:00 ET | Short | Bonjour or Salut? Don't Say the Wrong Hello in French |
| Sun Nov 08 | 15:00 UTC / 10:00 ET | Story | A Day at the Fun Fair |
| Mon Nov 09 | 23:00 UTC / 18:00 ET | Short | How to Say “No” in French Without Sounding Rude |
| Tue Nov 10 | 15:00 UTC / 10:00 ET | Lesson | Introducing Yourself |
| Wed Nov 11 | 23:00 UTC / 18:00 ET | Short | 3 French Phrases You'll Hear at Every Café (Understand Them!) |
| Thu Nov 12 | 23:00 UTC / 18:00 ET | Short | Count to 10 in French in 20 Seconds |
| Fri Nov 13 | 22:00 UTC / 17:00 ET | Short | Don't Say “Je Suis Chaud”! Say This Instead in French |
| Sat Nov 14 | 16:00 UTC / 11:00 ET | Short | 3 Ways to Say “You're Welcome” in French (Not Just De Rien) |
| Sun Nov 15 | 15:00 UTC / 10:00 ET | Story | A Walk in Paris |
| Mon Nov 16 | 23:00 UTC / 18:00 ET | Short | 3 Ways to Say “Excuse Me” in French (Pardon, Excusez-moi…) |
| Tue Nov 17 | 15:00 UTC / 10:00 ET | Lesson | Numbers and Prices |
| Wed Nov 18 | 23:00 UTC / 18:00 ET | Short | How to Ask “Where Is the Toilet?” in French (You'll Need It!) |
| Thu Nov 19 | 23:00 UTC / 18:00 ET | Short | Introduce Yourself in French in 20 Seconds (Beginner Script) |
| Fri Nov 20 | 22:00 UTC / 17:00 ET | Short | How to Compliment Food in French: “C'est Délicieux !” and More |
| Sat Nov 21 | 16:00 UTC / 11:00 ET | Short | Don't Just Say “Au Revoir”! 3 Better Goodbyes in French |
| Sun Nov 22 | 15:00 UTC / 10:00 ET | Story | A Saturday in Town |
| Mon Nov 23 | 23:00 UTC / 18:00 ET | Short | Bonsoir or Bonne Nuit? Don't Say Good Night Too Early in French |
| Tue Nov 24 | 15:00 UTC / 10:00 ET | Lesson | Ordering at the Café |
| Wed Nov 25 | 23:00 UTC / 18:00 ET | Short | Tu or Vous? The Easy Rule for Saying “You” in French |
| Thu Nov 26 | 23:00 UTC / 18:00 ET | Short | How to Ask “Do You Speak English?” in French (Politely!) |
| Fri Nov 27 | 22:00 UTC / 17:00 ET | Short | How to Ask “How Much Is It?” in French (Too Expensive!) |
| Sat Nov 28 | 16:00 UTC / 11:00 ET | Short | How to Say “Cheers!” in French (Santé!) and More |

Weeks 1-4 are all written. Weeks 5+ (December): see "Next" below.

## How the automation works

- `schedule.json` is the single source of truth: every video, its type and its publish time (UTC).
- The **Scheduled publishing** workflow (Actions tab) runs every day at 04:17 UTC. For every video that publishes in the next 5 days it renders the video, uploads it to YouTube as private with a publish time, and YouTube publishes it by itself at that moment. Nothing is public before its time.
- To move a video: change `publish_at` in `schedule.json` (if it was already uploaded, also change it in YouTube Studio). To pause everything: set `"paused": true`. To run it right now: Actions > Scheduled publishing > Run workflow.
- Videos that are already uploaded are skipped (`docs/videos/<name>.youtube.txt`). The scheduler does not commit the rendered .mp4 files to the repo (they are large); the YouTube link, description, subtitles and thumbnail are saved. Set `KEEP_MP4_ON_SITE=1` in the workflow if you want the mp4s on the site too.
- If a render fails the scheduler retries 3 times, then the workflow shows red in Actions and tries again the next day.

## Checkpoints

- **After week 1:** open YouTube Studio. Is each video processing and showing a publish date? Do thumbnails look right?
- **After 3 weeks (about Nov 24):** which 3 Shorts beat the others? Keep that hook formula, write 10 more like it. Which long video kept viewers longest? Adjust Sunday/Tuesday mix.
- Rule of thumb: a Short that gets 2x the channel's usual views is a formula worth repeating; one that gets 0.5x, stop making that kind.

## Next (December)

- Sunday Stories: 4 more directed stories (airport, hotel, a day at school, shopping for a gift).
- Tuesday Lessons: the existing "French sounds" series (fs-01 to fs-07: accents and alphabet, silent letters, nasal vowels, the French u and r...) and the "Everyday French" series (ef-01 to ef-07), re-dated into schedule.json.
- Shorts: another 20, built from whichever hook formulas won in November.

## Things to do by hand (2 minutes)

- Two videos were uploaded before the scheduler existed and are still plain private: **Ep.1 A Rainy Day in Paris** and **3 French Phrases for the Bakery**. In YouTube Studio > Content, open each one > Visibility > Schedule, and pick Sun Nov 1 10:00 ET (Ep.1) and Mon Nov 2 18:00 ET (bakery Short).
- The channel also holds three older private guided-meditation videos from Oct 26. They are private so they do no harm; delete them if you do not want them on a French channel.
- The scheduler uploads new videos private with a publish time, so you do not need to touch the YT_PRIVACY setting.

## Growth update (17 Nov 2026): English-first test and two Shorts a day

Why: Tiny French grows slowly next to Instagram. What the data showed:
- Shorts are 99% of all views (1,517 of about 1,524); the 4 public long videos got 9 views in total; the one "Polite vs Rude" Short is 74% of all views. Check Studio > Analytics > Audience > Geography for the country split.
- In the niche, the Shorts that broke out run 12-40 seconds around one situation or contrast and have English titles. Ours run 59-88 seconds.

What this change does:
- Adds 8 test Shorts (`shorts/20261118-...` to `shorts/20261125-...`), one a day at 15:00 UTC (10:00 ET), as a second daily Short next to the existing 23:00 UTC slot.
- Each opens with an English hook (the narrator voice speaks the English parts), runs about 20-40 seconds and ends with a comment question.
- Sets the upload language to English (`defaultLanguage` and `defaultAudioLanguage` in `upload.py`).
- 21 unpublished long videos moved from `items` to `held_items` in schedule.json (nothing deleted): 20261122-a-saturday-in-town.txt, 20261124-ordering-at-the-cafe.txt, fs-01-accents-and-the-alphabet.txt, fs-02-silent-letters-and-liaison.txt, ef-01-days-and-today.txt, ef-02-telling-the-time.txt .... Move one back into `items` with a new `publish_at` to publish it.
- Lowers `lookahead_hours` from 120 to 48. As far as I know the YouTube API allows about 6 uploads a day per Google project (1,600 units each on a 10,000 default), and a 120-hour window would try about 10 at once.

Checkpoints:
- 24 Nov: share of views outside the home country (Studio > Analytics > Audience > Geography). Keep the English-first openings if 25% or more of views come from outside Japan (Tiny Japanese) or the target countries.
- 1 Dec: median views per format, 10 Shorts each. Keep a format at 3x today's median (about 400 Japanese, 65 French) and above 50% viewed; cut one under 1x.

Not done here: weekly listen-and-repeat compilation videos (needs a new script type); the existing queued Shorts keep their current length and titles; the held lessons are only held back from YouTube, not removed from the repo or the website courses.

## Daily story week (Nov 29 - Dec 5) - added Nov 21, 2026
One new French story every day for a week, on top of the plan above. Scripts are in `stories/`, the calendar entries are in `schedule.json` (kind `story`), and the daily scheduler renders and uploads them like everything else (private + publish time).

| Date (UTC) | UTC | ET | Tehran | Title |
|---|---|---|---|---|
| Sun Nov 29 | 15:00 | 10:00 | 18:30 | Un Pique-nique au Parc |
| Mon Nov 30 | 14:00 | 09:00 | 17:30 | À la Boulangerie |
| Tue Dec 01 | 14:00 | 09:00 | 17:30 | Le Nouveau Voisin |
| Wed Dec 02 | 12:00 | 07:00 | 15:30 | Un Café, S'il Vous Plaît |
| Thu Dec 03 | 12:00 | 07:00 | 15:30 | Le Train de Neuf Heures |
| Fri Dec 04 | 17:00 | 12:00 | 20:30 | Perdue dans Paris |
| Sat Dec 05 | 20:00 | 15:00 | 23:30 | La Première Neige |

**Why these times:** long-form slots from Buffer's July 2026 study of 1.8M videos (Sunday 10:00 ET is the strongest slot of the week; Monday 09:00; weekday mornings; Thursday 17:00; Friday near noon; Saturday afternoon). Each slot is kept at least 4 hours away from the Shorts slots in this plan (22:00-23:00 UTC weekdays, 16:00 UTC Saturday) so long videos and Shorts do not compete. These are starting guesses, not facts about your audience.

**Honest caveat:** earlier in this plan, long videos got about 10 views in total and posting too much split the audience, which is why the other long videos are held. Seven long videos in seven days is an experiment. Check YouTube Studio after the week (views, average view duration, subscribers per video). If the stories do not hold viewers, move them to `held_items` in `schedule.json` or set `"paused": true`.

**Cast:** Marinette/Adrien or Mika/Alex plus Bernard (older neighbour), Pierre (shopkeeper), Camille (clerk). Check any new script before it is scheduled: Actions > "Check stories (no video)" (pattern e.g. `2026*.txt`).

## Extra stories before the story week (Nov 23 - 28) - added Nov 23, 2026
Six more stories, one a day, so every day until the Nov 29 story week has one. Same method as above, but because your Shorts already fill most of these days the story is placed in the gap that is at least 3 hours from every Shorts slot (usually 17:00-20:00 UTC).

| Date (UTC) | UTC | ET | Tehran | Title |
|---|---|---|---|---|
| Mon Nov 23 | 19:00 | 14:00 | 22:30 | Au Marché de Noël |
| Tue Nov 24 | 19:00 | 14:00 | 22:30 | À la Pharmacie |
| Wed Nov 25 | 19:00 | 14:00 | 22:30 | Une Journée avec Adrien |
| Thu Nov 26 | 12:00 | 07:00 | 15:30 | Des Vêtements pour l'Hiver |
| Fri Nov 27 | 17:00 | 12:00 | 20:30 | Ma Famille |
| Sat Nov 28 | 20:00 | 15:00 | 23:30 | Des Crêpes pour Tout le Monde |

Thursday Nov 26 is US Thanksgiving, so US viewing may be lower that day.

## December plan (28 Nov 2026): one more month of Shorts, built from the Nov data

Scripts for **6 Dec - 5 Jan** are in `shorts/` (62 Shorts, two a day at 15:00 UTC and 23:00 UTC) and listed in `schedule.json`. The scheduler renders and uploads each one as private with a publish time about 48 hours ahead.

### What the YouTube data shows (channel analytics + per-video stats)
Channel: 29 subscribers, about 4.6k views. 51 Shorts since 3 Nov (median 28 views, mean 88) and 17 long videos (median 7 views, 177 in total).

| What | Result |
|---|---|
| Where views come from | Shorts feed 89%, YouTube search 7.8%. Shorts are 97% of views, long videos about 2%. |
| Who watches | In the top 12 countries (1,549 views): France 730, US 240, Uzbekistan 128, Morocco 104, Algeria 70. About 65% of those views are from French-speaking countries (France, Morocco, Algeria, Cote d'Ivoire, Senegal, DR Congo), who mostly already speak French. Uzbekistan watched only 15% of each Short. |
| Top 5 Shorts | "Polite vs Rude: I Want" 1,122 (40x median, but 25% viewed); "3 Ways to Say Excuse Me" 744 (22% viewed); "It's freezing in Paris! Say this" 416 (48% viewed); "The Baker Said Ah Non!" 324 (71% viewed); "Stop Saying Just Merci" 285. |
| Hook shape | Story-style character hooks ("The Baker said Ah non! What did Adrien forget?") hold viewers best (71%). "N ways to say" median 285. Generic "Say X, not Y" mistakes: median 34. "How to say X": median 29. Counting/vocab: 26. |
| Length | Under 26 seconds: 57-59% viewed, median 31 views. Over 62 seconds: 28% viewed. The two big hits are 69-second Shorts with low retention, so the topic carried them, not the format. |
| Long videos | 17 videos, median 7 views. |

**Working:** polite-vs-rude and "ways to say" topics; Adrien making a mistake with a question hook; short scripts with a clear payoff.
**Not working:** plain "How to say X", counting and vocabulary Shorts, "Say X not Y" grammar corrections, long videos for now.

**Caveats:** one Short is 25% of all Shorts views. The country list covers only the top 12 countries, so the French-speaking share is for those, not for every view. The audience problem is the big open question: if many viewers already speak French, retention and subscriber conversion stay low. Titles in English (already in place) and learner-specific hooks ("in French for beginners") are the fix to test.

### The December mix (62 Shorts)
- survival phrase ("Ask like this"): 33
- seasonal / culture: 16
- mistake / "doesn't mean" hook: 7
- character hook ("Alex did X..."): 6

Rules used: English hook first; 20-30 seconds; one situation; a comment question at the end; no same phrase twice in a week; short titles. French Shorts lean on situations a learner meets (restaurant, shop, transport, holidays) instead of grammar rules. About a quarter of the month is Christmas and New Year culture (a guess about search interest, not measured).

### Calendar
Every day: Short A at 15:00 UTC (10:00 ET), Short B at 23:00 UTC (18:00 ET). First: Sun 6 Dec; last: Tue 5 Jan. Exact titles are the `title:` line of each file in `shorts/`.

### Checkpoints (ship it, or change it?)
- **6 Dec:** the Nov 23 - Dec 5 story week is over. If stories averaged under 30 views, move the rest to `held_items` and keep at most one story a week.
- **13 Dec:** median views of the first 14 December Shorts against the Nov median of 28. Keep a hook type at 2x (56) and 50% viewed; cut one under 1x.
- **3 Jan:** compare hook types over 40+ Shorts; double the best.
- Studio > Analytics > Audience > Geography: aim for at least 25% of views from the US/UK/Canada/Australia learner markets, not only French-speaking countries.

### Native-speaker check
The French is AI-written and not native-verified. Worth a look first: the "je suis plein" script, the "je suis crevé" slang line, the "ça m'est égal" line and the "Meilleurs voeux" New Year line.
