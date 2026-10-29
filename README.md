# Tiny French – YouTube

Turn one script file into a YouTube video with **Adrien & Marinette** teaching French. Same system as *Tiny Japanese* (`tiny-japanese-youtube`), with French voices, French text on screen and the Tiny French characters.

| Kind | What you get | Script folder | Workflow |
|---|---|---|---|
| **Short** | vertical 1080x1920 Short, about 45 seconds: mini story, 1-2 key words, 1 quiz question | `shorts/` | Render YouTube Short |
| **Long** | landscape 1920x1080 lesson: story, vocabulary, grammar, quiz (4-6 minutes) | `lessons/` | Render YouTube lesson |
| **Story** | like Long, but Adrien and Marinette *act out* the story: they walk, react, hold things, change places; rain, snow, umbrellas, day and night | `stories/` | Render story video |

Everything runs on free tools: GitHub Actions, Microsoft Edge neural voices (`fr-FR-DeniseNeural` for Marinette, `fr-FR-HenriNeural` for Adrien, an English narrator for the explanations), Pillow and ffmpeg. No paid API.

## Make a video
1. Open the studio page (GitHub Pages, from `docs/`), pick **Short**, **Long** or **Story**, paste a script and press the button. Or add a script to `shorts/`, `lessons/` or `stories/` and run the matching workflow under **Actions** with the file name.
2. The job renders the video, uploads it to YouTube (only if the secrets below are set) and publishes it on the site.
3. Outputs: `.mp4`, `.thumbnail.png`, `.srt` (lessons), `.description.txt` (title, chapters, vocabulary, hashtags) and `.youtube.txt` (the YouTube link).

Locally: `pip install -r requirements.txt` (plus ffmpeg and the fonts `fonts-noto-core fonts-dejavu-core`), then
`python lesson.py lessons/01-at-the-bakery.txt`, `python short.py shorts/01-bakery-phrases.txt` or `python story/lesson.py stories/01-a-rainy-day-in-paris.txt -o output`.
Quick checks: `--preview folder/` saves frames, `--dummy-audio` skips the voices.

## Script format
```
title: At the Bakery
episode: 1
scene: bakery                # or auto

[story]
Marinette: Bonjour, Adrien ! | Hello, Adrien!
Adrien: Je voudrais un croissant. | I would like a croissant. | zhuh voo-DRAY uhn kwa-SSAN

[vocab]
vocab: un croissant | a croissant | uhn kwa-SSAN          # pronunciation is optional
example: Je voudrais un croissant. | I would like a croissant.

[grammar]
grammar: Je voudrais + noun | Use this to politely ask for something
example: Je voudrais une baguette. | I would like a baguette.

[quiz]
quiz: Question? | option A | option B | option C | B | optional explanation
```
- Every spoken line is `French | English`, with an optional third part for a pronunciation line under the French. There is no automatic pronunciation line (French spelling is not reliable for that), so add one only where it helps.
- Speakers: `Marinette` (left) and `Adrien` (right). `Marinette and Adrien: ...` = both at once.
- In quizzes and explanations, French words are read by a character and English by the narrator. The engine decides from the words in your script; put a French phrase in «guillemets» (or in quotes) to force it.
- Scenes: bakery, cafe, station, restaurant, store, bookstore, classroom, home, airport, street, park, beach, hospital, sakura (spring), and more. French words such as *boulangerie*, *gare* or *plage* pick the place automatically.
- French places (all three video types): `terrace` (Paris café terrace, aliases *bistro*, *terrasse*), `eiffel` (the Eiffel Tower view, aliases *paris*, *tour eiffel*; it twinkles at night in Story videos) and `market` (a marché with cheese, vegetable and fruit stalls). Their code is in `french_places.py`; the Story spots are listed in `story/DIRECTING.md`.
- Everything except `[story]` is optional.

### Shorts
Keep a Short under about 58 seconds (the job warns when it is longer). Dialogue style (`title:`, `scene:`, `weather:`, sections `[hook] [story] [practice] [quiz] [ending]`) or the `[story]` + `[vocab]` + `[quiz]` style both work. A line whose English contains "your turn", "say it" or "repeat after" is followed by a 3-second countdown, and so is the quiz answer. Every Short also gets its own 1280x720 thumbnail.

### Story videos
Directed scripts add stage directions in `[story]` (`> Marinette enters left`, `@scene cafe`, `@weather rain`). The full vocabulary is in `story/DIRECTING.md`. To have Claude write one for you, copy `story/DIRECTOR_PROMPT.md` (also on the Story tab of the studio page) into a chat and give it a story idea.

## Characters
Adrien and Marinette are drawn by `sprites.py` and `frchars/` (the same artwork as the Tiny French story studio). `characters.py` plugs that artwork into the three engines: portraits for Shorts and lessons, and the head of the full-body acting rig used in Story videos. The language helpers (which words are French) are in `lang_fr.py`.

## Automatic YouTube upload
Uses your own Google Cloud OAuth app. Add these under **Settings → Secrets and variables → Actions**:

| Kind | Name | Value |
|---|---|---|
| Secret | `YT_CLIENT_ID` | OAuth client ID |
| Secret | `YT_CLIENT_SECRET` | OAuth client secret |
| Secret | `YT_REFRESH_TOKEN` | refresh token for the Tiny French channel (scope `youtube.upload`) |
| Variable (optional) | `YT_PRIVACY` | `private` (default), `unlisted` or `public` |

Keep the Google consent screen **In production**, otherwise the refresh token expires after 7 days. A video is uploaded once; its `docs/videos/<name>.youtube.txt` marks it as done. If the upload fails the video is still published on the site and the job is marked failed. Custom thumbnails need a phone-verified YouTube channel. Without the secrets the jobs still render and publish; they just skip YouTube.

## Studio page
`docs/index.html` triggers the workflows through the GitHub API. Create a fine-grained token limited to this repository with **Contents: read/write** and **Actions: read/write** and paste it once on the page (it is stored only in your browser). Turn on GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / `docs`**.

## Notes
- On Actions the render stops rather than using the low-quality fallback voice (`STRICT_VOICE=1`); just re-run.
- Marinette says each vocabulary word and example slowly; English is read by a narrator voice.
- Thumbnails: stories and lessons use `story/make_cover.py` (the place, weather and the two characters with the title on a banner); `thumb.py` is the fallback; Shorts use `short_thumb.py`.
- The extra Japan-only places from the original engine (ramen shop, shrine, festival, onsen, karaoke, ...) are switched off for automatic scene picking. More French places (a boulangerie interior, the Seine, the Paris metro) would be the next additions in `french_places.py`.
