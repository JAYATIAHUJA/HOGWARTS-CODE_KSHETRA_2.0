from .models import Category

def categories_processor(request):
    """
    Context processor to make categories available in all templates
    """
    return {
        'global_categories': Category.objects.all()
    } 