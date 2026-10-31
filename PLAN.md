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

## Things to clean up on the channel

- The channel still has three older guided-meditation videos from Oct 26 (they do not fit a beginner French channel). Consider making them private.
- The Tiny French videos that were uploaded earlier are all private. The scheduler uploads new ones private with a publish time, so you do not need to touch YT_PRIVACY.
