from probo import BUTTON, DIV, H5, H6, P, SPAN, A, I, SMALL, IMG
from django.urls import reverse
from probo.components import Frag

def AdminProductVariantDetailCard() -> Frag:
    """
    A robust admin card for ProductVariant model instances.
    Uses flat argument structure to prevent Probo rendering/bypass errors.
    """
    def product_variant_card(**dvars):
        variant = dvars.get('variant')
        if not variant:
            return DIV("No variant data available.", Class="alert alert-warning p-3")

        # 1. Logic & Helpers
        status_color = "success" if variant.is_active else "secondary"
        status_text = "Active" if variant.is_active else "Inactive"
        stock_color = "danger" if variant.stock < 10 else "dark"

        # Handle Price logic (Base vs Promo)
        has_promo = variant.promo_price and variant.promo_price < variant.base_price
        price_display = (
            DIV(
                H6(f"${variant.promo_price}", Class="mb-0 text-danger fw-bold d-inline"),
                SMALL(
                    f"${variant.base_price}",
                    Class="text-muted text-decoration-line-through ms-2 small",
                ),
                Class="d-flex align-items-center",
            )
            if has_promo
            else H6(f"${variant.base_price}", Class="mb-0 text-primary fs-5")
        )

        # 2. Attribute Badges (Color, Size, Fabric etc.)
        attributes = []
        if variant.color:
            attributes.append(
                SPAN(variant.color, Class="badge bg-light text-dark border me-1")
            )
        if variant.size:
            attributes.append(
                SPAN(variant.size, Class="badge bg-light text-dark border me-1")
            )
        if variant.fabric:
            attributes.append(
                SPAN(variant.fabric, Class="badge bg-light text-dark border me-1")
            )
        return DIV(
        DIV(
            # Header Row: Thumbnail and Title
            DIV(
                # Use variant image if exists, else fallback to parent or placeholder
                DIV(
                    H5(
                        f"{variant.product.name}",
                        Class="mb-0 fw-bold fs-6 text-truncate",
                        style="max-width: 200px;",
                    ),
                    SMALL(
                        f"REF: {variant.reference_number or 'N/A'}",
                        Class="text-muted font-monospace d-block small",
                    ),
                    Class="flex-grow-1",
                ),
                SPAN(status_text, Class=f"badge bg-{status_color} small"),
                Class="d-flex align-items-center mb-3",
            ),
            # Attributes & SKU
            DIV(
                SMALL(
                    f"SKU: {variant.sku}",
                    Class="text-muted d-block mb-2 font-monospace",
                ),
                DIV(*attributes, Class="d-flex flex-wrap"),
                Class="mb-3",
            ),
            # Logistics Grid (Price & Stock)
            DIV(
                DIV(
                    SMALL(
                        "Pricing",
                        Class="text-uppercase text-muted fw-bold d-block mb-1",
                        style="font-size: 10px;",
                    ),
                    price_display,
                    Class="col-6 border-end",
                ),
                DIV(
                    SMALL(
                        "Stock Level",
                        Class="text-uppercase text-muted fw-bold d-block mb-1",
                        style="font-size: 10px;",
                    ),
                    H6(str(variant.stock), Class=f"mb-0 text-{stock_color} fs-5"),
                    Class="col-6 ps-3",
                ),
                Class="row mb-4 bg-light p-2 rounded g-0",
            ),
            # Admin Actions
            DIV(
                A(
                    I(Class="bi bi-pencil-square"),
                    " Edit",
                    href=reverse(
                        "product:admin-productvariant-edit", kwargs={"product_id": variant.id}
                    ),
                    Class="btn btn-sm btn-outline-primary flex-fill me-2",
                ),
                BUTTON(
                    I("delete", Class="bi bi-trash"),
                    Class="btn btn-sm btn-outline-danger",
                    hx_get=reverse(
                        "product:admin-productvariant-delete", kwargs={"product_id": variant.id}
                    ),
                    hx_confirm=f"Delete variant {variant.sku}?",
                    hx_target=f"#variant-{variant.id}",
                    hx_swap="outerHTML",
                ),
                Class="d-flex border-top pt-3",
            ),
            Class="card-body",
        ),
        Id=f"variant-{variant.id}",
        Class="card shadow-sm border-0 h-100 col-md-4",
        style="max-width: 350px;",
    )
    return Frag({'variant',product_variant_card})


def AdminProductImageDetailCard() -> Frag:
    """Renders a gallery-style card for managing product images."""
    def product_image_card(**dvars):
        product_image = dvars.get('product_image')
        if not product_image:
            return DIV("No product image data available.", Class="alert alert-warning p-3")

        is_main = getattr(product_image, "is_main", False)
        border_class = "border-primary border-2" if is_main else "border-light"
        return DIV(
        DIV(
            # Image Preview
            DIV(
                IMG(
                    src=product_image.image.url,
                    Class="img-fluid rounded mb-2",
                    style="height: 160px; width: 100%; object-fit: cover;",
                ),
                (
                    SPAN(
                        "Main Image",
                        Class="badge bg-primary position-absolute top-0 end-0 m-2",
                    )
                    if is_main
                    else ""
                ),
                Class="position-relative",
            ),
            # Metadata
            SMALL(
                f"Alt: {product_image.alt_text or 'No alt text'}",
                Class="text-muted d-block text-truncate mb-2",
            ),
            # Actions
            DIV(
                (
                    BUTTON(
                        I(Class="bi bi-star-fill"),
                        " Set Main",
                        Class="btn btn-xs btn-outline-primary me-2",
                        hx_post=f"/admin/image/set-main/{product_image.id}/",
                    )
                    if not is_main
                    else ""
                ),
                BUTTON(
                    I(Class="bi bi-trash"),
                    Class="btn btn-xs btn-outline-danger ms-auto",
                    hx_delete=f"/admin/image/delete/{product_image.id}/",
                    hx_confirm="Delete this image?",
                ),
                Class="d-flex align-items-center mt-auto pt-2 border-top",
            ),
            Class="card-body d-flex flex-column",
        ),
        Class=f"card shadow-sm {border_class} h-100",
        style="width: 200px;",
    )
    return Frag({'product_image',product_image_card})


def AdminCategoryDetailCard() -> DIV:
    """Renders a management card for Category model."""
    def category_card(**dvar):
        category = dvar.get('category')
        if not category:
            return DIV("No category data available.", Class="alert alert-warning p-3")

        parent_text = (
            f"Parent: {category.parent.name}" if category.parent else "Top-level Category"
        )
        return DIV(
            DIV(
                (
                    IMG(
                        src=category.image.url,
                        Class="rounded me-3",
                        style="width: 50px; height: 50px; object-fit: cover;",
                    )
                    if category.image
                    else DIV(
                        I(Class="bi bi-folder2 text-primary fs-4"),
                        Class="bg-light rounded me-3 d-flex align-items-center justify-content-center",
                        style="width: 50px; height: 50px;",
                    )
                ),
                DIV(
                    H5(category.name, Class="mb-0 fw-bold fs-6"),
                    SMALL(parent_text, Class="text-muted d-block"),
                    Class="flex-grow-1",
                ),
                Class="d-flex align-items-center mb-3",
            ),
            P(
                category.description or "No description provided.",
                Class="text-secondary small mb-3 text-truncate-2",
            ),
            DIV(
                A(
                    "Edit",
                    href=f"/admin/category/edit/{category.id}/",
                    Class="btn btn-sm btn-link text-primary ps-0",
                ),
                BUTTON(
                    "Remove",
                    Class="btn btn-sm btn-link text-danger",
                    hx_delete=f"/admin/category/delete/{category.id}/",
                ),
                Class="d-flex border-top pt-2 mt-auto",
            ),
            Class="card-body d-flex flex-column",
        )
    return DIV(
        {'category',category_card},
        Class="card shadow-sm border-0 h-100",
        style="max-width: 300px;",
    )


def AdminReviewDetailCard() -> DIV:
    """Renders a card for moderation of ReviewModel."""
    def review_card(**dvars):
        review = dvars.get('review')
        if not review:
            return DIV("No review data available.", Class="alert alert-warning p-3")

        status_color = "success" if review.is_active else "danger"
        status_text = "Active" if review.is_active else "Hidden"

        # Generate stars
        stars = [I(Class="bi bi-star-fill text-warning me-1") for _ in range(review.rating)]
        stars += [I(Class="bi bi-star text-muted me-1") for _ in range(5 - review.rating)]
        return DIV(
            DIV(
                DIV(
                    H6(f"User: {review.user.username}", Class="mb-0 fw-bold small"),
                    SMALL(
                        f"Product: {review.product.sku}",
                        Class="text-muted d-block smaller",
                    ),
                    Class="flex-grow-1",
                ),
                SPAN(status_text, Class=f"badge bg-{status_color} smaller"),
                Class="d-flex justify-content-between align-items-start mb-2",
            ),
            DIV(*stars, Class="mb-2"),
            P(review.content, Class="small text-dark mb-3 border-start ps-2 py-1"),
            DIV(
                BUTTON(
                    "Toggle Visible",
                    Class="btn btn-xs btn-outline-secondary me-2",
                    hx_post=f"/admin/review/toggle/{review.id}/",
                ),
                A(
                    "View Replies",
                    href=f"/admin/review/{review.id}/replies/",
                    Class="btn btn-xs btn-link",
                ),
                Class="d-flex border-top pt-2 mt-auto",
            ),
            Class="card-body d-flex flex-column",
        )
    return DIV(
        {'review',review_card},
        Class="card shadow-sm border-0 h-100",
        style="max-width: 350px;",
    )


def AdminReplyDetailCard() -> DIV:
    """Renders a card for managing ReplyModel entries."""
    def reply_card(**dvars):
        reply = dvars.get('reply')
        if not reply:
            return DIV("No reply data available.", Class="alert alert-warning p-3")

        status_label = (
            SPAN("Visible", Class="badge bg-success")
            if reply.is_active
            else SPAN("Hidden", Class="badge bg-danger")
        )
        return DIV(
            DIV(
                SMALL("Reply to Review", Class="text-muted fw-bold"),
                status_label,
                Class="d-flex justify-content-between align-items-center mb-2",
            ),
            P(reply.reply_data, Class="small fst-italic mb-3"),
            DIV(
                BUTTON(
                    I(Class="bi bi-trash"),
                    Class="btn btn-sm btn-outline-danger",
                    hx_delete=f"/admin/reply/delete/{reply.id}/",
                ),
                BUTTON(
                    "Toggle",
                    Class="btn btn-sm btn-outline-warning ms-auto",
                    hx_post=f"/admin/reply/toggle/{reply.id}/",
                ),
                Class="d-flex border-top pt-2",
            ),
            Class="card-body",
        )
    return DIV(
        {'reply',reply_card},
        Class="card border-0 bg-light mb-2",
        style="max-width: 100%;",
    )


def AdminProductDetailCard() -> Frag:
    """
    Admin Detail Card following the Product model structure.
    Uses flat argument structure to avoid rendering/fetching errors.
    """
    # Create URLs using Django reverse
    def product_detail(**dvars):
        product=dvars.get('product')
        if not product:
            return DIV("No product data available.", Class="alert alert-warning")
        edit_url = reverse(
            "product:admin-product-detail", kwargs={"product_id": product.id}
        )  # Adjust name if needed
        has_vars = product.variants.all()
        if has_vars:
            variants = DIV(
                H5('Variants'),
                *[Frag(AdminProductVariantDetailCard(),data_pipeline={'variant':pv}) for pv in product.variants.all()],
                Class='row'
            )
        else:
            variants=Frag()
        return DIV(
        # Header Section
        DIV(
            H5(product.name, Class="mb-1 fw-bold"),
            SPAN("Featured", Class="badge bg-warning text-dark") if product.is_featured else "",
            Class="d-flex justify-content-between align-items-start mb-2"
        ),

        # Identity Row (Reference & SKU)
        DIV(
            SMALL(f"REF: {product.reference_number or 'N/A'}", Class="text-muted font-monospace me-3"),
            SMALL(f"SKU: {product.sku}", Class="text-muted font-monospace"),
            Class="mb-3 border-bottom pb-2"
        ),

        # Body (Description)
        P(product.short_description or "No short description provided.", Class="text-secondary small mb-3"),

        # Categories Summary (Flat iteration)
        DIV(
            *[SPAN(cat.name, Class="badge border text-dark me-1 small") for cat in product.categories.all()[:3]],
            Class="mb-4"
        ),

        # Action Footer
        DIV(
            A(
                I(Class="fas fa-edit me-1"), "Edit Product",
                href=edit_url,
                Class="btn btn-primary btn-sm flex-grow-1 me-2"
            ),
            Class="d-flex border-top pt-3",
            style="max-width: 300px;"

        ),
        variants if has_vars else '',

        Class="card shadow-sm p-3 mb-4 border-0",
        # style="max-width: 450px;"
    )
    return Frag({'product',product_detail})
