# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
We will pass `query_texts=[query]` (a list containing the single user query string), `n_results=n_results` (to limit the maximum returned chunks), and `include=["documents", "metadatas", "distances"]` to retrieve the chunk text, the associated game metadata, and the cosine similarity distance for each match.
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```json
{
    "text": "Hello There",
    "game": "Uno",
    "distance": 0.12
}
```

- `"text"` comes from `results["documents"][0][i]`
- `"game"` comes from the `"game"` key in `results["metadatas"][0][i]`
- `"distance"` comes from `results["distances"][0][i]`

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
`_collection.query()` returns lists of lists (e.g., `results['documents'][0]`) because Chroma is designed to handle multiple queries at once. Since we only send one query string, we need to access index `[0]` of the results to get the matching chunks for our specific question.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
I will return all `n_results` regardless of distance for now. 
Tradeoffs: Filtering would reduce "noise," but if the embedding model doesn't see a high similarity for a niche rule, filtering might prevent the AI from seeing the correct answer entirely. It is better to let the LLM see the chunks and decide if they are relevant.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: What happens when you roll a 7 in CATAN ? 
Top result game: CATAN
Distance score: 0.346
Does it make sense? [yes / no / explain]
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
