from probo import DIV, H3, H6, HEADER, INPUT,P
from ui.components.product.product_card import ProductCard
from ui.components.product.client.category_filter import CategoryFilterSidebar
from apps.global_context import get_global_context

def ProductsSection(products,hx_oob=False):

    return DIV(
        DIV(
            *[
                DIV(ProductCard(p,), Class="col-md-4 mb-4")
                for p in products
            ],
            Class="row"
        ),
        Class="col-md-9",
        Id="product-grid-container",
        hx_swap_oob="true" if hx_oob else False,
    )


def ProductCatalog(products=None,categpries=None):
    """Full Product Listing Page."""
    Context = get_global_context()
    products = products or Context.get("product_list", [])  # Get product list from global context
    categpries = categpries or Context.get("product_list", [])  # Get product list from global context

    return DIV(
        HEADER(H3("All Products", Class="fw-bold mb-4"), Class="container mt-5"),
        DIV(
            # Sidebar Filters (Visual only for now)
            CategoryFilterSidebar(categories=categpries),
            # Main Grid
            ProductsSection(products),
            Class="row container mx-auto mb-5",
        ),
    )

# DIV(
#                 H6("Filters", Class="text-uppercase fw-bold text-muted mb-3"),
#                 DIV(
#                     P("Categories", Class="fw-bold mb-2 small"),
#                     *[DIV(
#                         INPUT(type="checkbox", Class="form-check-input me-2",value=cat.slug),
#                         cat.name,

#                         Class="form-check small mb-1",
#                     )
#                       for cat in categpries
#                       ],
#                     Class="mb-4",
#                 ),
#                 Class="col-md-3 pe-4",
#             ),
