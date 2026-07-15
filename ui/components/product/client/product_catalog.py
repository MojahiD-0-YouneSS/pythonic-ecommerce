from ui.components.product.product_card import ProductCard
from ui.components.product.client.category_filter import CategoryFilterSidebar
from probo.components import Frag
from probo import DIV, H3, H6, HEADER, BUTTON, P, A, SPAN

from django.urls import reverse

def PaginationComponent():
    def pagination_component(**dvars):
        page_obj = dvars.get('page_obj')
        query_string = dvars.get('query_string', '')
        base_url = dvars.get('base_url', '')
        
        if not page_obj or not page_obj.has_other_pages():
            return str()
            
        # We append the query string to preserve category filters
        prefix = f"&{query_string}" if query_string else ""
        
        separator = "&" if "?" in base_url else "?"
        
        prev_url = f"{base_url}{separator}page={page_obj.previous_page_number()}{prefix}" if page_obj.has_previous() else ""
        next_url = f"{base_url}{separator}page={page_obj.next_page_number()}{prefix}" if page_obj.has_next() else ""
        
        # If HTMX is used, we usually specify an HTMX target. For now, assume if base_url is set, it might be an HTMX call, but let's just make it a generic link if hx_target isn't provided.
        hx_target = dvars.get('hx_target')
        
        if hx_target:
            prev_btn = BUTTON(
                "Previous", 
                Class="btn btn-outline-dark me-3",
                hx_get=prev_url,
                hx_target=hx_target,
                hx_swap="outerHTML"
            ) if prev_url else SPAN()
            
            next_btn = BUTTON(
                "Next", 
                Class="btn btn-outline-dark ms-3",
                hx_get=next_url,
                hx_target=hx_target,
                hx_swap="outerHTML"
            ) if next_url else SPAN()
        else:
            prev_btn = A("Previous", href=prev_url, Class="btn btn-outline-dark me-3") if prev_url else SPAN()
            next_btn = A("Next", href=next_url, Class="btn btn-outline-dark ms-3") if next_url else SPAN()
        
        return DIV(
            prev_btn,
            SPAN(f"Page {page_obj.number} of {page_obj.paginator.num_pages}", Class="text-muted fw-bold"),
            next_btn,
            Class="d-flex justify-content-center align-items-center mt-5 mb-5 w-100"
        )
    return DIV({'page_obj', 'query_string', 'base_url', 'hx_target', pagination_component})
def ProductsSection():
    def products_section(**dvars):
        products = dvars.get('products') or []
        return DIV(
            DIV(
                *[
                    DIV(Frag(ProductCard(),data_pipeline={'product':p}), Class="col-md-4 mb-4")
                    for p in products
                ],
                Class="row"
            ),
            Frag(PaginationComponent(), data_pipeline={
                "page_obj": dvars.get("page_obj"), 
                "query_string": dvars.get("query_string", ""),
                "base_url": reverse("product:product-filter"),
                "hx_target": "#product-grid-container"
            })
        )
    return DIV(
        {'products', 'page_obj', 'query_string', products_section},
        Class="col-md-9",
        Id="product-grid-container",
        hx_swap_oob={'hx_oob',lambda **dvars:"true" if dvars.get('hx_oob') else False},
    )


def ProductCatalog():
    """Full Product Listing Page."""
    def product_catalog(**dvars):
        products = dvars.get("products", [])  # Get product list from global context
        categories = dvars.get("categories", [])  # Get product list from global context
        return DIV(
            # Sidebar Filters (Visual only for now)
            CategoryFilterSidebar(categories=categories),
            # Main Grid
            Frag(ProductsSection(), data_pipeline={"products": products, "page_obj": dvars.get("page_obj"), "query_string": dvars.get("query_string", "")}),
            Class="row container mx-auto mb-5",
        )
    return DIV(
        HEADER(H3("All Products", Class="fw-bold mb-4"), Class="container mt-5"),
        {'products', 'categories', 'page_obj', 'query_string', product_catalog},
    )
