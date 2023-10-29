from django import template

register = template.Library()


@register.filter
def latest_message(model_instance, friend):
    return model_instance.latest_message_with_friend(friend)
