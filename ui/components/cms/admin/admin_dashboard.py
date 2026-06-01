from probo import DIV, H3, H4, H5, H6, P, SPAN, I, A, CANVAS, SCRIPT, SMALL,SVG, G, POLYLINE, POLYGON, RECT, TEXT, LINE
from apps.global_context import get_global_context
import json




def SVGSalesLineChart(dates, sales, returns):
    """Generates a raw SVG Line Chart without JavaScript"""
    width, height = 600, 250
    pad_left, pad_right, pad_top, pad_bottom = 50, 20, 20, 30
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom
    
    max_val = max(max(sales), max(returns))
    max_val = max_val * 1.1 if max_val > 0 else 1  # Add 10% headroom
    
    def get_xy(index, val):
        x = pad_left + index * (plot_w / (len(dates) - 1))
        y = height - pad_bottom - (val / max_val) * plot_h
        return x, y

    # Generate coordinate strings
    sales_points = " ".join([f"{get_xy(i, v)[0]},{get_xy(i, v)[1]}" for i, v in enumerate(sales)])
    returns_points = " ".join([f"{get_xy(i, v)[0]},{get_xy(i, v)[1]}" for i, v in enumerate(returns)])
    
    # Polygon for the filled area under Sales
    sales_fill_points = f"{pad_left},{height - pad_bottom} {sales_points} {pad_left + plot_w},{height - pad_bottom}"

    # Build X-axis labels and grid lines
    grid_lines = []
    x_labels = []
    for i, date in enumerate(dates):
        x, _ = get_xy(i, 0)
        x_labels.append(TEXT(date, x=x, y=height-10,  style="font-size=12", fill="#6c757d", text_anchor="middle"))
        grid_lines.append(LINE(x1=x, y1=pad_top, x2=x, y2=height-pad_bottom, stroke="#e9ecef", stroke_width="1"))

    # Build Y-axis labels (3 steps)
    y_labels = []
    for step in range(4):
        val = (max_val / 3) * step
        y = height - pad_bottom - (val / max_val) * plot_h
        y_labels.append(TEXT(f"{int(val)}", x=pad_left-10, y=y+4,  style="font-size=12", fill="#6c757d", text_anchor="end"))
        grid_lines.append(LINE(x1=pad_left, y1=y, x2=width-pad_right, y2=y, stroke="#e9ecef", stroke_width="1"))

    return SVG(
        *grid_lines,
        POLYGON(points=sales_fill_points, fill="rgba(13, 110, 253, 0.1)"),
        POLYLINE(points=sales_points, fill="none", stroke="#0d6efd", stroke_width="3"),
        POLYLINE(points=returns_points, fill="none", stroke="#dc3545", stroke_width="2", stroke_dasharray="5,5"),
        *x_labels, *y_labels,
        # Legend
        G(
            RECT(x=width/2 - 70, y=5, width=12, height=12, fill="#0d6efd", rx="2"),
            TEXT("Sales", x=width/2 - 50, y=15,  style="font-size=12", fill="#333"),
            RECT(x=width/2 + 10, y=5, width=12, height=12, fill="#dc3545", rx="2"),
            TEXT("Returns", x=width/2 + 30, y=15,  style="font-size=12", fill="#333")
        ),
        viewBox=f"0 0 {width} {height}", width="100%", height="100%", xmlns="http://www.w3.org/2000/svg"
    )

def SVGAbandonmentBarChart(dates, cart_ab, checkout_ab):
    """Generates a raw SVG Grouped Bar Chart without JavaScript"""
    width, height = 500, 250
    pad_left, pad_right, pad_top, pad_bottom = 40, 20, 20, 30
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom
    
    max_val = 100 # Percentages always go up to 100
    group_w = plot_w / len(dates)
    bar_w = group_w * 0.35
    
    bars = []
    x_labels = []
    
    # Grid lines & Y-labels
    grid_items = []
    for step in [0, 25, 50, 75, 100]:
        y = height - pad_bottom - (step / max_val) * plot_h
        grid_items.append(TEXT(f"{step}%", x=pad_left-10, y=y+4,  style="font-size=12", fill="#6c757d", text_anchor="end"))
        grid_items.append(LINE(x1=pad_left, y1=y, x2=width-pad_right, y2=y, stroke="#e9ecef", stroke_width="1"))

    for i, date in enumerate(dates):
        group_x = pad_left + (i * group_w)
        
        # Cart Abandonment Bar
        c_h = (cart_ab[i] / max_val) * plot_h
        bars.append(RECT(x=group_x + (group_w * 0.1), y=height - pad_bottom - c_h, 
                         width=bar_w, height=c_h, fill="#ffc107", rx="2"))
        
        # Checkout Abandonment Bar
        chk_h = (checkout_ab[i] / max_val) * plot_h
        bars.append(RECT(x=group_x + (group_w * 0.1) + bar_w + 2, y=height - pad_bottom - chk_h, 
                         width=bar_w, height=chk_h, fill="#fd7e14", rx="2"))
        
        # X Axis Label
        x_labels.append(TEXT(date, x=group_x + (group_w / 2), y=height-10, style="font-size=12", fill="#6c757d", text_anchor="middle"))

    return SVG(
        *grid_items, *bars, *x_labels,
        # Legend
        G(
            RECT(x=width/2 - 100, y=0, width=12, height=12, fill="#ffc107", rx="2"),
            TEXT("Cart Aband.", x=width/2 - 80, y=10,  style="font-size=12", fill="#333"),
            RECT(x=width/2 + 5, y=0, width=12, height=12, fill="#fd7e14", rx="2"),
            TEXT("Checkout Aband.", x=width/2 + 25, y=10,  style="font-size=12", fill="#333")
        ),
        viewBox=f"0 0 {width} {height}", width="100%", height="100%", xmlns="http://www.w3.org/2000/svg"
    )

def ChartCard(title, svg_component):
    return DIV(
        H6(title, Class="text-muted text-uppercase fw-bold mb-4 smaller"),
        DIV(svg_component, style="position: relative; height:250px; width:100%"),
        Class="card shadow-sm border-0 p-4 h-100"
    )

def ReviewRow(review):
    """Single review item"""
    stars = [I(Class="bi bi-star-fill text-warning smaller") for _ in range(review['rating'])]
    stars += [I(Class="bi bi-star text-warning smaller") for _ in range(5 - review['rating'])]
    
    return DIV(
        DIV(
            DIV(*stars, Class="mb-1"),
            SPAN(review['time'], Class="text-muted smaller ms-auto"),
            Class="d-flex justify-content-between align-items-center"
        ),
        H6(review['customer'], SPAN(f" on {review['product']}", Class="text-muted fw-normal"), Class="mb-1 small fw-bold"),
        P(f'"{review["text"]}"', Class="text-muted smaller mb-0 fst-italic"),
        Class="border-bottom py-3 last-border-0"
    )

def HotProductRow(product):
    """Single hot product item"""
    trend_color = "success" if product['trend'] == "up" else "danger"
    trend_icon = "bi-arrow-up-right" if product['trend'] == "up" else "bi-arrow-down-right"

    return DIV(
        DIV(
            H6(product['name'], Class="mb-1 small fw-bold text-truncate", style="max-width: 200px;"),
            SMALL(f"{product['sales']} sold", Class="text-muted smaller"),
            Class="flex-grow-1"
        ),
        DIV(
            SPAN(product['revenue'], Class="d-block small fw-bold text-end"),
            SPAN(I(Class=f"bi {trend_icon} me-1"), product['pct'], Class=f"smaller text-{trend_color} fw-bold float-end"),
            Class="text-end"
        ),
        Class="d-flex align-items-center border-bottom py-3 last-border-0"
    )


def get_admin_dashboard(*args,**kwargs):
    
    mock_dashboard_data = {
    "charts": {
        "dates": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "sales": [120, 190, 300, 250, 200, 450, 390],
        "returns": [5, 10, 8, 15, 2, 20, 12],
        "cart_abandonment": [65, 59, 80, 81, 56, 55, 40], # Percentages
        "checkout_abandonment": [28, 48, 40, 19, 86, 27, 90] # Percentages
    },
    "recent_reviews": [
        {"id": 1, "customer": "Alex S.", "rating": 5, "product": "Linen Shirt", "text": "Perfect fit and amazing quality!", "time": "2 hours ago"},
        {"id": 2, "customer": "Sarah M.", "rating": 4, "product": "Leather Wallet", "text": "Good, but shipping took a while.", "time": "5 hours ago"},
        {"id": 3, "customer": "Mike T.", "rating": 5, "product": "Denim Jacket", "text": "Exactly what I was looking for.", "time": "Yesterday"},
        {"id": 4, "customer": "Elena G.", "rating": 2, "product": "Wool Beanie", "text": "Color doesn't match the picture.", "time": "Yesterday"},
        {"id": 5, "customer": "David K.", "rating": 5, "product": "Canvas Backpack", "text": "Very durable, highly recommend.", "time": "2 days ago"},
    ],
    "hot_products": [
        {"id": 101, "name": "Classic Linen Shirt", "sales": 342, "revenue": "$15,390", "trend": "up", "pct": "+12%"},
        {"id": 102, "name": "Minimalist Leather Wallet", "sales": 285, "revenue": "$8,550", "trend": "up", "pct": "+8%"},
        {"id": 103, "name": "Vintage Denim Jacket", "sales": 190, "revenue": "$17,100", "trend": "down", "pct": "-3%"},
        {"id": 104, "name": "Canvas Daily Backpack", "sales": 150, "revenue": "$12,000", "trend": "up", "pct": "+25%"},
    ]
}
    context = get_global_context()
    charts = context.get('charts', mock_dashboard_data['charts'])
    reviews = context.get('recent_reviews', mock_dashboard_data["recent_reviews"])
    hot_products = context.get('hot_products', mock_dashboard_data["hot_products"])

    # Pre-render the Python SVG charts
    sales_chart_svg = SVGSalesLineChart(charts['dates'], charts['sales'], charts['returns'])
    abandonment_chart_svg = SVGAbandonmentBarChart(charts['dates'], charts['cart_abandonment'], charts['checkout_abandonment'])

    return  DIV(
        # Header
     DIV(
            H3("Performance Overview", Class="fw-bold mb-1"),
            P("Store analytics rendered purely in Python. Zero JavaScript.", Class="text-muted"),
            Class="mb-5"
        ),

        # The Pure SVG Charts
        DIV(
            DIV(ChartCard("Sales vs Returns", sales_chart_svg), Class="col-lg-7 mb-4"),
            DIV(ChartCard("Abandonment Funnel", abandonment_chart_svg), Class="col-lg-5 mb-4"),
            Class="row"
        ),
        # Row 2: Data Lists
        DIV(
            # Hot Products Column
            DIV(
                DIV(
                    H6("HOT PRODUCTS", Class="text-muted text-uppercase fw-bold mb-3 smaller"),
                    DIV(
                        *[HotProductRow(p) for p in hot_products],
                    ),
                    Class="card shadow-sm border-0 p-4 h-100"
                ),
                Class="col-lg-6 mb-4"
            ),
            
            # Recent Reviews Column
            DIV(
                DIV(
                    H6("RECENT REVIEWS", Class="text-muted text-uppercase fw-bold mb-3 smaller"),
                    DIV(
                        *[ReviewRow(r) for r in reviews],
                    ),
                    DIV(
                        A("View All Reviews", href="/admin/reviews/", Class="btn btn-sm btn-outline-secondary w-100 mt-3"),
                    ),
                    Class="card shadow-sm border-0 p-4 h-100"
                ),
                Class="col-lg-6 mb-4"
            ),
            Class="row"
        ),
                
        Class="container-fluid py-4"
    )