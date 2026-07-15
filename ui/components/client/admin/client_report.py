from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, IMG
from django.urls import reverse


def AdminUserDetailCard():
    """
    Deep-dive card for a specific user.
    Combines Auth User data with your Client app data.
    """

    return DIV(
        # Profile Header
        DIV(
            H5("Customer Profile", Class="fw-bold text-primary mb-3"),
            DIV(
                H6({'client.user.username'}, Class="mb-1"),
                P({'client',lambda **dvars:f"Member since {dvars.get('client').user.date_joined.strftime('%b %d, %Y') if dvars.get('client')else 'Never'}"}, Class="text-muted small"),
                Class="border-bottom pb-2 mb-3",
            ),
            Class="mb-3",
        ),
        # Data Grid
        DIV(
            DIV(
                SMALL("Account Status", Class="text-muted d-block small"),
                SPAN(
                    {'client',lambda **dvars:"Verified" if getattr(getattr(dvars.get('client'),'user'),'is_active') else "Unverified" },
                    Class={'client',lambda **dvars:"text-success" if getattr(getattr(dvars.get('client'),'user'),'is_active') else "text-danger" },
                ),
                Class="col-6 border-end",
            ),
            DIV(
                SMALL("Last Seen", Class="text-muted d-block small"),
                SPAN({'client',lambda **dvars:dvars.get('client').user.last_login.strftime("%b %d, %Y") if dvars.get('client') and dvars.get('client').user.last_login else "Never"}, Class="text-dark"),
                Class="col-6 ps-3",
            ),
            Class="row mb-4",
        ),
        # Client specific data (if available)
        DIV(
            H6("Purchase History", Class="small fw-bold text-uppercase text-muted"),
            P("Customer Group: Retail", Class="mb-1 small"),
            (
                P({'client', lambda **dvars:"Total Orders: 12" if dvars.get('client') else "No orders yet."}, Class={'client', lambda **dvars:"mb-0 small text-primary" if dvars.get('client') else "small text-muted"})
            ),
            Class="bg-light p-3 rounded mb-4",
        ),
        # Global Admin Controls
        Class="card shadow-sm p-4 border-3",
        style="max-width: 400px;",
    )
