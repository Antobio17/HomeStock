# HomeStock

The HomeStock application aims to make everyday problems easier, such as organising the household food supply. 
You will be able to manage the products in your fridge, preparations, shopping list, follow up of macros, etc.

## Architecture

Hexagonal architecture will be used for the development of this Python application.

```
HomeStock/
├── src/
│   ├── context/
│   │   ├── aggregate/
│   │   │   ├── application/
│   │   │   │   ├── query/
│   │   │   │   └── command/
│   │   │   ├── domain/
│   │   │   │   ├── service/
│   │   │   │   ├── model/
│   │   │   │   ├── event/
│   │   │   │   ├── exception/
│   │   │   │   └── query_model/
│   │   │   ├── infrastructure/
│   │   │   │   ├── application/
│   │   │   │   │   ├── command_handlers.yaml/
│   │   │   │   │   └── query_handlers.yaml
│   │   │   │   ├── domain/
│   │   │   │   │   ├── model/
│   │   │   │   │   │   ├── {implementation}/
│   │   │   │   │   │   │   ├── migration/
│   │   │   │   │   │   │   └── persistence/
│   │   │   │   │   │   └── repositories.yaml
│   │   │   │   │   ├── service/
│   │   │   │   │   │   ├── {implementation}/
│   │   │   │   │   │   └── services.yaml
│   │   │   │   │   ├── query_model/
│   │   │   │   │   │   ├── {implementation}/
│   │   │   │   │   │   └── queries.yaml
│   │   │   │   │   ├── connection/
│   │   │   │   │   │   ├── {implementation}/
│   │   │   │   │   │   └── connections.yaml
│   │   │   │   ├── adapter/
│   │   │   │   │   ├── api/
│   │   │   │   │   ├── cli/
│   │   │   │   │   └── messaging/
│   │   │   │   └── cli/
│   │   │   ├── __init__.py
│   │   │   ├── app.py
│   │   │   ├── manage.py
│   │   │   └── oauth.py
├── tests/
│   ├── context/
│   │   ├── aggregate/
│   │   │   ├── application/
│   │   │   │   ├── command/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   ├── domain/
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   └── __init__.py
├── LICENSE
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```


## Useful Links

- https://github.com/Iazzetta/hexagonal-fastapi-sentry-sqlalchemy/tree/main
- https://blog.szymonmiks.pl/p/domain-model-with-sqlalchemy/
- https://www.googleapis.com/oauth2/v1/certs


## Useful command

Start Flask App:
```shell
python src/manage.py
```

Run tests:
```shell
python -m unittest discover -s tests -p "test*.py" -v
```