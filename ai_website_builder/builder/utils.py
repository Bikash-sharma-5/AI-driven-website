import openai

openai.api_key = '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'

def generate_ai_content(business_type, industry):
    prompt = f"Generate homepage content for a {business_type} in the {industry} industry."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"homepage": response['choices'][0]['message']['content']}