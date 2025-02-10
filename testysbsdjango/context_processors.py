from viewer.models import FontSize

def get_font_size(request):
    current_font_size = FontSize.objects.first()
    return {'current_font_size': current_font_size.size}