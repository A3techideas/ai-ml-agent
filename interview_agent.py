from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_feedback(transcript, candidate_name, role):
    prompt = f"""
    You are an interview evaluation agent. Analyze the following interview transcript for the candidate: {candidate_name} applying for the role of {role}.
    Provide a structured evaluation including:
    - Summary
    - Communication Score (1-10)
    - Technical Knowledge Score (1-10)
    - Cultural Fit Score (1-10)
    - Final Recommendation (Yes/No with justification)

    Interview Transcript:
    {transcript}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return response.text

