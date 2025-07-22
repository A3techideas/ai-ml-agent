from config import OPENAI_API_KEY

try:
    from openai import OpenAI
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
            model="gpt-3.5-turbo",
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

except Exception as e:
    # 🔄 Fallback for development or OpenAI API quota issues
    print(f"⚠️ OpenAI API unavailable, using mock responses. Reason: {e}")

    def generate_feedback(transcript, candidate_name, role):
        return f"""
        Feedback for {candidate_name} applying for the position of {role}:

        - Summary: {candidate_name} has demonstrated relevant experience and communication skills. The candidate appears confident and knowledgeable.
        - Communication Score: 8/10
        - Technical Knowledge Score: 9/10
        - Cultural Fit Score: 7/10
        - Final Recommendation: Yes (Recommended for the role of {role} based on the provided transcript.)
        """

    def transcribe_audio(file_path):
        return "This is a mocked transcription from the audio file."

