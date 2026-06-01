from probo import DIV, H4, H5, P, SPAN, I, BUTTON, SECTION, HR, A
from django.urls import reverse
from ui.components.product.admin.product_details import AdminProductDetailCard, AdminProductVariantDetailCard
from ui.components.product.admin.product_listing import AdminProductList
from ui.components.shared import QuickActionsSection
def LowStockSection(products):
    """Filters and renders variants with stock < 10."""
    low_stock_variants = []
    for product in products:
        for variant in product.variants.filter(is_active=True):
            if variant.stock < 10:
                low_stock_variants.append(AdminProductVariantDetailCard(variant))
    
    return SECTION(
        H5(I(Class="bi bi-exclamation-triangle me-2"), "Low Stock Alerts", Class="text-danger mb-4"),
        DIV(*low_stock_variants, Class="d-flex flex-wrap gap-3") if low_stock_variants else 
        P("Inventory levels are healthy.", Class="text-muted small"),
        id="low-stock-alerts",
        Class="mb-5 p-3 border rounded bg-white shadow-sm"
    )

def NoVariantsSection(products):
    """Filters and renders products that are missing variants."""
    gaps = [AdminProductDetailCard(p) for p in products if not p.variants.exists()]
    
    return SECTION(
        H5(I(Class="bi bi-stack me-2"), "Products Missing Variants", Class="text-warning mb-4"),
        DIV(*gaps, Class="d-flex flex-wrap gap-3") if gaps else 
        P("All products have associated variants.", Class="text-muted small"),
        id="catalog-gaps",
        Class="mb-5 p-3 border rounded bg-white shadow-sm"
    )

def IncompleteVariantsSection(products):
    """Filters and renders variants missing crucial metadata (null/blank)."""
    incomplete = []
    for product in products:
        for variant in product.variants.filter(is_active=True):
            # Check for missing attributes based on your model
            is_incomplete = not all([variant.color, variant.size, variant.fabric])
            if is_incomplete:
                incomplete.append(AdminProductVariantDetailCard(variant))
                
    return SECTION(
        H5(I(Class="bi bi-search me-2"), "Incomplete Data Audit", Class="text-info mb-4"),
        DIV(*incomplete, Class="d-flex flex-wrap gap-3") if incomplete else 
        P("Data integrity is 100%.", Class="text-muted small"),
        id="data-integrity",
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

def AdminProductsDashboard(products):
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
        LowStockSection(products),
        NoVariantsSection(products),
        IncompleteVariantsSection(products),
        AdminProductList(products),
        HR(Class="my-5"),
        ProductQuickActions(),
        Class="container-fluid py-4",
        id="admin-dashboard-root",
    )
