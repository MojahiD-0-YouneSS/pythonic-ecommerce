# 🐍 Pythonic E-Commerce: Enterprise-Grade Django DDD Architecture

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/Celery-5.5-brightgreen?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-Cache%20%26%20Broker-red?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Production--Ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-black?logo=python&logoColor=white)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/Types-Mypy%20Strict-blue)](https://mypy-lang.org/)

A decoupled, Domain-Driven Design (DDD) e-commerce core built to demonstrate advanced software engineering and software architecture patterns in Python. Rather than following standard Django tutorial practices (tightly coupled views, string-based HTML templates, and fat models), this codebase utilizes custom core engines—[django-abstract](file:///c:/Users/pc/Desktop/Genneral%20Folders/django-abstract) and [probo-ui](file:///c:/Users/pc/Desktop/Genneral%20Folders/masstodon-ui/probo)—to achieve complete isolation of concerns, compile-time type safety for UI, and high-performance server-side state orchestration.

---

## 🏛️ Architectural Overview & Design Philosophy

The primary objective of this architecture is **uncompromised modularity**. In standard Django, views directly query the database, parse HTML strings, and mutate state, leading to a highly coupled codebase that is difficult to scale, test, or refactor. 

This platform completely decouples the **Persistence layer**, the **Business Domain layer**, and the **User Interface layer**:

```mermaid
graph TD
    %% User/Browser Interactions
    Browser[🌐 User Browser] -->|HTTP Request / HTMX Ajax| Nginx[🔀 Reverse Proxy / Traefik]
    Nginx -->|Route Request| DjangoWSGI[🚀 Gunicorn / Django WSGI]
    
    %% Middleware Processing
    subgraph Django Pipeline [Django Request & Middleware Pipeline]
        DjangoWSGI --> GlobalSession[1. GlobalSessionMiddleware<br>Injects session context]
        GlobalSession --> CsrfContext[2. CsrfContextMiddleware<br>Hydrates Probo UI global token]
        CsrfContext --> EntryMiddleware[3. EntryMiddleware<br>Hydrates Domain Master Entry]
    end

    %% Routing to Views
    EntryMiddleware -->|Hydrated request.django_abstract_entry| View[📋 Django Domain View]

    %% Domain DDD Layer
    subgraph Business Logic Layer [Domain-Driven Business Layer (django-abstract)]
        View -->|Injects context| Dependency[💉 App Dependency Container<br>Resolves Selectors & Creators]
        View -->|Executes mutating action| Service[🛠️ Model Service / Bare Service]
        Service -->|Validation checks| Validator[🔍 Service Validator<br>Asserts business rules & boundaries]
        Validator -->|Reads data| Selector[📈 Dynamic Selector<br>Retrieves Model objects]
        Validator -->|Mutates state| Creator[✏️ Dynamic Creator<br>Inserts/Updates records]
        Selector -->|ORM Queries| DB[(💾 PostgreSQL / SQLite)]
        Creator -->|ORM Mutate| DB
    end

    %% UI Rendering Layer
    subgraph Presentation Layer [Component-Driven Python UI (probo-ui)]
        View -->|Supplies domain dictionary| Page[📄 Probo Page Component]
        Page -->|Assembles| Component[🧩 UI Components & Cards]
        Component -->|SSDOM Manipulation| Element[🏷️ Python HTML Elements]
        Element -->|JIT styling compilation| CSS[🎨 Probo StyleManager]
        Element -->|Generates string| RawHTML[📝 Optimized HTML / HTMX DOM payload]
    end

    %% Response Delivery
    RawHTML -->|HttpResponse| Browser
    
    %% Background Work
    Service -->|Dispatches async event| RedisBroker[📬 Redis Queue / Broker]
    RedisBroker -->|Consume task| CeleryWorker[⚙️ Celery Workers]
    CeleryWorker -->|Mutate state| DB
```

---

## ⚡ Core Technical Features

### 1. Metaprogramming-Driven Dependency Injection (`django-abstract`)
To eliminate repetitive boilerplates for model queries (Selectors) and record insertions (Creators), the system uses a custom class decorator pattern. By decorating a model with `@creator_selector`, the system dynamically creates dedicated, isolated selector and creator classes at import time and registers them in a centralized domain container.

```python
# apps/product/models.py
from django_abstract.registry import creator_selector
from apps.product.dependencies import ProductAppDependecy

@creator_selector(dependency=ProductAppDependecy)
class ProductVariant(BaseModel):
    """Represents a specific variant of a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

At runtime, developers access these selector instances cleanly through the resolved dependency container without direct database importing:

```python
# apps/product/views/client_views/crud_views.py
class ProductCatalogView(View):
    _dependency = get_product_app_dependency()

    def get(self, request):
        # The selector is dynamically instantiated and bound via __getattr__ interception
        active_variants = self._dependency.select_product_variant.model_class.objects.filter(is_active=True)
        # ...
```

Under the hood, `BaseDependency` intercepts access using Python's `__getattr__` magic method, fetching the correct dynamic class from the `GLOBAL_REGISTRY` bucket corresponding to the app domain:

```python
# django_abstract/src/django_abstract/base/base_dependency.py
def __getattr__(self, item):
    if hasattr(self, 'selectors') and item in self.selectors:
        return self.selectors[item]()  # Instantiates the dynamic Selector subclass
    
    if hasattr(self, 'creators') and item in self.creators:
        return self.creators[item]()  # Instantiates the dynamic Creator subclass
    # ...
```

---

### 2. Service Layer Boundaries & Business Rules Enforcement
State mutations do not live in models or views. The system separates reads and writes:
*   **Selectors**: Perform pure, read-only queries (e.g. `get_by()`, `filter_by()`).
*   **Services & Validators**: Enforce strict mutation logic.

Every model service implements a nested `BaseServiceValidator` specifying minimum required fields, allowed schema fields, and reserved database transactions:

```python
# apps/cart/services/cart_service.py
@register_service()
class CartItemModelService(BaseModelService):
    model_dependency = CartAppDependency()
    model_slug = "cart_item"

    class CartItemServiceValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            # Strict validation constraints for DB operations
            self.MINIMUM_WRITE_FIELDS = ["cart", "product_variant", "quantity"]
            self.SERVICE_DOMAIN_FIELDS = ["session", "pk", "product_variant", "quantity"]
            
            self.VALID_FIELDS_PER_ACTION = {
                "add_item_to_cart": ["product_variant", "quantity", "session"],
                "remove_item_from_cart": ["pk"],
            }
            
            self.regester_method("add_item_to_cart", self.add_item_to_cart)
            self.regester_method("remove_item_from_cart", self.remove_item_from_cart)

        def add_item_to_cart(self):
            product_variant_id, quantity, session = self.get_method_args("add_item_to_cart")
            cart = self.dependency.select_cart.get_by(session=session)
            product = get_product_app_dependency().select_product_variant.get_by(id=product_variant_id)
            
            if product.stock < quantity:
                raise ServiceException("Insufficient stock available")
                
            cart_item, _ = self.dependency.create_cart_item.access_db.get_or_create(
                product_variant=product, cart=cart
            )
            cart_item.quantity += quantity
            cart_item.save()
```

---

### 3. Server-Side DOM (SSDOM) Rendering Engine (`probo-ui`)
Instead of string-based parsing (like Django Templates) or heavy JavaScript-centric Single-Page Application (SPA) client rendering (like React/Vue), the UI is built using **Probo UI**, a backend-first UI framework written in pure, type-safe Python. 

Rather than rendering plain strings directly, Probo UI constructs a **live object tree in memory** (SSDOM), allowing developers to manipulate node properties, inject scripts, and append dynamic nodes after layout definition but prior to serialization.

```python
# ui/pages/product/client/product_catalog.py
from ui.pages.base import get_client_base_template 
from probo import DIV, H1
from ui.components.product.client.product_catalog import ProductCatalog

class ProductCatalogPage:
    def __init__(self, products=None, categories=None):
        self.template = get_client_base_template()
        self.products = products or []
        self.categories = categories or []
        self._title = "Store Catalog"

    def render(self):
        # 1. SSDOM Search: Find TITLE tag and rewrite inner HTML dynamically
        base_title = self.template.html_doc.find(lambda n: n.tag == 'TITLE')
        if base_title:
            base_title.inner_html(self._title)

        # 2. Compile component instance
        product_list = ProductCatalog(self.products, self.categories)

        # 3. SSDOM Search: Find matching node in the template tree and inject the component
        root_container = self.template.html_doc.find(
            lambda n: n.attr_manager.get_attr("data_ssdom_id") == 'root-container'
        )
        if root_container:
            root_container.add(DIV(product_list))

        # 4. Serialize the final SSDOM tree into standard, minified HTML
        return self.template.render()
```

### 4. Zero-JavaScript SPA Experience (HTMX Integration)
Interactive features—like updating cart quantities, checking out, and searching filters—harness native **HTMX** integration within the Python UI components. Out-of-band (OOB) swaps are returned natively from views to update disparate sections of the page layout asynchronously (e.g. updating the cart subtotal inside the header nav while modifying quantity in the cart table list).

```python
# ui/components/product/client/product_catalog.py
def ProductsSection(products, hx_oob=False):
    return DIV(
        DIV(
            *[DIV(ProductCard(p), Class="col-md-4 mb-4") for p in products],
            Class="row"
        ),
        Class="col-md-9",
        Id="product-grid-container",
        hx_swap_oob="true" if hx_oob else False,  # Declares an OOB swap to HTMX
    )
```

---

## 🛠️ Technology Stack & Dependencies

*   **Runtime Core**: Python 3.12, Django 5.0
*   **Task Scheduling**: Celery 5.5 (Distributed asynchronous event/state tasks)
*   **Caching & Broker**: Redis (Used as a Django cache store and Celery AMQP broker)
*   **Database Engine**: PostgreSQL (Production) / SQLite (Local development)
*   **Code Verification**: 
    *   **Mypy**: Typed static checking with `django-stubs` plugin
    *   **Ruff**: Ultrafast Python linter and formatter running on 70+ strict rule-sets
    *   **Pytest & Coverage**: Automated testing suite with DB reusability

---

## 📦 Project Structure

```bash
pythonic-ecommerce/
│
├── apps/                        # Django domain applications
│   ├── cart/                    # Cart business domain and state services
│   ├── checkout/                # Checkout domain and Stripe/payment systems
│   ├── client/                  # Client authentication, user links, middlewares
│   ├── cms/                     # Admin dashboard controllers and layout managers
│   ├── order/                   # Order placement, receipt generation, and archiving
│   └── product/                 # Catalog search, pricing engine, variant mapping
│
├── pythonic_ecommerce/          # Django configuration root
│   ├── settings.py              # Main configuration file (middlewares, database, logging)
│   ├── celery_app.py            # Celery broker initialization and configuration
│   └── urls.py                  # Global route dispatcher
│
├── ui/                          # Frontend layout architecture (probo-ui)
│   ├── components/              # Reusable UI elements (cards, headers, filters)
│   └── pages/                   # Main page layouts (storefront, detail pages)
│
├── devops/                      # Infrastructure orchestrations
│   ├── compose/                 # Docker Compose build configurations
│   │   ├── local/               # Django, Postgres, Redis, Celery, Flower for local
│   │   └── production/          # Traefik, Django, Postgres, Redis, Celery for prod
│   └── .envs/                   # Environment config files
│
├── requirements/                # Strict dependency files divided by environment
├── manage.py                    # Django CLI manager
├── pyproject.toml               # Mypy, Ruff, Pytest configurations
└── README.md                    # This developer handbook
```

---

## 🚀 Getting Started

This repository provides a production-ready containerized environment. No local Python or Database installation is required to boot the application.

### 1. Prerequisite Checks
Ensure you have Docker and Docker Compose (v2+) installed:
```bash
docker --version
docker compose version
```

### 2. Startup Containers
Spin up the backend app, database service, redis cache, celery workers, and Celery Flower monitoring dashboard:
```bash
docker compose -f docker-compose.local.yml up --build -d
```

### 3. Initialize Database
Execute migrations and create your default superuser account:
```bash
docker compose -f docker-compose.local.yml exec django python manage.py migrate
docker compose -f docker-compose.local.yml exec django python manage.py createsuperuser
```

### 4. Access Entry Points
*   **Web Storefront**: [http://localhost:8000](http://localhost:8000)
*   **Flower Dashboard**: [http://localhost:5555](http://localhost:5555) (Celery task monitoring)

---

## 🧪 Testing & Verification

Automated testing is configured via Pytest. Run the test suite within the running application container:

```bash
docker compose -f docker-compose.local.yml exec django pytest
```

To run coverage reports:
```bash
docker compose -f docker-compose.local.yml exec django coverage run -m pytest
docker compose -f docker-compose.local.yml exec django coverage report -m
```