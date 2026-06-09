from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # Format the retrieved chunks in a structured XML block as specified
    context_parts = ["<retrieved_rules>"]
    for i, chunk in enumerate(retrieved_chunks, start=1):
        game_name = chunk.get("game", "Unknown Game")
        text = chunk.get("text", "").strip()
        context_parts.append(f'  <rule_chunk index="{i}" game="{game_name}">\n    {text}\n  </rule_chunk>')
    context_parts.append("</retrieved_rules>")
    context_str = "\n".join(context_parts)

    # System prompt - grounding instruction and citation instruction
    system_prompt = (
        "You are a strict board game rules assistant. Answer the user's question using ONLY the provided rules text.\n"
        "Strictly adhere to the following rules:\n"
        "1. GROUNDING: Rely ONLY on facts directly and explicitly stated in the provided text. Do not assume, extrapolate, speculate, or make logical leaps.\n"
        "2. NO OUTSIDE KNOWLEDGE: Do not use any prior knowledge you have about board games, real-world rules, or game terms. If the provided text contradicts real-world rules, follow the provided text.\n"
        "3. MISSING INFORMATION: If the provided text does not contain the direct answer to the query, state clearly: \"I cannot find the answer in the provided rules.\" Do not try to answer using general knowledge or guess.\n"
        "4. CITATION: Always identify which game the answer comes from. Make sure to clearly state the game name in your response (e.g. \"In [Game Name], ...\")."
    )

    user_message = (
        f"Context:\n{context_str}\n\n"
        f"Query: {query}"
    )

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

