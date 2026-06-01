from probo import DIV,BUTTON

def form_button() -> DIV:
    return DIV([
            BUTTON("Save Product", type="submit", Class="btn btn-primary w-100 mt-3"),
            BUTTON("Discard", type="reset", Class="btn btn-link btn-sm w-100 mt-2 text-muted")
        ], Class="col-md-4")


def form_field_wrapper(field):

    return DIV(
        field,
    Class="mb-3").render()