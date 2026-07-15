from probo import DIV, H4, BUTTON, FORM, P, I
from ui.components.product.form_button import form_button

def AdminForm() -> FORM:
    """
    Renders a Django form into a polished Bootstrap 5 Admin UI.
    """

    return FORM(
        DIV( {'rdt_form'}, form_button(), Class="row g-4"),
        method="POST",
        enctype="multipart/form-data",
        action={'action'},
    )

def FormConfirmation() -> DIV:
    """
    A beautiful, centered success state to display after a form submission.
    Designed to fit perfectly inside a modal or a standard dashboard card.
    """
    return DIV(
        # Large Icon
        DIV(
            I(
                Class={'icon_class','color_theme', lambda **dvars:f"bi {dvars.get('icon_class') or 'bi-check-circle-fill'} text-{dvars.get('color_theme') or 'success'}"},
                style="font-size: 4rem; line-height: 1;",
            ),
            Class="mb-3 animate__animated animate__bounceIn",  # Optional: Add animate.css classes if you use them!
        ),
        # Typography
        H4({'title',lambda **dvars:dvars.get('title') or "Item Saved!"}, Class="fw-bold text-dark mb-2"),
        P({'message',lambda **dvars:dvars.get('message') or "The record has been updated successfully."}, Class="text-muted mb-4"),
        # Close/Done Button (Natively dismisses the Bootstrap modal!)
        BUTTON(
            "Done",
            Type="button",
            Class={'color_theme',lambda **dvars:f"btn btn-{dvars.get('color_theme') or 'success'} px-5 rounded-pill fw-bold shadow-sm"},
            data_bs_dismiss="modal",  # This closes the hovering modal automatically
        ),
        # Layout classes for perfect centering
        Class="d-flex flex-column align-items-center justify-content-center p-4 py-5 text-center w-100",
    )
