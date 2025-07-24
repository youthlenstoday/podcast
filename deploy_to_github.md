# Deploying Youth Lens Today Podcast to GitHub

## Step 1: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Youth Lens Today podcast hosting setup"

# Add remote repository
git remote add origin https://github.com/youthlenstoday/podcast.git

# Push to main branch
git push -u origin main
```

## Step 2: Enable GitHub Pages

1. Go to your repository: https://github.com/youthlenstoday/podcast
2. Click "Settings" tab
3. Scroll down to "Pages" section
4. Under "Source", select "Deploy from a branch"
5. Select "main" branch and "/ (root)" folder
6. Click "Save"

## Step 3: Add Cover Art (Optional)

Upload a `cover.jpg` file to the root directory. Recommended size: 1400x1400 pixels.

## Step 4: Test the Setup

1. Add a test MP3 file to the `episodes/` directory
2. Commit and push the changes
3. The GitHub Action will automatically generate the RSS feed
4. Check the RSS feed at: https://youthlenstoday.github.io/podcast/rss.xml

## Step 5: Submit to Podcast Platforms

Use this RSS URL to submit to podcast platforms:
```
https://youthlenstoday.github.io/podcast/rss.xml
```

### Platform Submission Links:
- **Spotify for Podcasters**: https://podcasters.spotify.com/
- **Apple Podcasts**: https://podcastsconnect.apple.com/
- **Google Podcasts**: https://podcastsmanager.google.com/
- **Amazon Music**: https://podcasters.amazon.com/

## Step 6: Automate Podcast Generation

To automatically generate and publish podcasts:

```bash
# Generate and publish a new episode
python3 publish_podcast.py

# Then commit and push
git add episodes/
git commit -m "Add new episode"
git push
```

## File Structure After Deployment

```
podcast/
├── episodes/                    # MP3 files (auto-populated)
├── rss.xml                     # RSS feed (auto-generated)
├── index.html                   # Podcast homepage
├── cover.jpg                    # Podcast cover art
├── generate_rss.py             # RSS generation script
├── publish_podcast.py          # Publishing script
├── podcast_generator.py        # Podcast generation script
├── .github/workflows/generate-rss.yml  # Auto-update workflow
└── README.md                   # Documentation
```

## Verification Checklist

- [ ] GitHub Pages is enabled and working
- [ ] RSS feed is accessible at the correct URL
- [ ] GitHub Action runs successfully when episodes are added
- [ ] Podcast platforms accept the RSS feed
- [ ] Cover art is displayed correctly
- [ ] Episodes play correctly from the RSS feed

## Troubleshooting

### RSS Feed Not Working
- Check that the GitHub Action completed successfully
- Verify the RSS XML is valid using an online validator
- Ensure all required RSS tags are present

### GitHub Pages Not Loading
- Check repository settings for Pages configuration
- Verify the main branch is selected as source
- Wait a few minutes for changes to propagate

### Audio Files Not Playing
- Ensure MP3 files are properly formatted
- Check file permissions and size
- Verify the enclosure URLs in the RSS feed are correct 