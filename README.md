# HomeStock

La aplicación HomeStock tiene como objetivo facilitar los problemas cotidianos como puede ser la organización de la alimentación de la casa. 
Podrás gestionar los productos de tu frigorifico, elaboraciones, lista de la compra, seguimiento de los macros, etc.

## Arquitectura

Se usará arquitectura hexagonal para el desarrollo de esta aplicación Python.

```
HomeStock/
├── src/
│   ├── context/
│   │   ├── aggregate/
│   │   │   ├── application/
│   │   │   │   ├── services/
│   │   │   │   └── use_cases/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   ├── events/
│   │   │   │   ├── exceptions/
│   │   │   │   ├── repositories/
│   │   │   │   └── query_models/
│   │   │   ├── infrastructure/
│   │   │   │   ├── domain/
│   │   │   │   │   ├── repositories/
│   │   │   │   │   ├── query_models/
│   │   │   │   │   └── persistence/
│   │   │   │   ├── web/
│   │   │   │   └── cli/
│   │   │   └── __init__.py
├── tests/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── __init__.py
├── requirements.txt
└── README.md
```
