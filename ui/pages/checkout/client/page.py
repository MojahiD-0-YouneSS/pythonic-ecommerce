from probo import DIV, TEXT, FORM, INPUT, BUTTON


def CheckoutPage(cart_summary):
    """
    Renders the secure checkout flow.
    Left: Shipping/Payment FORM
    Right: Order Summary
    """
    return DIV(
        class_name="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8 flex flex-col lg:flex-row gap-12",
        children=[
            # Left Column: HTMX Checkout FORM
            DIV(
                class_name="w-full lg:w-2/3 bg-white p-8 rounded-2xl shadow-sm border border-gray-100",
                children=[
                    TEXT(
                        "Checkout",
                        as_="h2",
                        class_name="TEXT-3xl font-bold TEXT-gray-900 mb-8",
                    ),
                    FORM(
                        hx_post="/api/checkout/process_order/",
                        hx_target="body",  # Redirects or swaps entire body to success page on completion
                        class_name="space-y-6",
                        children=[
                            TEXT(
                                "Shipping InFORMation",
                                as_="h3",
                                class_name="TEXT-xl font-semibold border-b pb-2",
                            ),
                            DIV(
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                                children=[
                                    INPUT(
                                        name="first_name",
                                        label="First Name",
                                        required=True,
                                        class_name="w-full",
                                    ),
                                    INPUT(
                                        name="last_name",
                                        label="Last Name",
                                        required=True,
                                        class_name="w-full",
                                    ),
                                    INPUT(
                                        name="address",
                                        label="Street Address",
                                        required=True,
                                        class_name="w-full md:col-span-2",
                                    ),
                                    INPUT(
                                        name="city",
                                        label="City",
                                        required=True,
                                        class_name="w-full",
                                    ),
                                    INPUT(
                                        name="zip_code",
                                        label="ZIP Code",
                                        required=True,
                                        class_name="w-full",
                                    ),
                                ],
                            ),
                            BUTTON(
                                "Complete Order",
                                type_="submit",
                                class_name="w-full bg-green-600 TEXT-white TEXT-lg font-bold py-4 rounded-xl hover:bg-green-700 transition mt-8 shadow-lg",
                            ),
                        ],
                    ),
                ],
            ),
            # Right Column: Cart Summary (Read-Only)
            DIV(
                class_name="w-full lg:w-1/3 bg-gray-50 p-8 rounded-2xl shadow-inner border border-gray-200 h-fit",
                children=[
                    TEXT(
                        "Order Summary",
                        as_="h3",
                        class_name="TEXT-2xl font-bold TEXT-gray-900 mb-6",
                    ),
                    # Iterate through cart items
                    DIV(
                        class_name="space-y-4 mb-6 border-b pb-6 border-gray-200",
                        children=[
                            DIV(
                                class_name="flex justify-between TEXT-gray-700",
                                children=[
                                    TEXT(f"{item.get('quantity')}x {item.get('name')}"),
                                    TEXT(f"${item.get('price')}"),
                                ],
                            )
                            for item in cart_summary.get("items", [])
                        ],
                    ),
                    # Totals
                    DIV(
                        class_name="flex justify-between font-bold TEXT-xl TEXT-gray-900",
                        children=[
                            TEXT("Total"),
                            TEXT(f"${cart_summary.get('total_amount', '0.00')}"),
                        ],
                    ),
                ],
            ),
        ],
    )
