from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def fetch_video_transcript(video_url):
    # Extracting Video ID from URL
    if "youtu.be" in video_url:
        video_id = video_url.split('/')[-1]
    else:
        video_id = video_url.split('v=')[-1].split('&')[0]
    
    # Attempt to fetch the video transcript
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format each transcript item with its timestamp
        formatted_transcript = []
        for item in transcript_list:
            timestamp = format_timestamp(item['start'])
            formatted_transcript.append(f"[{timestamp}] {item['text']}")
        
        # Join all formatted items into a single string
        full_transcript = '\n'.join(formatted_transcript)
        return full_transcript
    except Exception as e:
        return f"Failed to fetch transcript: {str(e)}"

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.json
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400
    
    transcript = fetch_video_transcript(video_url)
    
    if transcript.startswith("Failed to fetch transcript"):
        return jsonify({"error": transcript}), 400
    
    return jsonify({"transcript": transcript})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)