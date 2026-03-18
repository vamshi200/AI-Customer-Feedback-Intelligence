def generate_insight(query, context):
    """
    Mock LLM response (no API required)
    """

    return f"""
🔍 Insight Summary:

User Question:
{query}

Relevant Feedback:
{context[:300]}

📊 Key Observations:
- Customers are showing mixed sentiment across feedback.
- Negative feedback indicates possible issues in service or product quality.
- Some recurring complaints suggest systemic problems.

💡 Suggested Actions:
- Improve customer support response time.
- Focus on resolving frequent complaints.
- Enhance overall user experience.

⚠️ Note:
This is a simulated AI-generated insight (mock mode due to API quota limits).
"""