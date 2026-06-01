from probo import DIV, H5, BUTTON, I 
from probo.styles.frameworks.bs5.components import BS5Modal

def AdminEditModal(title=None, modal_id=None, content=None) -> BS5Modal:
    """
    A reusable Bootstrap 5 dismissable modal for hovering forms over the dashboard.

    Args:
        title (str): The header text for the modal.
        modal_id (str): Unique ID for the modal (used for JS toggling).
        content (probo component): The actual form or content to inject inside.
    """
    title, modal_id, content = title or "Edit Item", modal_id or "adminEditModal", content or None
    # If no content is provided, render an empty state (useful for HTMX targeting)
    inner_content = (
        content if content else DIV("Loading...", Class="p-4 text-center text-muted")
    )
    modal = BS5Modal(
        Class="modal fade",
        Id=modal_id,
        tabindex="-1",
        aria_labelledby=f"{modal_id}Label",
        aria_hidden="true",
    )
    modal.add_modal_header(title=title, Id=modal_id,Class="modal-title fw-bold",)
    modal.add_modal_body(inner_content, Class="modal-body",Id='admin-edit-modal-body')
    # return DIV(
    #     DIV(
    #         DIV(
    #             # Modal Header
    #             DIV(
    #                 BUTTON(
    #                     Type="button",
    #                     Class="btn-close",
    #                     data_bs_dismiss="modal",
    #                     aria_label="Close",
    #                 ),
    #                 Class="modal-header border-bottom-0 pb-0",
    #             ),
    #             # Modal Body (Where your injected form lives)
    #             DIV(inner_content, Class="modal-body"),
    #             # We omit a standard modal-footer because your forms
    #             # (like OrderManagementPage) usually have their own "Save/Cancel" buttons.
    #             Class="modal-content shadow-lg border-0 rounded-4",
    #         ),
    #         # Modal Dialog Configuration (centered, max width)
    #         Class="modal-dialog modal-dialog-centered modal-lg",
    #     ),
    #     # Modal Container Configuration
    #     Class="modal fade",
    #     id=modal_id,
    #     tabindex="-1",
    #     aria_labelledby=f"{modal_id}Label",
    #     aria_hidden="true",
    # )

    return modal
