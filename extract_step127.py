import json

with open('/Users/viveknegi/.gemini/antigravity/brain/a3fde2f0-241d-4f37-8cd3-3676843e9f37/.system_generated/logs/transcript_full.jsonl') as f:
    for line in f:
        data = json.loads(line)
        if data.get('step_index') == 127:
            content = data.get('content', '')
            start = content.find('\\documentclass')
            end = content.find('\\end{document}')
            if start != -1 and end != -1:
                with open('/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/presentation_from_transcript.tex', 'w') as out:
                    out.write(content[start:end+14])
                print('Saved presentation_from_transcript.tex!')
            else:
                print('Start or end not found in content!')
