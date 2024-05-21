# HomeStock

API para la gestión de del stock de nuestro hogar.

## Convención de código 💻

Este proyecto se desarrolla en Python y se van a definir algunas reglas y recomendaciones para la homegeneidad del mismo.

Siguiendo el documento PEP8 que establece una serie de pautas y recomendaciones para escribir código Python legible, consistente y mantenible definimos que:
- **Indentación:** La indentación en Python se basa en espacios, y usarán 4 espacios por nivel de indentación.
- **Nombres de variables y funciones:** Los nombres de variables y funciones deben ser descriptivos y utilizar minúsculas. Las palabras compuestas se deben separar por guiones bajos.
- **Comentarios:** Los comentarios deben ser claros y concisos, y se deben utilizar para explicar el código complejo o no obvio.
- **Importaciones:** Las importaciones deben estar organizadas y se deben utilizar declaraciones de importación from para evitar ambigüedades.
- **Cadenas de texto:** Se recomienda utilizar comillas simples para cadenas de texto a menos que se necesiten comillas dobles para caracteres especiales.
- **Operadores:** Los operadores deben estar espaciados adecuadamente y se deben usar paréntesis para aclarar la precedencia de operaciones.
- **Control de flujo:** Las declaraciones de control de flujo, como if, while y for, deben estar indentadas consistentemente y se deben usar bloques elif cuando sea apropiado.

Además añadiremos nuestras propias recomendaciones:
- No se hará uso de bloques else.
- Usaremos Se usarán clausulas de guarda para evitar indentaciones complejas de leer.

## Organización de directorios
La organización de directorios del proyecto será la siguiente:

```
proyecto/
├── README.md
├── LICENSE
├── src/
│   ├── application/
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── command.py
│   │   │   └── ...
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── command_handler.py
│   │   │   └── ...
│   │   ├── queries/
│   │   │   ├── __init__.py
│   │   │   ├── query.py
│   │   │   └── ...
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       ├── crear_pedido_use_case.py
│   │       └── ...
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── aggregate.py
│   │   │   └── ...
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── event.py
│   │   │   └── ...
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── value_object.py
│   │   │   └── ...
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── repository.py
│   │       └── ...
│   ├── infrastructure/
│   │   ├── databases/
│   │   │   ├── __init__.py
│   │   │   ├── sql_repository.py
│   │   │   └── ...
│   │   ├── event_sourcing/
│   │   │   ├── __init__.py
│   │   │   └── event_store.py
│   │   └── messaging/
│   │       ├── __init__.py
│   │       ├── rabbitmq_publisher.py
│   │       └── ...
│   └── interfaces/
│       ├── api/
│       │   ├── __init__.py
│       │   ├── crear_pedido_controller.py
│       │   └── ...
│       ├── dtos/
│       │   ├── __init__.py
│       │   ├── crear_pedido_dto.py
│       │   └── ...
│       └── http/
│           ├── __init__.py
│           └── main.py
└── tests/
    ├── application/
    │   ├── commands/
    │   │   └── test_crear_pedido.py
    │   ├── handlers/
    │   │   └── test_crear_pedido_handler.py
    │   └── use_cases/
    │       └── test_crear_pedido_use_case.py
    ├── domain/
    │   ├── entities/
    │   │   └── test_pedido.py
    │   ├── events/
    │   │   └── test_pedido_creado.py
    │   └── repositories/
    │       └── test_pedido_repository.py
    ├── infrastructure/
    │   ├── databases/
    │   │   └── test_sql_alchemy_repository.py
    │   └── event_sourcing/
    │       └── test_event_store.py
    └── interfaces/
        ├── api/
        │   └── test_crear_pedido_controller.py
        └── http/
            └── test_main.py
```
