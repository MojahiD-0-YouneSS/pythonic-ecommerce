from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, IMG
from django.urls import reverse

def AdminUserListingCard(user):
    """
    A compact row-style card for user listings.
    Focuses on quick identification and status.
    """
    if user is None:

        return DIV(
            DIV(
                # Avatar / Initial
                DIV(
                    SPAN("nothing to see here!!".upper(), Class="fw-bold text-primary"),
                    Class="d-flex align-items-center justify-content-center",
                    style="width: 100%; height: 28px;"
                ),
                Class="d-flex align-items-center mb-3"
            ),
            Class="p-3 mb-2",
            style="width: 100%; max-width: 450px;"
        )
    status_color = "success" if user.is_active else "secondary"
    # Assuming user might have a related Client profile
    is_staff = user.user.is_staff

    return DIV(
        DIV(
            # Avatar / Initial
            DIV(
                SPAN(user.user.username[0].upper(), Class="fw-bold text-primary"),
                Class="rounded-circle bg-light d-flex align-items-center justify-content-center border me-3",
                style="width: 48px; height: 48px;",
            ),
            # Identity
            DIV(
                H6(
                    user.user.get_full_name() or user.user.username,
                    Class="mb-0 fw-bold",
                ),
                SMALL(user.user.email, Class="text-muted d-block"),
                Class="flex-grow-1",
            ),
            # Badges
            DIV(
                SPAN("Staff", Class="badge bg-info text-dark me-1") if is_staff else "",
                SPAN(
                    "Active" if user.user.is_active else "Inactive",
                    Class=f"badge bg-{status_color} small",
                ),
                Class="text-end",
            ),
            Class="d-flex align-items-center mb-3",
        ),
        # Actions
        DIV(
            A(
                I(Class="bi bi-eye me-1"),
                "Details",
                href=reverse("client:client_detail", kwargs={"user_id": user.id}),
                Class="btn btn-sm btn-outline-primary flex-fill me-2",
            ),
            BUTTON(
                I(Class="bi bi-shield-lock"),
                Class="btn btn-sm btn-outline-warning me-2",
                hx_post=reverse("client:client_detail", kwargs={"user_id": user.id}),
                title="Toggle Staff Access",
            ),
            BUTTON(
                I(Class="bi bi-trash"),
                Class="btn btn-sm btn-outline-danger",
                hx_delete=reverse("client:client_detail", kwargs={"user_id": user.id}),
                hx_confirm="Delete user?",
            ),
            Class="d-flex border-top pt-2",
        ),
        Class="card shadow-sm p-3 mb-2 border-0",
        style="width: 100%; max-width: 450px;",
    )
