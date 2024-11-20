# Caso de uso

## Implementación

- Lenguaje de la aplicación Python 3.13
- Crear los directorios necesarios para el desarrollo.
- Crear los archivos que sean necesarios y si ya existieran se modificar.
- Crear/modificar dentro de la carpeta src en el contexto y agregado que correspondan.
- Usar la información del archivo README.md
- Todos los parámetros de funciones, propiedades de dtos y entidades deberán estar tipados.

## Context

Necesito un caso de uso para la creación de productos. El identificador será un uuid.

La ruta donde se trabajará para este caso de uso será src/catalogue/product/

### Parámetros de entrada

- name (64 Caracteres)
- price (float)
- ingredientes (text) es un parámetro opcional
- calorias (int)

### Validaciones

Realizar comprobaciónes pertinentes para la validaciones del caso de uso. Estas validaciones en el caso de no complirlas se devolverán con una excepción.

- No puede exister un producto con el mismo nombre.

### Evento de salida

Crear un evento si el caso de uso se ha ejecutado con exito.
