import re

from django.conf import settings
from furl import furl

from karrot.groups.models import GroupNotificationType
from karrot.unsubscribe.utils import generate_token


def message_url(message):
    if message.is_thread_reply():
        return thread_url(message.thread)
    else:
        return conversation_url(message.conversation, message.author)


def conversation_url(conversation, user):
    type = conversation.type()
    if type == 'group':
        return group_wall_url(conversation.target)
    elif type == 'place':
        return place_wall_url(conversation.target)
    elif type == 'activity':
        return activity_detail_url(conversation.target)
    elif type == 'private':
        return user_detail_url(user)
    elif type == 'application':
        return application_url(conversation.target)
    elif type == 'issue':
        return issue_chat_url(conversation.target)
    elif type == 'offer':
        return offer_url(conversation.target)
    elif type is None:
        return None

    raise Exception('conversation url with type {} is not defined'.format(type))


def place_url(place):
    return '{hostname}/#/group/{group_id}/place/{place_id}/activities'.format(
        hostname=settings.HOSTNAME,
        group_id=place.group.id,
        place_id=place.id,
    )


def user_url(user):
    return '{hostname}/#/user/{user_id}/'.format(
        hostname=settings.HOSTNAME,
        user_id=user.id,
    )


def absolute_url(path):
    if re.match(r"https?:", path):
        return path
    return '{hostname}{path}'.format(
        hostname=settings.HOSTNAME,
        path=path,
    )


def activity_detail_url(activity):
    place = activity.place
    group = place.group
    return '{hostname}/#/group/{group_id}/place/{place_id}/activities/{activity_id}/detail'.format(
        hostname=settings.HOSTNAME,
        group_id=group.id,
        place_id=place.id,
        activity_id=activity.id,
    )


def activity_notification_unsubscribe_url(user, group):
    return unsubscribe_url(user, group, notification_type=GroupNotificationType.DAILY_ACTIVITY_NOTIFICATION)


def group_summary_unsubscribe_url(user, group):
    return unsubscribe_url(user, group, notification_type=GroupNotificationType.WEEKLY_SUMMARY)


def new_application_unsubscribe_url(user, application):
    return unsubscribe_url(
        user,
        group=application.group,
        conversation=application.conversation,
        notification_type=GroupNotificationType.NEW_APPLICATION,
    )


def new_offer_unsubscribe_url(user, offer):
    return unsubscribe_url(
        user,
        group=offer.group,
        notification_type=GroupNotificationType.NEW_OFFER,
    )


def group_photo_url(group):
    if not group or not group.photo:
        return None
    return '{hostname}/api/groups-info/{group_id}/photo/'.format(hostname=settings.HOSTNAME, group_id=group.id)


def karrot_logo_url():
    return settings.KARROT_LOGO


def group_photo_or_karrot_logo_url(group):
    return group_photo_url(group) or karrot_logo_url()


def offer_image_url(offer):
    image = offer.images.first()
    if not image:
        return None
    return '{hostname}/api/offers/{offer_id}/image/'.format(hostname=settings.HOSTNAME, offer_id=offer.id)


def conflict_resolution_unsubscribe_url(user, issue):
    return unsubscribe_url(
        user,
        group=issue.group,
        conversation=issue.conversation,
        notification_type=GroupNotificationType.CONFLICT_RESOLUTION,
    )


def application_url(application):
    return '{hostname}/#/group/{group_id}/applications/{application_id}'.format(
        hostname=settings.HOSTNAME,
        group_id=application.group.id,
        application_id=application.id,
    )


def offer_url(offer):
    return '{hostname}/#/group/{group_id}/offers/{offer_id}'.format(
        hostname=settings.HOSTNAME,
        group_id=offer.group.id,
        offer_id=offer.id,
    )


def issue_url(issue):
    return '{hostname}/#/group/{group_id}/issues/{issue_id}'.format(
        hostname=settings.HOSTNAME,
        group_id=issue.group.id,
        issue_id=issue.id,
    )


def issue_chat_url(issue):
    return issue_url(issue) + '/chat'


def user_detail_url(user):
    return '{hostname}/#/user/{user_id}/detail'.format(
        hostname=settings.HOSTNAME,
        user_id=user.id,
    )


def thread_url(thread):
    """
    Assumes that thread.conversation.target is a group
    """
    return '{hostname}/#/group/{group_id}/message/{message_id}/replies'.format(
        hostname=settings.HOSTNAME,
        group_id=thread.conversation.target_id,
        message_id=thread.id,
    )


def thread_unsubscribe_url(user, group, thread):
    return unsubscribe_url(user, group, thread=thread)


def group_wall_url(group):
    return '{hostname}/#/group/{group_id}/wall'.format(hostname=settings.HOSTNAME, group_id=group.id)


def place_wall_url(place):
    return '{hostname}/#/group/{group_id}/place/{place_id}/wall'.format(
        hostname=settings.HOSTNAME, group_id=place.group.id, place_id=place.id
    )


def applications_url(group):
    return '{hostname}/#/group/{group_id}/applications'.format(
        hostname=settings.HOSTNAME,
        group_id=group.id,
    )


def group_preview_url(group):
    return '{hostname}/#/groupPreview/{group_id}'.format(
        hostname=settings.HOSTNAME,
        group_id=group.id,
    )


def group_edit_url(group):
    return '{hostname}/#/group/{group_id}/edit'.format(
        hostname=settings.HOSTNAME,
        group_id=group.id,
    )


def conversation_unsubscribe_url(user, conversation, group=None):
    return unsubscribe_url(user, group=group, conversation=conversation)


def unsubscribe_url(user, group=None, conversation=None, thread=None, notification_type=None):
    return '{hostname}/#/unsubscribe/{token}'.format(
        hostname=settings.HOSTNAME,
        token=generate_token(
            user,
            group=group,
            conversation=conversation,
            thread=thread,
            notification_type=notification_type,
        ),
    )


def group_settings_url(group):
    return '{hostname}/#/group/{group_id}/settings'.format(
        hostname=settings.HOSTNAME,
        group_id=group.id,
    )


def invite_url(invitation):
    invite_url = furl('{hostname}/#/signup'.format(hostname=settings.HOSTNAME))
    invite_url.fragment.args = {'invite': invitation.token, 'email': invitation.email}
    return invite_url


def user_delete_url(code):
    return '{hostname}/#/delete-user?code={code}'.format(hostname=settings.HOSTNAME, code=code)


def user_emailverification_url(code):
    return '{hostname}/#/email/verify?code={code}'.format(hostname=settings.HOSTNAME, code=code)


def user_passwordreset_url(code):
    return '{hostname}/#/password/reset?code={code}'.format(hostname=settings.HOSTNAME, code=code)


def logo_url():
    return '{hostname}/statics/carrot_logo.png'.format(hostname=settings.HOSTNAME, )
