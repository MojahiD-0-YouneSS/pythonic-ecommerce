from probo import DIV, H4, H5, P, SPAN, I, BUTTON, SECTION, HR, A
from probo.components import Frag
from django.urls import reverse
from ui.components.product.admin.product_details import AdminProductDetailCard, AdminProductVariantDetailCard
from ui.components.product.admin.product_listing import AdminProductList
from ui.components.shared import QuickActionsSection

def LowStockSection():
    """Filters and renders variants with stock < 10."""
    def low_stock_section(**dvars):
        products = dvars.get('all_products') or []
        if not products:
            return P("Inventory levels are healthy.", Class="text-muted small")
        low_stock_variants = []
        for product in products:
            for variant in product.variants.filter(is_active=True):
                if variant.stock < 10:
                    low_stock_variants.append(Frag(AdminProductVariantDetailCard(),data_pipeline={'variant':variant}))
        return DIV(
            DIV(*low_stock_variants, Class="d-flex flex-wrap gap-3"),
            style="max-height: 350px; overflow-y: auto; scrollbar-width: thin; overflow-x: hidden;",
            Class="pe-2"
        )
    return SECTION(
        H5(I(Class="bi bi-exclamation-triangle me-2"), "Low Stock Alerts", Class="text-danger mb-4"),
        {'all_products',low_stock_section},
        Id="low-stock-alerts",
        Class="mb-5 p-3 border rounded bg-white shadow-sm"
    )

def NoVariantsSection():
    """Filters and renders products that are missing variants."""
    def no_variant_section(**dvars):
        products = dvars.get('all_products') or []
        if not products:
            return P("All products have associated variants.", Class="text-muted small")
        gaps = [Frag(AdminProductDetailCard(),data_pipeline={'product':p}) for p in products if not p.variants.exists()]
        return DIV(
            DIV(*gaps, Class="d-flex flex-wrap gap-3"),
            style="max-height: 350px; overflow-y: auto; scrollbar-width: thin; overflow-x: hidden;",
            Class="pe-2"
        )

    return SECTION(
        H5(I(Class="bi bi-stack me-2"), "Products Missing Variants", Class="text-warning mb-4"),
        {'all_products',no_variant_section},
        Id="catalog-gaps",
        Class="mb-5 p-3 border rounded bg-white shadow-sm"
    )

def IncompleteVariantsSection():
    """Filters and renders variants missing crucial metadata (null/blank)."""
    def incomplete_inventory(**dvars):
        products = dvars.get('all_products') or []
        if not products:
            return P("Data integrity is 100%.", Class="text-muted small")
        incomplete = []
        for product in products:
            for variant in product.variants.filter(is_active=True):
                # Check for missing attributes based on your model
                is_incomplete = not all([variant.color, variant.size, variant.fabric])
                if is_incomplete:
                    incomplete.append(Frag(AdminProductVariantDetailCard(),data_pipeline={'variant':variant}))
        return DIV(
            DIV(*incomplete, Class="d-flex flex-wrap gap-3"),
            style="max-height: 350px; overflow-y: auto; scrollbar-width: thin; overflow-x: hidden;",
            Class="pe-2"
        )
    return SECTION(
        H5(I(Class="bi bi-search me-2"), "Incomplete Data Audit", Class="text-info mb-4"),
        {'all_products',incomplete_inventory},
        Id="data-integrity",
        Class="mb-5 p-3 border rounded bg-white shadow-sm"
    )

def ProductQuickActions():
    """Centralized navigation for adding new catalog items."""
    
    info = {
        "product": reverse("product:product"),
        "product Variant": reverse("product:variant"),
        "category": reverse("product:category"),
        "image": reverse("product:image"),
        "review": reverse("product:review"),
        "reply": reverse("product:reply"),
    }
    
    return QuickActionsSection(**info)

def AdminProductsDashboard():
    """
    Main Orchestrator Component.
    Takes a single products queryset and distributes it to child modules.
    """
    return DIV(
        DIV(
            H4("Product Operations Hub", Class="fw-bold mb-1"),
            P(
                "Automated inventory and catalog health monitoring.",
                Class="text-muted small",
            ),
            Class="mb-4",
        ),
        # Modular Components
        {'products', 'all_products', lambda **dvars: (
            DIV("No product data available.", Class="alert alert-warning")if not (dvars.get('all_products')) else

        DIV(LowStockSection(),
        NoVariantsSection(),
        IncompleteVariantsSection(),
        AdminProductList(),
        HR(Class="my-5"),
        ProductQuickActions(),data_pipeline=dvars)
        )},
        Class="container-fluid py-4",
        Id="admin-dashboard-root",
    )
