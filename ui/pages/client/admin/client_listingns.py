from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, IMG
from django.urls import reverse

def AdminUserListingCard() -> DIV:
    """
    A compact row-style card for user listings.
    Focuses on quick identification and status.
    """
    return DIV(
        DIV(
            # Avatar / Initial
            DIV(
                SPAN({'client.user', lambda **dvars: dvars.get('client').user.username[0].upper() if getattr(dvars.get('client'), 'user', None) else "N/A"}, Class="fw-bold text-primary"),
                Class="rounded-circle bg-light d-flex align-items-center justify-content-center border me-3",
                style="width: 48px; height: 48px;",
            ),
            # Identity
            DIV(
                H6(
                    {'client.user', lambda **dvars: dvars.get('client').user.get_full_name() or dvars.get('client').user.username if getattr(dvars.get('client'), 'user', None) else "Unknown"},
                    Class="mb-0 fw-bold",
                ),
                SMALL({'client.user', lambda **dvars: dvars.get('client').user.email if getattr(dvars.get('client'), 'user', None) else "No email"}, Class="text-muted d-block"),
                Class="flex-grow-1",
            ),
            # Badges
            DIV(
                {'client.user', lambda **dvars: SPAN("Staff", Class="badge bg-info text-dark me-1") if getattr(dvars.get('client'), 'user', None) and getattr(dvars.get('client').user, 'is_staff', False) else ""},
                {'client.user', lambda **dvars: SPAN("Active" if getattr(dvars.get('client').user, 'is_active', False) else "Inactive", Class=f"badge bg-{'success' if getattr(dvars.get('client').user, 'is_active', False) else 'secondary'} small") if getattr(dvars.get('client'), 'user', None) else ""},
                Class="text-end",
            ),
            Class="d-flex align-items-center mb-3",
        ),
        # Actions
        DIV(
            A(
                I(Class="bi bi-eye me-1"),
                "Details",
                href={'client', lambda **dvars: reverse("client:client_detail", kwargs={"user_id": dvars.get('client').id}) if dvars.get('client') else "#"},
                Class="btn btn-sm btn-outline-primary flex-fill me-2",
            ),
            BUTTON(
                I(Class="bi bi-shield-lock"),
                Class="btn btn-sm btn-outline-warning me-2",
                hx_post={'client', lambda **dvars: reverse("client:client_detail", kwargs={"user_id": dvars.get('client').id}) if dvars.get('client') else "#"},
                title="Toggle Staff Access",
            ),
            BUTTON(
                I(Class="bi bi-trash"),
                Class="btn btn-sm btn-outline-danger",
                hx_delete={'client', lambda **dvars: reverse("client:client_detail", kwargs={"user_id": dvars.get('client').id}) if dvars.get('client') else "#"},
                hx_confirm="Delete user?",
            ),
            Class="d-flex border-top pt-2",
        ),
        Class="card shadow-sm p-3 mb-2 border-0",
        style="width: 100%; max-width: 450px;",
    )
