
def render_with_rtx(image):
    return f"[RTX]: Отрендерено изображение {image}"

def upscale_with_dlss(image):
    return f"[DLSS]: Улучшено изображение {image}"



def check_limitations(response_text):
    warnings = [
        "quota", "limit", "rate exceeded", "payment required", "upgrade your plan"
    ]
    if any(w in response_text.lower() for w in warnings):
        return f"[Предупреждение]: Обнаружено ограничение или необходимость подписки: {response_text}"
    return response_text
