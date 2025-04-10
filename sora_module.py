
def generate_video(text):
    return f"[SoraAI]: Сгенерировано видео по запросу: '{text}'"



def check_limitations(response_text):
    warnings = [
        "quota", "limit", "rate exceeded", "payment required", "upgrade your plan"
    ]
    if any(w in response_text.lower() for w in warnings):
        return f"[Предупреждение]: Обнаружено ограничение или необходимость подписки: {response_text}"
    return response_text
