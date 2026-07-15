from probo import DIV, H2, A, SPAN
from django.urls import reverse
from probo.components import Frag

def PaginationComponent():
    def pagination_component(**dvars):
        page_obj = dvars.get('page_obj')
        if not page_obj or not page_obj.has_other_pages():
            return str()
            
        prev_btn = A("Previous", href=f"?page={page_obj.previous_page_number()}", Class="btn btn-outline-dark me-3") if page_obj.has_previous() else SPAN()
        next_btn = A("Next", href=f"?page={page_obj.next_page_number()}", Class="btn btn-outline-dark ms-3") if page_obj.has_next() else SPAN()
        
        return DIV(
            prev_btn,
            SPAN(f"Page {page_obj.number} of {page_obj.paginator.num_pages}", Class="text-muted fw-bold"),
            next_btn,
            Class="d-flex justify-content-center align-items-center mt-5 mb-5 w-100"
        )
    return DIV({'page_obj', pagination_component})

def AdminProductList():
    def process_product_items(**dvars):
        products = dvars.get('products') or []
        product_items = []
        for product in products:
            item = DIV(
                H2(product.name),
                DIV(
                    A(
                        "Edit",
                        href=reverse(
                            "product:admin-product-edit", kwargs={"product_id": product.id}
                        ),
                        Class="nav-link",
                    ),
                    Class="me-2 btn btn-primary btn-sm",
                ),
                DIV(
                    A(
                        "View",
                        href=reverse(
                            "product:admin-product-detail",
                            kwargs={"product_id": product.id},
                        ),
                        Class="nav-link",
                    ),
                    Class="me-2 btn btn-outline-secondary btn-sm",
                ),
                Class="border p-3 mb-3 rounded col-md-4",
            )
            product_items.append(item)
        return DIV(
            DIV(*product_items,Class="row"),
            style="max-height: 400px; overflow-y: auto; scrollbar-width: thin; overflow-x: hidden;",
            Class="pe-2 mb-3"
        )

    return DIV(
        {'products',process_product_items}, 
        Frag(PaginationComponent()),
        Class="admin-product-list"
    )
