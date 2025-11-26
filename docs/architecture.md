# Arquitectura tuki_admin

## Apps

### core
- Rol:
- Vistas principales: 
-- index

- Templates clave: 
-- base.html
-- index.html
-- navbar.html

- Otros componentes:

### user
- Rol: 
-- user login control

- Modelos:
-- no models created yet

- URLs:
    app_name = 'user'

    urlpatterns = [
        path('login/', views.user_login, name='login'),
        path('signup/', views.user_signup, name='signup'),
        path('logout/', views.user_logout, name='logout'),
    ]

- Templates:
-- user_login.html
-- user_signup.html

### CUSTOMER
- Rol:
-- Representa a la persona/empresa dueña del vehículo.

- Modelos:
    Customer (Model)
        customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        customer_name = models.CharField(max_length=100)
        customer_phone = models.CharField(max_length=20)
        customer_email = models.EmailField(blank=True, null=True)
        customer_address = models.CharField(max_length=100, blank=True, null=True)

- Relaciones:
-- 1 Customer -> N Vehicles

- Vistas / URLs importantes:
-- all/

### VEHICLEMODEL
- Rol:
-- Representa el tipo de vehiculo, no el auto fisico

- Modelos:
-- VehicleModel (Model)
    vehiclemodel_id
    vehiclemodel_brand
    vehiclemodel_name
    vehiclemodel_version
    vehiclemodel_production

- Relaciones:
-- 1 VehicleModel -> N Vehicles
    

### vehiculos (apps.vehiculos)
- Rol:
Representa el auto específico que entra al taller.

- Modelos:
-- Vehicle (Model)
    vehicle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_customer (FK -> Customer)
    vehicle_model = (FK -> VehicleModel)
    vehicle_plate
    vehicle_color
    vehicle_details

- Relaciones:
-- N Vehicles -> 1 Customer
-- N Vehicles -> 1 VehicleModel
-- N Vehicles -> N Products

- Vistas / URLs:
-- Views
        add
        edit
        delete
        all
        vehicle
-- URLs
        all/
        add/
        uuid:vehicleid/
        uuid:vehicleid/delete
        uuid:vehicleid/edit

- Templates:
-- add
-- all
-- delete
-- edit
-- vehicle

### product
- Rol:
-- product app control
-- full control of products and business related information (prices, stock, supliers)

- Modelos:
    Product Model
        product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        product_name = models.CharField(max_length=100)
        product_description = models.TextField(blank=True)
        product_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
        product_supplier = models.CharField(max_length=100, choices=TYPE_SUPPLIERS)
        product_price = models.DecimalField(max_digits=10, decimal_places=0)
        product_currency = models.CharField(max_length=3, default='ARS')
        product_discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
        product_stock = models.IntegerField(default=0)
        product_sku = models.CharField(
            max_length=10, 
            null=True,
            blank=True,
            )
        product_is_active = models.BooleanField(default=True)
        product_related_products = models.ManyToManyField('self', blank=True)

- Relaciones:
-- accesorios o productos del mismo modelo de auto

- Vistas / URLs:
-- views
    all
    add
-- URLs
    add/
    all/

- Templates:
-- add
-- all
-- product 

### WORKORDER
-WorkOrder (un trabajo hecho a un vehículo en una fecha):
    id
    vehicle (FK → Vehicle)
    customer (FK → Customer) – redundante pero práctico.
    date
    mileage
    notes
    status (abierto, cerrado, presupuestado…)
    total_amount (opcional, lo podés calcular).

### WORKORDERITEM
-WorkOrderItem (línea de producto en un trabajo)
-Une trabajos con productos y permite contabilidad real:
    id
    work_order (FK → WorkOrder)
    product (FK → Product)
    quantity
    unit_price
    discount
    total_line (o lo calculas on the fly)

-Relaciones:
--1 WorkOrder → N WorkOrderItem
--1 Product → N WorkOrderItem
--A través de esto podés responder:
    Qué productos se usaron en un vehículo.
    Cuántas unidades de un producto se vendieron en un período.
    Historial de trabajos de un auto.

## Modelo de datos (relaciones)
- Customer 1 ─── N Vehicle
- Vehicle N ─── 1 (opcional) VehicleModel
- Vehicle 1 ─── N WorkOrder
- WorkOrder 1 ─── N WorkOrderItem
- Product 1 ─── N WorkOrderItem

(compatibilidad futura)
- VehicleModel N ─── N Product (productos compatibles)