from jingo import register


@register.function
def user_is_rep(user):
    """Check if a user belongs to Rep's group."""
    return user.groups.filter(name='Rep').exists()