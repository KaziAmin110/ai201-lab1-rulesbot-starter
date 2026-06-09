# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Format the retrieved chunks in a structured, hierarchical XML block. 
Each chunk will be wrapped in its own XML tag containing metadata attributes (game name) and a unique index.

Example Structure:
<retrieved_rules>
  <rule_chunk index="1" game="Catan">
    [Rule text content goes here...]
  </rule_chunk>
  
  <rule_chunk index="2" game="Ticket to Ride">
    [Rule text content goes here...]
  </rule_chunk>
</retrieved_rules>

```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are a strict board game rules assistant. Answer the user's question using ONLY the provided rules text.
Strictly adhere to the following rules:
1. GROUNDING: Rely ONLY on facts directly and explicitly stated in the provided text. Do not assume, extrapolate, speculate, or make logical leaps.
2. NO OUTSIDE KNOWLEDGE: Do not use any prior knowledge you have about board games, real-world rules, or game terms. If the provided text contradicts real-world rules, follow the provided text.
3. MISSING INFORMATION: If the provided text does not contain the direct answer to the query, state clearly: "I cannot find the answer in the provided rules." Do not try to answer using general knowledge or guess.
4. CITATION: Always identify which game the answer comes from. Make sure to clearly state the game name in your response (e.g. \"In [Game Name], ...\").

```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
Always identify which game the answer comes from. Make sure to clearly state the game name in your response (e.g. "In [Game Name], ...").
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
"I cannot find the answer in the provided rules."
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
Pass all retrieved chunks in. Let the strict grounding system prompt determine if the rules contain the answer. This is safer since sometimes relevant details might reside in chunks with slightly higher distance, but the model can rule them out if they don't apply.
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
System message: Strict rules assistant persona, grounding rules, citation requirements, and missing info fallback.
User message: Hierarchical XML rules context block and user's original query.
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: What happens at the start of a turn in Catan?
Response: In Catan, at the start of your turn, you roll both dice.
Correctly grounded? yes
Cited the right game? yes
```

**One thing you changed from your original spec after seeing the actual output:**

```
Ensured that the system prompt explicitly tells the model to start or clearly mention the game name (e.g. "In [Game Name], ...") so citation is unambiguous.
```
