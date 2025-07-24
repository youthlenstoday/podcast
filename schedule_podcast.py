#!/usr/bin/env python3
"""
Podcast Automation Scheduler
Run this script to generate a podcast episode on schedule
"""

import os
import sys
import logging
from datetime import datetime
from podcast_generator import PodcastGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('podcast_generation.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Main function for scheduled podcast generation"""
    
    try:
        logging.info("🎙️ Starting scheduled podcast generation...")
        
        # Initialize the podcast generator
        generator = PodcastGenerator()
        
        # Generate the podcast
        success = generator.generate_podcast()
        
        if success:
            logging.info("✅ Podcast generation completed successfully!")
            
            # Optional: Add upload logic here
            # upload_to_spotify()
            # upload_to_anchor()
            
        else:
            logging.error("❌ Podcast generation failed!")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"❌ Error during podcast generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 