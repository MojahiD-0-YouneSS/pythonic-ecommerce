from probo import DIV, BUTTON, SPAN, P
from apps.global_context import get_global_context
def get_messages(messages=None,hx_oob=False) -> DIV:
    """
    Renders Django contrib.messages using Bootstrap alert classes.
    Expects the standard Django messages object from the template context.
    """
    Context = get_global_context()
    django_messages = Context.get('django_messages')
    messages = messages or django_messages or []
    if not messages:
        return DIV("", style="display: none;")

    alert_list = []

    # Map Django message tags to Bootstrap alert classes
    # Django tags: debug, info, success, warning, error
    tag_mapping = {
        'debug': 'alert-secondary',
        'info': 'alert-info',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger',
    }

    for message in messages:
        # Determine the correct CSS class based on the message tag
        alert_class = tag_mapping.get(message.tags, 'alert-primary')

        alert_list.append(
            DIV(
                # Message Content
                SPAN(str(message)),
                # Bootstrap Close Button
                BUTTON(
                    Type="button",
                    Class="btn-close",
                    data_bs_dismiss="alert",
                    aria_label="Close",
                ),
                Class=f"alert {alert_class} alert-dismissible fade show shadow-sm mb-3 pe-auto",
                role="alert",
            )
        )
    if Context.get('clear_messages'):
        Context.clear('django_messages')
        Context.clear('clear_messages')
    return DIV(
        *alert_list,
        Class="messages-container mt-3",
        hx_swap_oob="innerHTML:#messages-container" if hx_oob else False,
    )
