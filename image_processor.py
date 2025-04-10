
def process_image(image_path):
    return f"[ImageProcessor]: Обработан файл: {image_path}"



def check_limitations(response_text):
    warnings = [
        "quota", "limit", "rate exceeded", "payment required", "upgrade your plan"
    ]
    if any(w in response_text.lower() for w in warnings):
        return f"[Предупреждение]: Обнаружено ограничение или необходимость подписки: {response_text}"
    return response_text
