# Youth Lens Today Podcast

A podcast exploring current events and youth perspectives, hosted by Nathan Goldberg and Jonah Herman.

## RSS Feed

Subscribe to our podcast using the RSS feed:
```
https://youthlenstoday.github.io/podcast/rss.xml
```

## Repository Structure

```
podcast/
├── episodes/          # MP3 files for each episode
├── rss.xml           # RSS feed (auto-generated)
├── index.html        # Podcast homepage
├── cover.jpg         # Podcast cover art (optional)
├── generate_rss.py   # Script to generate RSS feed
└── .github/workflows/generate-rss.yml  # Auto-update workflow
```

## How It Works

1. **Upload Episodes**: Add `.mp3` files to the `episodes/` directory
2. **Auto-Generate RSS**: The GitHub Action automatically regenerates `rss.xml` when new episodes are added
3. **Publish**: The RSS feed is available at `https://youthlenstoday.github.io/podcast/rss.xml`

## Adding New Episodes

1. Upload your `.mp3` file to the `episodes/` directory
2. Commit and push to the `main` branch
3. The GitHub Action will automatically update the RSS feed
4. The episode will be available in the RSS feed within minutes

## Podcast Platforms

Submit the RSS URL to your preferred podcast platforms:
- Spotify for Podcasters
- Apple Podcasts
- Google Podcasts
- Amazon Music
- And more...

## Local Development

To test the RSS generation locally:

```bash
python generate_rss.py
```

This will create/update `rss.xml` based on the MP3 files in the `episodes/` directory.

## GitHub Pages

This repository is configured to serve the podcast via GitHub Pages at:
`https://youthlenstoday.github.io/podcast/`

The RSS feed will be available at:
`https://youthlenstoday.github.io/podcast/rss.xml` 