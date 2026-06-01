from django.urls import reverse
from probo import DIV, H1, P, A, IMG

def HeroBanner(title=None, subtitle=None, image_url=None):

    title= title or "New Arrivals"
    subtitle= subtitle or "Built with Probo UI & Python" 
    image_url= image_url or "/static/images/img/hero4.png"

    return DIV(
        DIV(
            DIV(
                H1(title, Class="display-4 fw-bolder text-white"),
                P(subtitle, Class="lead fw-normal text-white-50 mb-4"),
                A(
                    "Shop Now",
                    href=reverse("product:product-catalog"),
                    Class="btn btn-light btn-lg px-4 me-sm-3",
                ),
                Class="text-center text-md-start",
            ),
            Class="container px-4 px-lg-5 my-5",
        ),
        Class="bg-dark py-5",
        # Using inline styles for the background image, perfectly valid in Probo UI
        style=f"background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{image_url}'); background-size: cover; background-position: center;",
    )