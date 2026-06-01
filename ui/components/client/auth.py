from probo import DIV, H2, P, FORM, LABEL, INPUT, BUTTON, A, SPAN
from ui.components.crf_token import CsrfToken

def SignupForm():
    """Renders a sleek, two-column responsive Signup card."""
    return DIV(
        DIV(
            DIV(
                DIV(
                    # Header
                    H2(
                        "Create an Account",
                        Class="fw-bolder mb-2 text-center text-dark",
                    ),
                    P(
                        "Join us to start shopping premium items.",
                        Class="text-muted text-center mb-4",
                    ),
                    # The Form
                    FORM(
                        DIV(
                            CsrfToken(),
                            Class="mb-3",
                        ),
                        # First & Last Name side-by-side using a nested row
                        DIV(
                            DIV(
                                LABEL(
                                    "First Name",
                                    Class="form-label fw-semibold text-secondary",
                                    **{"for": "first_name"}
                                ),
                                INPUT(
                                    Type="text",
                                    Id="first_name",
                                    name="first_name",
                                    Class="form-control form-control-lg bg-light border-0",
                                    required=True,
                                ),
                                Class="col-sm-6 mb-3 mb-sm-0",
                            ),
                            DIV(
                                LABEL(
                                    "Last Name",
                                    Class="form-label fw-semibold text-secondary",
                                    **{"for": "last_name"}
                                ),
                                INPUT(
                                    Type="text",
                                    Id="last_name",
                                    name="last_name",
                                    Class="form-control form-control-lg bg-light border-0",
                                    required=True,
                                ),
                                Class="col-sm-6",
                            ),
                            Class="row mb-3",
                        ),
                        DIV(
                            LABEL(
                                "Email Address",
                                Class="form-label fw-semibold text-secondary",
                                **{"for": "email"}
                            ),
                            INPUT(
                                Type="email",
                                Id="email",
                                name="email",
                                Class="form-control form-control-lg bg-light border-0",
                                placeholder="name@example.com",
                                required=True,
                            ),
                            Class="mb-3",
                        ),
                        DIV(
                            LABEL(
                                "Username Of Choice",
                                Class="form-label fw-semibold text-secondary",
                                **{"for": "email"}
                            ),
                            INPUT(
                                Type="text",
                                Id="username",
                                name="username",
                                Class="form-control form-control-lg bg-light border-0",
                                placeholder="human12388",
                                required=True,
                            ),
                            Class="mb-3",
                        ),
                        DIV(
                            LABEL(
                                "Password",
                                Class="form-label fw-semibold text-secondary",
                                **{"for": "password"}
                            ),
                            INPUT(
                                Type="password",
                                Id="password",
                                name="password",
                                Class="form-control form-control-lg bg-light border-0",
                                placeholder="••••••••",
                                required=True,
                            ),
                            Class="mb-4",
                        ),
                        BUTTON(
                            "Create Account",
                            Type="submit",
                            Class="btn btn-dark btn-lg w-100 mb-3 fw-bold shadow-sm",
                        ),
                        method="POST",
                        action="/client/auth/signup/",
                    ),
                    # Footer Link
                    DIV(
                        SPAN("Already have an account? ", Class="text-muted"),
                        A(
                            "Log in",
                            href="/client/auth/login/",
                            Class="text-decoration-none fw-bold text-dark",
                        ),
                        Class="text-center mt-3",
                    ),
                    Class="card-body p-sm-5 p-4",
                ),
                Class="card border-0 shadow-lg rounded-4",
            ),
            Class="col-12 col-md-8 col-lg-6",  # Slightly wider for the two-column name inputs
        ),
        Class="row justify-content-center align-items-center min-vh-100 bg-gray-50 py-5 m-0",
    )

def LoginForm():
    """Renders a sleek, centered Login card."""
    return DIV(
        DIV(
            DIV(
                DIV(
                    # Header
                    H2("Welcome Back", Class="fw-bolder mb-2 text-center text-dark"),
                    P(
                        "Sign in to your account to continue",
                        Class="text-muted text-center mb-4",
                    ),
                    # The Form
                    FORM(
                        # Pass Django CSRF token directly into the form if needed
                        DIV(
                            CsrfToken(),
                            Class="mb-3",
                        ),
                        DIV(
                            LABEL(
                                "Email Address",
                                Class="form-label fw-semibold text-secondary",
                                **{"for": "email"}
                            ),
                            INPUT(
                                Type="email",
                                Id="email",
                                name="email",
                                Class="form-control form-control-lg bg-light border-0",
                                placeholder="name@example.com",
                                required=True,
                            ),
                            Class="mb-3",
                        ),
                        DIV(
                            DIV(
                                LABEL(
                                    "Password",
                                    Class="form-label fw-semibold text-secondary",
                                    **{"for": "password"}
                                ),
                                A(
                                    "Forgot password?",
                                    href="/auth/reset/",
                                    Class="text-decoration-none small text-muted",
                                ),
                                Class="d-flex justify-content-between",
                            ),
                            INPUT(
                                Type="password",
                                Id="password",
                                name="password",
                                Class="form-control form-control-lg bg-light border-0",
                                placeholder="••••••••",
                                required=True,
                            ),
                            Class="mb-4",
                        ),
                        BUTTON(
                            "Sign In",
                            Type="submit",
                            Class="btn btn-dark btn-lg w-100 mb-3 fw-bold shadow-sm",
                        ),
                        method="POST",
                        action="/client/auth/login/",
                    ),
                    # Footer Link
                    DIV(
                        SPAN("Don't have an account? ", Class="text-muted"),
                        A(
                            "Sign up here",
                            href="/client/auth/signup/",
                            Class="text-decoration-none fw-bold text-dark",
                        ),
                        Class="text-center mt-3",
                    ),
                    Class="card-body p-sm-5 p-4",
                ),
                Class="card border-0 shadow-lg rounded-4",
            ),
            Class="col-12 col-md-8 col-lg-5",
        ),
        # min-vh-100 forces the row to be full screen height, align-items-center centers it vertically
        Class="row justify-content-center align-items-center min-vh-100 bg-gray-50 py-5 m-0",
    )
