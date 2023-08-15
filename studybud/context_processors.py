from .models import UserProfile

def get_profile(request):
    if request.user.is_authenticated:
        user_profile, create = UserProfile.objects.get_or_create(user=request.user)
        return {'user_profile': user_profile}
    return {}