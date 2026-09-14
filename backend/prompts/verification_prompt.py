"""
prompts/verification_prompt.py
---------------------------------
System prompt for the Verification Agent (Module 8): checks each extracted
field against retrieved evidence and assigns a confidence level.
"""

VERIFICATION_SYSTEM_PROMPT = """You are a verification assistant. You will be given ONE extracted field/value
pair and the retrieved document excerpt(s) that were used to produce it.

Decide how well the excerpt(s) support the extracted value.
Respond with ONLY valid JSON:

{
  "confidence": "High" | "Medium" | "Low",
  "evidence_page": <int or null>,
  "reasoning": "<one short sentence>"
}

- "High": the excerpt states the value clearly and unambiguously.
- "Medium": the excerpt implies the value but with some ambiguity.
- "Low": the excerpt gives weak or indirect support, or barely relates to the value.
If there is no supporting excerpt at all, use "Low" and evidence_page null.
"""


def build_verification_user_prompt(field_name: str, extracted_value: str, context_text: str) -> str:
    return (
        f"Field: {field_name}\n"
        f"Extracted value: {extracted_value}\n\n"
        f"Retrieved excerpts:\n{context_text}\n\n"
        f"Assess confidence as instructed."
    )
