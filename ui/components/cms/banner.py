from django.urls import reverse
from probo import DIV, H1, P, A, IMG

def HeroBanner():
    return DIV(
        DIV(
            DIV(
                H1(
                    {'banner.title', lambda **dvars: dvars.get('banner.title') or "New Arrivals"},
                    Class="display-4 fw-bolder text-white"
                ),
                P(
                    {'banner.subtitle', lambda **dvars: dvars.get('banner.subtitle') or "Built with Probo UI & Python"},
                    Class="lead fw-normal text-white-50 mb-4"
                ),
                A(
                    "Shop Now",
                    href={'banner.id', lambda **dvars: reverse("product:product-catalog")},
                    Class="btn btn-light btn-lg px-4 me-sm-3",
                ),
                Class="text-center text-md-start",
            ),
            Class="container px-4 px-lg-5 my-5",
        ),
        Class="bg-dark py-5",
        # Using inline styles for the background image, perfectly valid in Probo UI
        style={'banner.image', lambda **dvars: f"background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{dvars.get('banner.image') or '/static/images/img/hero4.png'}'); background-size: cover; background-position: center;"},
    )