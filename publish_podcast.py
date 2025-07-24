#!/usr/bin/env python3
"""
Publish a podcast episode to the episodes/ directory
This script combines podcast generation with publishing
"""

import os
import shutil
from datetime import datetime
from podcast_generator import PodcastGenerator

def publish_podcast():
    """Generate and publish a podcast episode"""
    
    print("🎙️ Starting podcast generation and publishing...")
    
    # Generate the podcast
    generator = PodcastGenerator(test_mode=False)
    success = generator.generate_podcast()
    
    if not success:
        print("❌ Podcast generation failed")
        return False
    
    # Find the generated podcast file
    podcast_files = [f for f in os.listdir('.') if f.startswith('Youth_Lens_Today_') and f.endswith('.mp3')]
    
    if not podcast_files:
        print("❌ No podcast file found")
        return False
    
    # Get the most recent podcast file
    latest_podcast = max(podcast_files, key=os.path.getctime)
    
    # Create episodes directory if it doesn't exist
    os.makedirs('episodes', exist_ok=True)
    
    # Move the podcast to episodes directory
    source_path = latest_podcast
    dest_path = os.path.join('episodes', latest_podcast)
    
    shutil.move(source_path, dest_path)
    
    print(f"✅ Podcast published: {dest_path}")
    
    # Generate RSS feed
    print("📡 Updating RSS feed...")
    os.system('python3 generate_rss.py')
    
    print("🎉 Podcast published successfully!")
    print(f"📁 Episode: {dest_path}")
    print("📡 RSS URL: https://youthlenstoday.github.io/podcast/rss.xml")
    
    return True

if __name__ == '__main__':
    publish_podcast() 