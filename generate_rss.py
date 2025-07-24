#!/usr/bin/env python3
"""
Generate RSS feed for Youth Lens Today podcast
Scans episodes/ directory for .mp3 files and creates rss.xml
"""

import os
import glob
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_file_info(filepath):
    """Get file creation time and size"""
    stat = os.stat(filepath)
    return {
        'mtime': datetime.fromtimestamp(stat.st_mtime),
        'size': stat.st_size
    }

def format_rfc822_date(dt):
    """Format datetime to RFC 822 format for RSS"""
    return dt.strftime('%a, %d %b %Y %H:%M:%S %z')

def generate_rss():
    """Generate RSS feed from MP3 files in episodes/ directory"""
    
    # RSS feed template
    rss_template = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>Youth Lens Today</title>
        <description>A podcast exploring current events and youth perspectives</description>
        <language>en-us</language>
        <link>https://youthlenstoday.github.io/podcast/</link>
        <atom:link href="https://youthlenstoday.github.io/podcast/rss.xml" rel="self" type="application/rss+xml"/>
        <itunes:author>Nathan Goldberg, Jonah Herman</itunes:author>
        <itunes:explicit>no</itunes:explicit>
        <itunes:category text="News"/>
        <itunes:category text="Politics"/>
        <itunes:category text="Education"/>
        <itunes:image href="https://youthlenstoday.github.io/podcast/cover.jpg"/>
        <image>
            <url>https://youthlenstoday.github.io/podcast/cover.jpg</url>
            <title>Youth Lens Today</title>
            <link>https://youthlenstoday.github.io/podcast/</link>
        </image>
        {items}
    </channel>
</rss>'''
    
    # Find all MP3 files in episodes directory
    mp3_files = glob.glob('episodes/*.mp3')
    
    if not mp3_files:
        print("No MP3 files found in episodes/ directory")
        return
    
    # Sort files by modification time (newest first)
    mp3_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    items = []
    for mp3_file in mp3_files:
        filename = os.path.basename(mp3_file)
        episode_name = os.path.splitext(filename)[0]
        file_info = get_file_info(mp3_file)
        
        # Create episode item
        item = f'''        <item>
            <title>{episode_name}</title>
            <description>Episode of Youth Lens Today podcast</description>
            <pubDate>{format_rfc822_date(file_info['mtime'])}</pubDate>
            <guid>https://youthlenstoday.github.io/podcast/episodes/{filename}</guid>
            <enclosure url="https://youthlenstoday.github.io/podcast/episodes/{filename}" length="{file_info['size']}" type="audio/mpeg"/>
            <itunes:duration>00:00:00</itunes:duration>
        </item>'''
        items.append(item)
    
    # Generate RSS content
    items_content = '\n'.join(items)
    rss_content = rss_template.format(items=items_content)
    
    # Write RSS file
    with open('rss.xml', 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f"Generated RSS feed with {len(items)} episodes")
    print("RSS URL: https://youthlenstoday.github.io/podcast/rss.xml")

if __name__ == '__main__':
    generate_rss() 