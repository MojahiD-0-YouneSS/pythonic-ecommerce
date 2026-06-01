from probo import DIV, H4, LABEL, BUTTON, TEXTAREA, SELECT, INPUT, SMALL, FORM, P, I
from probo.utility import ProboSourceString
from ui.components.product.form_button import form_button
from ui.components.crf_token import CsrfToken

def AdminForm(form, action,**attrs) -> FORM:
    """
    Renders a Django form into a polished Bootstrap 5 Admin UI.
    """

    return FORM(
        DIV(CsrfToken(), ProboSourceString(form), form_button(), Class="row g-4"),
        method="POST",
        enctype="multipart/form-data",
        action=action,
        **attrs
    )

def FormConfirmation(
    title=None,
    message=None,
    icon_class=None,
    color_theme=None,
) -> DIV:
    """
    A beautiful, centered success state to display after a form submission.
    Designed to fit perfectly inside a modal or a standard dashboard card.
    """

    title = title or "Item Saved!"

    message = message or "The record has been updated successfully."

    icon_class = icon_class or "bi-check-circle-fill"

    color_theme = color_theme or "success"

    return DIV(
        # Large Icon
        DIV(
            I(
                Class=f"bi {icon_class} text-{color_theme}",
                style="font-size: 4rem; line-height: 1;",
            ),
            Class="mb-3 animate__animated animate__bounceIn",  # Optional: Add animate.css classes if you use them!
        ),
        # Typography
        H4(title, Class="fw-bold text-dark mb-2"),
        P(message, Class="text-muted mb-4"),
        # Close/Done Button (Natively dismisses the Bootstrap modal!)
        BUTTON(
            "Done",
            Type="button",
            Class=f"btn btn-{color_theme} px-5 rounded-pill fw-bold shadow-sm",
            data_bs_dismiss="modal",  # This closes the hovering modal automatically
        ),
        # Layout classes for perfect centering
        Class="d-flex flex-column align-items-center justify-content-center p-4 py-5 text-center w-100",
    )
