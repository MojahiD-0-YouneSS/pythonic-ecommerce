from probo import DIV, BUTTON, SPAN, P
def get_messages() -> DIV:
    """
    Renders Django contrib.messages using Bootstrap alert classes.
    Expects the standard Django messages object from the template context.
    """
    def django_messages(**dvars,):
        messages = dvars.get('django_messages',[])
        clear_messages = dvars.get('clear_messages',False)

        if not messages:
            return DIV("", style="display: none;")


        # Map Django message tags to Bootstrap alert classes
        # Django tags: debug, info, success, warning, error
        tag_mapping = {
            'debug': 'alert-secondary',
            'info': 'alert-info',
            'success': 'alert-success',
            'warning': 'alert-warning',
            'error': 'alert-danger',
        }

        alert_list = [

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
                    Class=f"alert {tag_mapping.get(message.tags, 'alert-primary')} alert-dismissible fade show shadow-sm mb-3 pe-auto",
                    role="alert",
                )

        for message in messages
        ]
        return alert_list
    return DIV(DIV(
        {'django_messages',django_messages},
                Class="messages-container mt-3",
            ),
            Id="messages-container",
            Class="toast-container position-fixed bottom-0 end-0 p-3",
            style="z-index: 1055;",
            data_ssdom_id="root-messages-container",
            hx_swap_oob={"hx_oob"}
        )
