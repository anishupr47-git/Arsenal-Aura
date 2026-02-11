from rest_framework.permissions import BasePermission


class IsArsenalAllowed(BasePermission):
    message = "Banter Gate: switch your club to Arsenal to access this feature."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, "profile", None)
        if not profile:
            return True
        if profile.favorite_club in ["Tottenham Hotspur", "Chelsea"]:
            return False
        return True
