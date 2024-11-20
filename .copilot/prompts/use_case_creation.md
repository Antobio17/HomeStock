# PROMPT: Generación de Caso de Uso

## Información Requerida
- Nombre del Caso de Uso: Creación de producto
- Contexto de Negocio: catalogue
- Entidad Principal: product
- Propiedades de la Entidad:
    - name (64 Caracteres)
    - price (float)
    - ingredientes (text) es un parámetro opcional
    - calorias (int)
- Validaciones Requeridas:
    - No puede existir un  producto en la base de datos con el mismo nombre.

## Estructura de Directorios
src/
└── {contexto}/
    └── {entidad}/
        ├── domain/
        │   ├── entities/
        │   │   └── {entidad}.py
        │   ├── events/
        │   ├── exceptions/
        │   │   └── create_{entidad}_exception.py
        │   ├── repositories/
        │   │   └── {entidad}_repository.py
        │   └── query_models/
        ├── application/
        │   ├── services/
        │   └── use_cases/
        │       └── create_{Entidad}_use_case.py
        └── infrastructure/
            └── domain/
            │   ├── repositories/
            │   ├── query_models/
            │   └── persistence/
            ├── web/
            └── cli/

## Comandos de Creación
```powershell
# Crear estructura de directorios
mkdir src\{contexto}\{entidad}
mkdir src\{contexto}\{entidad}\domain
mkdir src\{contexto}\{entidad}\application
mkdir src\{contexto}\{entidad}\infrastructure\persistence

# Crear archivos Python
ni src\{contexto}\{entidad}\domain\__init__.py
ni src\{contexto}\{entidad}\domain\{Entidad}.py
ni src\{contexto}\{entidad}\domain\{Entidad}Repository.py
ni src\{contexto}\{entidad}\application\__init__.py
ni src\{contexto}\{entidad}\application\Create{Entidad}UseCase.py
ni src\{contexto}\{entidad}\infrastructure\persistence\__init__.py
ni src\{contexto}\{entidad}\infrastructure\persistence\{Entidad}SQLRepository.py