from probo import DIV, H4, P, FORM, INPUT, LABEL, BUTTON, TEXTAREA
from django.urls import reverse
from probo.components import Frag

def AddAddressForm() -> DIV:
    """
    Renders a custom Address Form bound directly to a Django Form instance.
    Extracts bound values and validation errors for a premium UX.
    """
    # is_editing = bool(address_id)

    # --- UI HELPER: Automatically handles values, errors, and styling ---
    def Input_Field(**dvars):
        form=dvars.get('form',)
        name=dvars.get('name',)
        print('<===========Input_Field============>',dvars)
        label=dvars.get('label',)
        input_type=dvars.get('input_type',) or "text"
        placeholder=dvars.get('placeholder',) or ""
        col_class=dvars.get('col_class',) or"mb-3"

        if not form:
            return DIV()

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
    def Textarea_Field(**dvars):
        form = dvars.get('form',)
        name = dvars.get('name') or None
        label = dvars.get('label') or None
        placeholder=""
        rows="3"
        col_class="mb-4"
        if not form:
            return DIV
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
            H4({'title',lambda **dvars:dvars.get('title') or "Edit Address"}, Class="card-title fw-bold mb-4"),
            FORM(
                # 1. Full Name & Phone Number,
                DIV(
                    Frag({'form','name','label','placeholder','col_class',Input_Field},data_pipeline={
                        'name':"full_name",
                        'label':"Full Name",
                        'placeholder':"John Doe",
                        'col_class':"col-md-6 mb-3"}),
                    Frag({'form','name','label','placeholder','col_class','input_type',Input_Field},
                         data_pipeline={
                        'name':"phone_number",
                        'label':"Phone Number",
                        'placeholder':"+1 (555) 000-0000",
                        'input_type':"tel",
                        'col_class':"col-md-6 mb-3"}),
                    Class="row",
                ),
                # 2. Address Lines
                Frag({'form','name','label','placeholder','col_class',Input_Field},
                     data_pipeline={
                        'name':"address_line_1",
                        'label':"Address Line 1",
                        'placeholder':"123 Main St",
                        'col_class':"col-md-6 mb-3",}),
                Frag({'form','name','label','placeholder','col_class',Input_Field},
                     data_pipeline={
                        'name':"address_line_2",
                        'label':"Address Line 2 (Optional)",
                        'placeholder':"Apartment, studio, suite, or floor",
                        'col_class':"col-md-6 mb-3",}),
                # 3. City, State, Postal Code
                DIV(
                    Frag({'form','name','label','placeholder','col_class',Input_Field},data_pipeline={
                        'name':"city",
                        'label':"City",
                        'placeholder':"Apartment, studio, suite, or floor",
                        'col_class':"col-md-4 mb-3",}),
                    Frag({'form','name','label','placeholder','col_class',Input_Field},data_pipeline={
                        'name':"state",
                        'label':"State / Province",
                        'placeholder':"Apartment, studio, suite, or floor",
                        'col_class':"col-md-6 mb-3",}),
                    Frag({'form','name','label','placeholder','col_class',Input_Field},data_pipeline={
                        'name':"postal_code",
                        'label':"Postal Code",
                        'placeholder':"Apartment, studio, suite, or floor",
                        'col_class':"col-md-4 mb-3",}),
                    Class="row",
                ),
                # 4. Country
                Frag({'form','name','label','placeholder',Input_Field},data_pipeline={
                        'name':"country",
                        'label':"Country",
                        'placeholder':"USA",}),
                # 5. Delivery Instructions
                Frag({'form','name','label','placeholder',Textarea_Field},data_pipeline={
                        'name':"delivery_instructions",
                        'label':"Delivery Instructions (Optional)",
                        'placeholder':"E.g., Leave package at the front door, gate code is 1234...",}),
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
                hx_post=reverse("order:add-billing-address",),
                hx_target="#profile-content-area",
                hx_swap="innerHTML",
            ),
            Class="card-body p-4",
        ),
        Class="card border-0 shadow-sm rounded-4",
    )
