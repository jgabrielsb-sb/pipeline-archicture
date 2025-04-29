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



# 📜 Design by Contract

This project follows a **Design by Contract** philosophy to ensure robust collaboration between components.

In this architecture:

- **Pipelines** expect that the **Tasks** they orchestrate correctly implement the task interface (providing task definitions and execution order).
- **Tasks** expect that the **business operation classes** they receive correctly implement the required **contract**, specifically a `run(input_data)` method.
- **Business logic classes** (located in the `operations/` folder) must fulfill this contract, providing reliable input/output behavior without breaking the expected data flow.

✅ **Contracts are not enforced by strict inheritance**, but by respecting **clear expectations** (interfaces by behavior, not necessarily abstract classes).

✅ **Tasks validate input data and output data** before and after invoking the `run()` method, ensuring that all parties respect the agreed-upon data formats and types.




## 🔥 Why Design by Contract?

| Principle | Application in this Project |
|:----------|:-----------------------------|
| **Clear Expectations** | Each layer defines *what* it expects from the others, minimizing surprises. |
| **Robustness** | If a component misbehaves (wrong type, wrong output), validation catches it immediately. |
| **Loose Coupling** | Business logic classes can change freely as long as they respect the contract, without breaking the pipeline or tasks. |
| **Testability** | Each component can be unit-tested independently, knowing exactly what is expected. |





# 🧪 Testing Strategy

This project applies a **layered testing philosophy** to enforce robustness in the core infrastructure while maintaining flexibility for business logic components.

---

## 📚 Testing Rules by Component

| Component | Testing Requirement | Coverage Target |
|:----------|:---------------------|:----------------|
| **BasePipeline** (`base_pipeline.py`) | Must be fully unit tested independently | ✅ 100% |
| **BaseTask** (`base_task.py`) | Must be fully unit tested independently | ✅ 100% |
| **Tasks Layer** (`tasks/`) | Should have light integration testing if necessary | ➡️ No strict 100% coverage required |
| **Operations Layer** (`operations/`) | Should be tested according to business criticality | ➡️ No strict 100% coverage required |

---

## 🎯 Core Testing Principles

✅ **Isolation**:  
- Pipeline tests **do not depend** on any Tasks or Operations.  
- Task tests **do not depend** on Pipelines or Operations.  
- Operations are tested **separately** if needed.

✅ **Design by Contract Enforcement**:  
- BaseTask tests must ensure that the input and output validation mechanisms correctly enforce the expected contract.

✅ **Minimal Mocking Needed**:  
- Pipeline and Task testing can use simple dummy objects or mocks to simulate task or operation behavior if required.

✅ **Clear Boundaries**:  
- Business rules (Operations) can change without impacting the stability of the Pipeline and Task core.



# 🚀 Example

- When testing `BasePipeline`, you can create **dummy tasks** that just pass data along.
- When testing `BaseTask`, you can create **dummy operation classes** that only return fixed outputs.

✅ This ensures **pure unit tests**, **minimal dependencies**, and **fast, reliable test runs**.



# 📜 Summary

This testing strategy ensures:

- The **core infrastructure remains stable, safe, and trustworthy**.
- The **business logic remains flexible and evolvable** without burdening the core with instability.
- The project remains **highly maintainable** and **scalable** over time.

✅ **100% tested where necessary**, ✅ **pragmatically tested where flexibility is needed**.



# 🚦 Contribution and Extension Rules

This project is designed with a clear separation of responsibilities between the core execution system (Pipeline and Task layers) and the business logic (Operations layer).

To maintain the system's integrity and stability:

✅ **Users and contributors must NOT modify:**
- The `BasePipeline` class (located in `base_pipeline.py`).
- The `BaseTask` class (located in `base_task.py`).
- Existing task definitions (inside the `tasks/` folder).

These components define the stable foundation of the system and are **critical for maintaining reliability and testability**.

---

✅ **To extend the system properly:**

- If a new type of operation is needed (e.g., a new data extraction, transformation, or validation process):
  - ➔ **Create a new Operation class** in the `operations/` folder.
  - ➔ The new class must implement a `run(input_data)` method, respecting the contract expected by Tasks.

- If a fundamentally different kind of Task behavior is needed:
  - ➔ **Create a new Task class** inside the `tasks/` folder.
  - ➔ The new Task must inherit from `BaseTask` and respect the existing execution interface (input validation, execution, output validation).

---

✅ **In short:**

| Goal | Correct Action |
|:----|:---------------|
| Add new business logic | ➔ Create a new class in `operations/`. |
| Add new task type | ➔ Create a new class in `tasks/`. |
| Modify how tasks are orchestrated | ➔ **Not allowed** — `BasePipeline` must remain stable. |
| Modify how tasks handle execution/validation | ➔ **Not allowed** — `BaseTask` must remain stable. |
| Modify existing tasks | ➔ **Not allowed** — create a new task if necessary. |

---

# 🎯 Philosophy

The Pipeline and Task structures form the **stable execution engine**.  
The Operations layer provides the **flexible, evolving business logic**.

This separation ensures:
- **Maintainability**: Changes in business rules do not break the system foundation.
- **Extensibility**: New operations and tasks can be added cleanly.
- **Robustness**: The core system remains reliable and easy to test.

✅ By following these guidelines, we ensure that the system remains **clean, modular, and professionally maintainable**.

---







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
<a href="https://github.com/jgabrielsb-sb/pipeline-archicture/actions">
    <img src="https://github.com/jgabrielsb-sb/pipeline-archicture/actions/workflows/ci.yml/badge.svg" alt="Build Status">
</a>

<!-- Code coverage badge (optional, requires Codecov setup) -->
<a href="https://codecov.io/gh/jgabrielsb-sb/pipeline-archicture">
  <img src="https://codecov.io/gh/jgabrielsb-sb/pipeline-archicture/branch/main/graph/badge.svg" alt="Coverage">
</a>

<!-- Python version badge -->
<img src="https://img.shields.io/badge/Python-3.11%2B-blue" alt="Python Version">

</div>

---



