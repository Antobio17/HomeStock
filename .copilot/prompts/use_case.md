# Use case: Update {aggregate}

## Implementation

- Application language: Python 3.13.
- Create/modify the necessary files within the `src` folder, adhering to the specified directory structure.  Do not create any files or directories not explicitly listed below.
- All function parameters, data properties, and entities shall be typed.
- Maintain the existing programming style of the project.  Pay close attention to naming conventions, code formatting, and the use of docstrings.
- Do not modify existing methods.  Create new methods as needed.

## Context

This use case updates an existing {aggregate}. The working path for this use case is `src/{context}/{aggregate}/`.

The properties that can be modified are:

- `price`
- `calories`
- `carbohydrates`
- `proteins`
- `fats`
- `sugar`

The `updated_at` field must be set to the current date and time.

### Validations

Implement the same validations as the {aggregate} creation use case.  This includes:

- Name length must not exceed 64 characters.
- All numeric fields (price, calories, carbohydrates, proteins, fats, sugar) must be greater than or equal to 0.

### Files involved (Create/Modify)

```
HomeStock/
├── src/
│   ├── context/
│   │   ├── {aggregate}/
│   │   │   ├── application/
│   │   │   │   ├── command/
│   │   │   │   │   ├── {action}_{aggregate}_command.py
│   │   │   │   │   └── {action}_{aggregate}_command_handler.py
│   │   │   ├── domain/
│   │   │   │   ├── model/
│   │   │   │   │   ├── {aggregate}_repository.py
│   │   │   │   │   └── {aggregate}.py
│   │   │   │   ├── event/
│   │   │   │   │   └── {aggregate}_{action_in_pass}.py
│   │   │   │   ├── exception/
│   │   │   │   │   └── {acttion}_{aggregate}_exception.py
│   │   │   ├── infrastructure/
│   │   │   │   ├── application/
│   │   │   │   │   └── command_handlers.yaml/
│   │   │   │   ├── domain/
│   │   │   │   │   ├── model/
│   │   │   │   │   │   ├── {implementation}/
│   │   │   │   │   │   │   ├── persistence/
│   │   │   │   │   │   │   │   └── model.py
│   │   │   │   │   │   │   └── {implementation}_{aggregate}_repository.py
│   │   │   │   │   │   └── repositories.yaml
│   │   │   │   └── adapter/
│   │   │   │       └── api/
│   │   │   │           ├── controller/
│   │   │   │           │   └── {action}_{aggregate}_controller.py
│   │   │   │           └── routing.yaml
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
│   │   │   └── __init__.py
│   └── __init__.py
```

### Mapping

- `{action}` = `update`
- `{action_in_pass}` = `updated`
- `{context}` = `catalogue`
- `{aggregate}` = `product`
- `{implementation}` = `sqlalchemy`

### Constraints

- Do not create any files or directories that are not specified in the file tree above.
- Do not modify methods that already exist.  Create new methods as needed.  Ensure new methods are clearly documented with docstrings, including type hints.
- Adhere to the project's existing coding style and conventions.  This includes naming conventions, code formatting, and the use of docstrings.  Pay particular attention to how exceptions are handled and raised in the existing codebase and replicate that pattern.
- Ensure that the use case is fully testable. Consider how the different components (command handler, repository, etc.) can be easily mocked or stubbed for testing purposes.  While test files are not being created in this prompt, the code should be written with testability in mind.