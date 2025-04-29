# 📚 Pipeline Execution Framework

This project is structured around two main core components: **Pipeline** and **Task**.

The architecture ensures a **clear separation of concerns**, **modularity**, and **extensibility**.

---

## 🛠️ Core Concepts

### 1. Pipeline

A **Pipeline** is an abstract execution orchestrator.  
It manages a **sequence of tasks**, executing each task **in order**, and passing the **output of the previous task** as the **input to the next one**.

Responsibilities of a Pipeline:
- Validate the sequence of tasks.
- Execute tasks sequentially.
- Manage the flow of data across tasks.

The Pipeline does not implement business logic itself — it only controls the execution flow.

---

### 2. Task

A **Task** represents a **unit of work** within a pipeline.  
However, a Task **does not implement specific business logic directly**.

Instead:
- It defines the **expected parameters**, **input data**, and **output data**.
- It **receives a class instance** during initialization, which implements the actual **business logic**.
- It is responsible for:
  - Validating input data.
  - Instantiating and running the provided class.
  - Validating output data.

Thus, the Task provides a **standardized execution interface**, while delegating specific behavior to an injected **business logic class**.

---

# 📜 Design by Contract

This project follows a **Design by Contract** philosophy to ensure robust collaboration between components.

In this architecture:

- **Pipelines** expect that the **Tasks** they orchestrate correctly implement the task interface (providing task definitions and execution order).
- **Tasks** expect that the **business operation classes** they receive correctly implement the required **contract**, specifically a `run(input_data)` method.
- **Business logic classes** (located in the `operations/` folder) must fulfill this contract, providing reliable input/output behavior without breaking the expected data flow.

✅ **Contracts are not enforced by strict inheritance**, but by respecting **clear expectations** (interfaces by behavior, not necessarily abstract classes).

✅ **Tasks validate input data and output data** before and after invoking the `run()` method, ensuring that all parties respect the agreed-upon data formats and types.

---

## 🔥 Why Design by Contract?

| Principle | Application in this Project |
|:----------|:-----------------------------|
| **Clear Expectations** | Each layer defines *what* it expects from the others, minimizing surprises. |
| **Robustness** | If a component misbehaves (wrong type, wrong output), validation catches it immediately. |
| **Loose Coupling** | Business logic classes can change freely as long as they respect the contract, without breaking the pipeline or tasks. |
| **Testability** | Each component can be unit-tested independently, knowing exactly what is expected. |

---

## 📚 Example of the Contract

A class provided to a Task must:

- Implement a method `run(input_data)`.
- Receive validated input data.
- Return output data matching the expected format.

## 🔥 Example Workflow

Suppose we have a task called `ExtractDataFromFileTask`:

- **Input:** a Pydantic model representing a document (e.g., `DocumentFile`).
- **Output:** a JSON-like dictionary containing extracted data.
- **Business Logic:** provided by a class (e.g., `FileExtractor`) passed during initialization.


# 🖼️ Architecture Diagram
<div align="center">

```text
+-------------------------------+
|            main.py            |
|     (Execution Entry Point)   |
+-------------------------------+
               |
               v
+-------------------------------+
|         BasePipeline          |
| (Pipeline Orchestration Logic)|
+-------------------------------+
               |
               v
+-------------------------------+
|           BaseTask            |
|    (Generic Task Interface)   |
+-------------------------------+
               |
               v
+-------------------------------+
|          Tasks Layer          |
| (Specific Task Definitions)   |
| (e.g., ExtractDataTask)        |
+-------------------------------+
               |
               v
+-------------------------------+
|       Operations Layer        |
|   (Business Logic Classes)    |
| (e.g., FileExtractor, Cleaner)|
+-------------------------------+
```
</div>

# 📚 Pipeline Execution Framework

<div align="center">

<!-- GitHub Actions CI badge -->
<a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions">
    <img src="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/ci.yml/badge.svg" alt="Build Status">
</a>

<!-- Code coverage badge (optional, requires Codecov setup) -->
<a href="https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO_NAME">
  <img src="https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO_NAME/branch/main/graph/badge.svg" alt="Coverage">
</a>

<!-- Python version badge -->
<img src="https://img.shields.io/badge/Python-3.11%2B-blue" alt="Python Version">

</div>

---



