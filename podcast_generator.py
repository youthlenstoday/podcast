import requests
import os
import subprocess
from datetime import datetime
import re

class PodcastGenerator:
    def __init__(self, test_mode=False):
        # Test mode flag
        self.test_mode = test_mode
        
        # Try to load from local config first, then environment variables
        try:
            from config_local import OPENAI_API_KEY, ELEVENLABS_API_KEY_1, ELEVENLABS_API_KEY_2, VOICE_ID_1, VOICE_ID_2
            self.openai_api_key = OPENAI_API_KEY
            self.elevenlabs_api_key_1 = ELEVENLABS_API_KEY_1
            self.elevenlabs_api_key_2 = ELEVENLABS_API_KEY_2
            self.voice_id_1 = VOICE_ID_1
            self.voice_id_2 = VOICE_ID_2
        except ImportError:
            # Fallback to environment variables
            self.openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
            self.elevenlabs_api_key_1 = os.getenv('ELEVENLABS_API_KEY_1', 'your-elevenlabs-api-key-1-here')
            self.elevenlabs_api_key_2 = os.getenv('ELEVENLABS_API_KEY_2', 'your-elevenlabs-api-key-2-here')
            self.voice_id_1 = os.getenv('VOICE_ID_1', 'iw4PJTWp4tOErnqySu4l')
            self.voice_id_2 = os.getenv('VOICE_ID_2', 'SzvGngFCMygUr9c1lyUW')
        
        # Headers
        self.openai_headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        self.elevenlabs_headers_1 = {
            "xi-api-key": self.elevenlabs_api_key_1,
            "Content-Type": "application/json"
        }
        
        self.elevenlabs_headers_2 = {
            "xi-api-key": self.elevenlabs_api_key_2,
            "Content-Type": "application/json"
        }

    def generate_script(self):
        """Generate a podcast script using GPT-4 with web search and multi-step approach"""
        
        # Step 1: Get current news and generate outline
        print("📰 Step 1: Researching current news and generating outline...")
        outline = self.generate_outline_with_web_search()
        if not outline:
            print("❌ Failed to generate outline")
            return None
        
        # Step 2: Generate HALF 1 (Nathan's content)
        print("🎤 Step 2: Generating Nathan Goldberg's script...")
        nathan_script = self.generate_nathan_script(outline)
        if not nathan_script:
            print("❌ Failed to generate Nathan's script")
            return None
        
        # Step 3: Generate HALF 2 (Jonah's content)
        print("🎤 Step 3: Generating Jonah Herman's script...")
        jonah_script = self.generate_jonah_script(outline)
        if not jonah_script:
            print("❌ Failed to generate Jonah's script")
            return None
        
        # Step 4: Combine the scripts
        print("🔗 Step 4: Combining scripts...")
        combined_script = f"HALF 1:\n\n{nathan_script}\n\nHALF 2:\n\n{jonah_script}"
        
        return combined_script

    def generate_outline_with_web_search(self):
        """Generate an outline with current news using GPT-4 with web search"""
        
        prompt = """Research the most recent news from the past 3-7 days and create a detailed outline for a podcast episode.

REQUIREMENTS:
- Use web search to find CURRENT news from the past week
- Focus on 3 main stories: US domestic politics/economics/law, international story, and offbeat policy story
- Include specific dates, names, and details from recent news
- Provide detailed context and implications for each story
- Use the current date (July 2024)

OUTLINE FORMAT:
1. US Domestic Story: [Title] - [Brief description with current details]
2. International Story: [Title] - [Brief description with current details]  
3. Offbeat Story: [Title] - [Brief description with current details]

For each story, include:
- What happened (with specific dates and details)
- Why it matters
- Key players involved
- Potential implications
- Current status/developments

Make sure all stories are from the past week and include current, specific details."""

        url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": "gpt-4o-search-preview",
            "messages": [
                {"role": "system", "content": "You are a news researcher. Use web search to find the most recent, current news from the past week."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(url, headers=self.openai_headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"❌ Error generating outline: {e}")
            return None

    def generate_nathan_script(self, outline):
        """Generate Nathan Goldberg's script (HALF 1)"""
        prompt = f"""Write Nathan Goldberg's portion of a podcast script (4,000+ characters) for Youth Lens Today.

CURRENT OUTLINE:
{outline}

REQUIREMENTS:
- Write as Nathan Goldberg (first person)
- Brief intro (1 paragraph): welcome listeners, state current date, summarize the 3 stories
- Cover the FIRST story from the outline in detail (2,000+ chars)
- Include transition to the second story
- Use current date (July 2024)
- Be extremely detailed and thorough
- NO dialogue format - write as monologue
- NO stage directions
- NO markdown formatting (no **bold**, *italic*, or headers)
- NO section titles or headers
- NO bullet points or lists (no "-" or "*" at start of lines)
- NO repetition of sentences or paragraphs
- NO weather reports or casual content
- NO source citations or links (no parentheses with URLs)
- Focus on serious news analysis
- Include extensive context, background, and implications
- Use natural, conversational tone
- Write as flowing narrative without any formatting markers
- Ensure each sentence is unique and contributes to the story
- Write in paragraph form only, no lists or bullet points

FORMAT: Write as a flowing narrative that ends with a transition to Jonah's portion. Do not use any formatting, headers, section titles, bullet points, or lists. Write everything in paragraph form."""

        url = "https://api.openai.com/v1/chat/completions"
        data = {
            "model": "gpt-4o-search-preview",
            "messages": [
                {"role": "system", "content": "You are Nathan Goldberg, a podcast host. Write detailed, engaging content (4,000+ characters)."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 5000
        }
        
        try:
            response = requests.post(url, headers=self.openai_headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"❌ Error generating Nathan's script: {e}")
            return None

    def generate_jonah_script(self, outline):
        """Generate Jonah Herman's script (HALF 2)"""
        prompt = f"""Write Jonah Herman's portion of a podcast script (4,000+ characters) for Youth Lens Today.

CURRENT OUTLINE:
{outline}

REQUIREMENTS:
- Write as Jonah Herman (first person)
- Cover the SECOND and THIRD stories from the outline in detail (2,500+ chars)
- Include brief outro (1 paragraph): reflect on all stories, ask listeners to follow
- Use current date (July 2024)
- Be extremely detailed and thorough
- NO dialogue format - write as monologue
- NO stage directions
- NO markdown formatting (no **bold**, *italic*, or headers)
- NO section titles or headers
- NO bullet points or lists (no "-" or "*" at start of lines)
- NO repetition of sentences or paragraphs
- NO weather reports or casual content
- NO source citations or links (no parentheses with URLs)
- Focus on serious news analysis
- Include extensive context, background, and implications
- Use natural, conversational tone
- End with both hosts signing off
- Write as flowing narrative without any formatting markers
- Ensure each sentence is unique and contributes to the story
- Write in paragraph form only, no lists or bullet points

FORMAT: Write as a flowing narrative that continues from Nathan's portion and concludes the episode. Do not use any formatting, headers, section titles, bullet points, or lists. Write everything in paragraph form."""

        url = "https://api.openai.com/v1/chat/completions"
        data = {
            "model": "gpt-4o-search-preview",
            "messages": [
                {"role": "system", "content": "You are Jonah Herman, a podcast host. Write detailed, engaging content (4,000+ characters)."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 5000
        }
        
        try:
            response = requests.post(url, headers=self.openai_headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"❌ Error generating Jonah's script: {e}")
            return None

    def clean_text_for_audio(self, text):
        """Clean text to remove formatting artifacts and prepare for audio synthesis"""
        
        # Remove markdown formatting (both ** and * patterns)
        import re
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove **text** -> text
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove *text* -> text
        text = text.replace('**', '').replace('*', '')   # Remove any remaining asterisks
        
        # Remove bullet points and list formatting
        text = re.sub(r'^\s*[-*]\s*', '', text, flags=re.MULTILINE)  # Remove "- " or "* " at start of lines
        text = re.sub(r'^\s*[-*]\s*\*\*([^*]+)\*\*:\s*', r'\1: ', text, flags=re.MULTILINE)  # Remove "- **text**: " -> "text: "
        
        # Remove source citations - anything in parentheses with https
        text = re.sub(r'\s*\([^)]*https[^)]*\)', '', text)  # Remove (source links)
        text = re.sub(r'\s*\[[^\]]*https[^\]]*\]', '', text)  # Remove [source links]
        
        # Remove HALF 1/HALF 2 markers
        text = text.replace('HALF 1:', '').replace('HALF 2:', '')
        
        # Remove section headers and formatting
        text = text.replace('HOST 1:', '').replace('HOST 2:', '')
        text = text.replace('SEGMENT 1:', '').replace('SEGMENT 2:', '').replace('SEGMENT 3:', '')
        text = text.replace('INTRO:', '').replace('OUTRO:', '')
        text = text.replace('Transition to Segment 2:', '').replace('Transition to Segment 3:', '')
        
        # Remove any remaining formatting artifacts
        text = text.replace('===', '').replace('---', '')
        
        # Remove any lines that are just formatting or headers
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # Skip lines that are just formatting, headers, or empty
            if (line and 
                not line.startswith('**') and 
                not line.startswith('===') and 
                not line.startswith('---') and
                not line.startswith('#') and
                not line.startswith('-') and  # Skip bullet points
                not line.startswith('*') and  # Skip asterisk bullets
                not re.match(r'^[A-Z\s]+$', line) and  # Skip ALL CAPS headers
                not re.match(r'^\*\*[^*]+\*\*$', line)):  # Skip **header** lines
                cleaned_lines.append(line)
        
        # Join back together with proper spacing
        cleaned_text = ' '.join(cleaned_lines)
        
        # Remove repetition (detect and remove repeated sentences)
        sentences = re.split(r'[.!?]+', cleaned_text)
        unique_sentences = []
        seen_sentences = set()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Only consider substantial sentences
                # Normalize sentence for comparison (remove extra spaces, lowercase)
                normalized = re.sub(r'\s+', ' ', sentence.lower()).strip()
                if normalized not in seen_sentences:
                    unique_sentences.append(sentence)
                    seen_sentences.add(normalized)
        
        # Reconstruct text from unique sentences
        cleaned_text = '. '.join(unique_sentences) + '.'
        
        # Final cleanup - remove extra spaces and normalize
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        return cleaned_text

    def split_script_for_hosts(self, script):
        """Split the script into two parts for the two hosts using HALF 1/HALF 2 markers"""

        # Look for the HALF 1 and HALF 2 markers
        if "HALF 1:" in script and "HALF 2:" in script:
            # Split on the HALF 2 marker
            parts = script.split("HALF 2:")
            if len(parts) == 2:
                # Extract HALF 1 content (remove the "HALF 1:" prefix)
                host1_script = parts[0].replace("HALF 1:", "").strip()
                # Extract HALF 2 content
                host2_script = parts[1].strip()

                return host1_script, host2_script

        # Fallback: if markers aren't found, use the old method
        print("⚠️  Warning: HALF 1/HALF 2 markers not found, using fallback splitting method")

        lines = script.split('\n')
        first_part_end = len(lines) // 2
        second_part_start = first_part_end
        
        host1_script = '\n'.join(lines[:first_part_end])
        host2_script = '\n'.join(lines[second_part_start:])
        
        host1_script = host1_script.strip()
        host2_script = host2_script.strip()
        
        return host1_script, host2_script

    def generate_audio(self, text, voice_id, api_key, headers, filename):
        """Generate audio using ElevenLabs API"""
        
        # Clean the text for audio
        cleaned_text = self.clean_text_for_audio(text)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        data = {
            "text": cleaned_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return False

    def combine_audio_files(self, file1, file2, output_file):
        """Combine two audio files using ffmpeg"""
        
        try:
            cmd = [
                'ffmpeg', '-i', file1, '-i', file2,
                '-filter_complex', '[0:0][1:0]concat=n=2:v=0:a=1[out]',
                '-map', '[out]', output_file, '-y'
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error combining audio files: {e}")
            return False

    def generate_podcast(self):
        """Generate a complete podcast episode"""
        
        print("🎙️ Starting podcast generation...")
        
        # Step 1: Generate script
        print("📝 Generating script...")
        script = self.generate_script()
        
        if not script:
            print("❌ Failed to generate script")
            return False
        
        print("✅ Script generated successfully")
        print(f"📄 Script length: {len(script)} characters")
        
        # Step 2: Split script for hosts
        print("👥 Splitting script for two hosts...")
        host1_script, host2_script = self.split_script_for_hosts(script)
        
        print(f"🎤 Host 1 script length: {len(host1_script)} characters")
        print(f"🎤 Host 2 script length: {len(host2_script)} characters")
        
        # Test mode: Stop before expensive API calls
        if self.test_mode:
            print("\n🧪 TEST MODE: Stopping before ElevenLabs API calls")
            print("✅ Script generation and splitting completed successfully!")
            print("📊 Analysis:")
            print(f"   - Total script length: {len(script)} characters")
            print(f"   - Nathan Goldberg content: {len(host1_script)} characters")
            print(f"   - Jonah Herman content: {len(host2_script)} characters")
            print(f"   - Split ratio: {len(host1_script)/(len(host1_script)+len(host2_script))*100:.1f}% / {len(host2_script)/(len(host1_script)+len(host2_script))*100:.1f}%")
            
            # Save test results
            test_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(test_file, 'w') as f:
                f.write("=== TEST RESULTS ===\n\n")
                f.write(f"Script Length: {len(script)} characters\n")
                f.write(f"Nathan Goldberg Length: {len(host1_script)} characters\n")
                f.write(f"Jonah Herman Length: {len(host2_script)} characters\n\n")
                f.write("=== FULL SCRIPT ===\n\n")
                f.write(script)
                f.write("\n\n=== NATHAN GOLDBERG SCRIPT ===\n\n")
                f.write(host1_script)
                f.write("\n\n=== JONAH HERMAN SCRIPT ===\n\n")
                f.write(host2_script)
            
            print(f"📄 Test results saved to: {test_file}")
            return True
        
        # Production mode: Continue with audio generation
        print("🎵 Generating audio for Nathan Goldberg...")
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        nathan_audio_file = f"Nathan_Goldberg_{current_time}.mp3"
        success1 = self.generate_audio(
            host1_script, 
            self.voice_id_1, 
            self.elevenlabs_api_key_1, 
            self.elevenlabs_headers_1, 
            nathan_audio_file
        )
        
        if not success1:
            print("❌ Failed to generate Nathan Goldberg audio")
            return False
        
        # Step 4: Generate audio for Jonah Herman
        print("🎵 Generating audio for Jonah Herman...")
        jonah_audio_file = f"Jonah_Herman_{current_time}.mp3"
        success2 = self.generate_audio(
            host2_script, 
            self.voice_id_2, 
            self.elevenlabs_api_key_2, 
            self.elevenlabs_headers_2, 
            jonah_audio_file
        )
        
        if not success2:
            print("❌ Failed to generate Jonah Herman audio")
            return False
        
        # Step 5: Combine audio files
        print("🔗 Combining audio files...")
        final_audio_file = f"Youth_Lens_Today_{current_time}.mp3"
        success3 = self.combine_audio_files(nathan_audio_file, jonah_audio_file, final_audio_file)
        
        if not success3:
            print("❌ Failed to combine audio files")
            return False
        
        print("✅ Podcast generated successfully!")
        print(f"📁 Final audio file: {final_audio_file}")
        
        # Clean up individual files
        try:
            os.remove(nathan_audio_file)
            os.remove(jonah_audio_file)
            print("🧹 Cleaned up temporary audio files")
        except:
            pass
        
        return True

def main():
    """Main function to run the podcast generator"""
    
    # Check for test mode argument
    import sys
    test_mode = "--test" in sys.argv
    
    if test_mode:
        print("🧪 Running in TEST MODE - will stop before ElevenLabs API calls")
    else:
        # Check if ffmpeg is installed (only needed for production mode)
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ ffmpeg is not installed. Please install ffmpeg to generate podcasts.")
            print("   macOS: brew install ffmpeg")
            print("   Ubuntu: sudo apt-get install ffmpeg")
            return
    
    # Generate podcast
    generator = PodcastGenerator(test_mode=test_mode)
    success = generator.generate_podcast()
    
    if success:
        print("\n🎉 Podcast generation completed successfully!")
        if test_mode:
            print("🧪 Test completed successfully!")
            print("📁 Check the current directory for test results.")
    else:
        print("\n❌ Podcast generation failed.")

if __name__ == "__main__":
    main() 