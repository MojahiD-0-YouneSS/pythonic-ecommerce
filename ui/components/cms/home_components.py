from django.urls import reverse
from probo import DIV, H1, H2, H3, P, SPAN, IMG, A
from probo.components import Frag
from probo.styles.frameworks.bs5.components import BS5Carousel
from ui.components.cms.banner import HeroBanner
def RenderHeroBanner(banners=None):
    """Renders the main Banner model at the top of the page."""
    if not banners:
        return DIV()
    carousel = BS5Carousel(
        Id="homeHeroCarousel",
        Class="carousel slide",
        
    )
    counter = 1
    for banner in banners:
        carousel.add_carousel_item(
            Frag(HeroBanner(), data_pipeline={'banner': banner}),
            Class="active" if counter == 1 else "",
            Id=f"slide-{counter}",
        )
        counter += 1
        carousel.add_carousel_indicators()
    return DIV(
        carousel,
        Class="w-full",)


def RenderFeaturedProducts(products):
    """Renders a grid of Product models."""
    if not products:
        return DIV()

    product_cards = [
        A(
            DIV(
                IMG(
                    src=p.get("image", ""),
                    Class="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-500",
                ),
                Class="aspect-w-1 aspect-h-1 w-full overflow-hidden bg-gray-200",
            ),
            DIV(
                H3(
                    p.get("name", "Product"),
                    Class="text-lg font-bold text-gray-900 mb-2",
                ),
                SPAN(
                    f"${p.get('price', '0.00')}",
                    Class="text-blue-600 font-extrabold text-xl",
                ),
                Class="p-6",
            ),
            href=f"/product/{p.get('id')}/",
            Class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1",
        )
        for p in products
    ]

    return DIV(
        H2(
            "Featured Collection",
            Class="text-4xl font-bold text-gray-900 text-center mb-12",
        ),
        DIV(
            *product_cards, Class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8"
        ),
        Class="max-w-7xl mx-auto py-20 px-4 sm:px-6 lg:px-8 w-full",
    )


def PosterCard():
    return DIV(
        DIV(
            # Background Image
            IMG(
                src={'poster.image'},
                Class="position-absolute top-0 start-0 w-100 h-100 object-fit-cover",
            ),
            # Gradient Overlay
            DIV(
                Class="position-absolute top-0 start-0 w-100 h-100",
                style="background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);",
            ),
            # Content
            DIV(
                H3({'poster.title'}, Class="text-white fw-bold mb-2"),
                P(
                    {'poster.description'},
                    Class="text-light mb-4",
                    style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;",
                ),
                A(
                    "Learn More",
                    href={'poster.link_url'},
                    Class="text-white fw-semibold text-decoration-underline transition",
                ),
                Class="position-relative p-4 w-100",
            ),
            Class="position-relative rounded-4 overflow-hidden shadow h-100 d-flex align-items-end",
            style="min-height: 300px;",
        ),
        # col-md-6 is the magic Bootstrap class that groups them in PAIRS (2 per row)
        Class="col-md-6 mb-4",
    )

def RenderPosters(posters):
    """Renders Poster models in pairs (side-by-side) using Bootstrap grid."""
    if not posters:
        return DIV()

    poster_cards = [
        DIV(PosterCard(), data_pipeline={'poster': p})
        for p in posters
    ]

    return DIV(
        DIV(*poster_cards, Class="row"),
        Class="container py-5 w-100",
    )


def RenderAboutUs(about_data):
    """Renders the AboutUs model in a split text/image pair layout."""
    if not about_data:
        return DIV()

    return DIV(
        DIV(
            # Text side (First half of the pair)
            DIV(
                H2(
                    {'about.title'},
                    Class="fw-bolder text-dark mb-4 display-6",
                ),
                P(
                    {'about.content'},
                    Class="lead text-secondary mb-4",
                ),
                A(
                    {'about.call_to_action_text'},
                    href={'about.call_to_action_url'},
                    Class="btn btn-primary btn-lg fw-bold px-4 rounded-3",
                ),
                Class="col-lg-6 pe-lg-5 mb-4 mb-lg-0",
            ),
            # Image side (Second half of the pair)
            DIV(
                IMG(
                    src={'about.image'},
                    Class="img-fluid w-100 h-auto object-fit-cover rounded-4 shadow-lg",
                ),
                Class="col-lg-6",
            ),
            Class="row align-items-center",
        ),
        data_pipeline={'about': about_data},
        Class="container py-5 my-5 border-top border-bottom",
    )


def TestimonyCard():
    return DIV(
        DIV(
            DIV(
                SPAN(
                    {'testimony.rating', lambda **dvars: "★" * dvars.get('testimony.rating', 5) + "☆" * (5 - dvars.get('testimony.rating', 5))},
                    Class="text-warning fs-5 tracking-widest mb-3 d-block",
                ),
                P(
                    {'testimony.feedback', lambda **dvars: f'"{dvars.get("testimony.feedback")}"'},
                    Class="text-secondary fst-italic mb-4",
                ),
            ),
            DIV(
                IMG(
                    src={'testimony.customer_image'},
                    Class="rounded-circle object-fit-cover bg-light border",
                    style="width: 50px; height: 50px;",
                ),
                SPAN(
                    {'testimony.customer_name'},
                    Class="fw-bold text-dark ms-3",
                ),
                Class="d-flex align-items-center border-top pt-3 mt-auto",
            ),
            Class="bg-white p-4 rounded-4 shadow-sm border h-100 d-flex flex-column justify-content-between",
        ),
        # col-md-6 forces these into perfect pairs!
        Class="col-md-6 mb-4",
    )

def RenderTestimonies(testimonies):
    """Renders Testimonies in pairs (2 per row) using Bootstrap grid."""
    if not testimonies:
        return DIV()

    from probo.components import Frag
    testimony_cards = [
        Frag(TestimonyCard(), data_pipeline={'testimony': t})
        for t in testimonies
    ]

    return DIV(
        DIV(
            H2(
                "What Our Customers Say",
                Class="fw-bold text-center mb-5",
            ),
            DIV(*testimony_cards, Class="row"),
        ),
        Class="container py-5",
    )
