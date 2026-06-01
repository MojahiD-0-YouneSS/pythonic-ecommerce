from probo import DIV, H4, P, FORM, INPUT, LABEL, BUTTON, TEXTAREA
from django.urls import reverse

def AddAddressForm(form, address_id=None) -> DIV:
    """
    Renders a custom Address Form bound directly to a Django Form instance.
    Extracts bound values and validation errors for a premium UX.
    """
    # is_editing = bool(address_id)
    title = "Edit Address" #if is_editing else "Add New Address"
    post_url = (
        reverse(
            "order:add-billing-address",
        )  # kwargs={addr.get('id')})
        # if is_editing
        # else "/client/profile/addresses/add/"
    )

    # --- UI HELPER: Automatically handles values, errors, and styling ---
    def InputField(name, label, input_type="text", placeholder="", col_class="mb-3"):
        field = form[name]
        has_error = bool(field.errors)

        # Safely extract value, default to empty string if None
        val = field.value()
        val = str(val) if val is not None else ""

        # Add Bootstrap error class if validation failed
        css_class = f"form-control {'is-invalid border-danger' if has_error else ''}"

        return DIV(
            LABEL(label, Class="form-label text-muted small"),
            INPUT(
                Type=input_type,
                name=name,
                value=val,
                Class=css_class,
                placeholder=placeholder,
            ),
            # Inject the specific Django validation error immediately under the input
            (
                DIV(field.errors[0], Class="invalid-feedback d-block fw-medium")
                if has_error
                else ""
            ),
            Class=col_class,
        )

    # --- TEXTAREA HELPER for delivery instructions ---
    def TextareaField(name, label, placeholder="", rows="3", col_class="mb-4"):
        field = form[name]
        has_error = bool(field.errors)
        val = field.value()
        val = str(val) if val is not None else ""
        css_class = f"form-control {'is-invalid border-danger' if has_error else ''}"

        return DIV(
            LABEL(label, Class="form-label text-muted small"),
            TEXTAREA(
                val, name=name, Class=css_class, rows=rows, placeholder=placeholder
            ),
            (
                DIV(field.errors[0], Class="invalid-feedback d-block fw-medium")
                if has_error
                else ""
            ),
            Class=col_class,
        )

    return DIV(
        DIV(
            H4(title, Class="card-title fw-bold mb-4"),
            FORM(
                # 1. Full Name & Phone Number,
                DIV(
                    InputField(
                        "full_name",
                        "Full Name",
                        placeholder="John Doe",
                        col_class="col-md-6 mb-3",
                    ),
                    InputField(
                        "phone_number",
                        "Phone Number",
                        input_type="tel",
                        placeholder="+1 (555) 000-0000",
                        col_class="col-md-6 mb-3",
                    ),
                    Class="row",
                ),
                # 2. Address Lines
                InputField(
                    "address_line_1", "Address Line 1", placeholder="123 Main St"
                ),
                InputField(
                    "address_line_2",
                    "Address Line 2 (Optional)",
                    placeholder="Apartment, studio, suite, or floor",
                ),
                # 3. City, State, Postal Code
                DIV(
                    InputField("city", "City", col_class="col-md-4 mb-3"),
                    InputField("state", "State / Province", col_class="col-md-4 mb-3"),
                    InputField("postal_code", "Postal Code", col_class="col-md-4 mb-3"),
                    Class="row",
                ),
                # 4. Country
                InputField("country", "Country"),
                # 5. Delivery Instructions
                TextareaField(
                    "delivery_instructions",
                    "Delivery Instructions (Optional)",
                    placeholder="E.g., Leave package at the front door, gate code is 1234...",
                ),
                # 6. Action Buttons
                DIV(
                    BUTTON(
                        "Cancel",
                        Type="button",
                        Class="btn btn-light me-2 px-4",
                        hx_get="/client/profile/addresses/",
                        hx_target="#profile-content-area",
                        hx_swap="innerHTML",
                    ),
                    BUTTON("Save Address", Type="submit", Class="btn btn-dark px-4"),
                    Class="mt-2 pt-3 border-top",
                ),
                # HTMX Integration
                hx_post=post_url,
                hx_target="#profile-content-area",
                hx_swap="innerHTML",
            ),
            Class="card-body p-4",
        ),
        Class="card border-0 shadow-sm rounded-4",
    )
