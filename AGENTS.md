# Thoughtful Code Writing Guidelines

**Forget conventional "clean code" dogma.**

**Simplicity Over Abstraction**: Consider whether each abstraction genuinely simplifies the codebase. Ask yourself if a simpler approach would work just as well. While abstractions can be powerful, they add cognitive overhead that's only justified when they meaningfully reduce complexity elsewhere. Evaluate whether a straightforward implementation might be more maintainable than a clever pattern or framework that requires deeper understanding.

**Code Locality**: Think about how readers will understand your code. When related functionality is spread across multiple files, comprehension requires constant context-switching. Aim to organize code so that related behaviors stay close together, making it easier to reason about complete features. Consider whether splitting code into separate files actually improves clarity or merely follows convention without adding value.

**Meaningful Organization**: Arrange your code to tell a coherent story, with the most significant pieces appearing first. Ask how a new developer would read your code - would they quickly grasp its purpose and structure? High-level functions should provide a roadmap to understanding the module's purpose, with implementation details following naturally as the reader progresses through the file.

**Minimal Parameterization**: Question each parameter or configuration option you create. Is this value likely to change frequently? Is it used in multiple places? Will users genuinely need to adjust it? Resist the urge to make everything configurable - each parameter adds complexity and indirection. Consider whether hardcoding certain values might actually improve readability and maintainability.

**Linear Flow**: Examine whether your code follows a logical progression that's easy to mentally trace. Complex branching often makes code difficult to reason about. Consider if special case handling is truly necessary or if your main algorithm could be adapted to handle edge cases naturally. Aim for implementations where the primary path through the code is clear and intuitive.

**Flat Conditionals**: Analyze nested conditionals critically - they often indicate opportunities for simplification. Deep nesting makes it difficult to track the current state and conditions as you read. Consider alternative approaches like early returns, guard clauses, lookup tables, or state machines when faced with complex conditional logic. Flatter structures typically lead to more maintainable and testable code.

**Functional Approach**: Consider state management carefully in your design. Functions with clear inputs and outputs are easier to test and reason about, but classes may be appropriate when state needs to be maintained. Ask whether introducing a class adds value beyond organizing related functions, or if it's merely adding structure without purpose. Choose the approach that best communicates intent.

**Focused Error Handling**: Think deliberately about which errors deserve special handling. Not every exception warrants a try-except block - sometimes it's better to let errors propagate to a level where they can be meaningfully addressed. Consider whether your error handling actually improves the robustness of your code or just obscures problems that should be fixed directly.

**Purposeful Implementation**: Evaluate each feature against actual requirements rather than hypothetical future needs. Ask whether additional functionality truly serves the current purpose or adds unnecessary complexity. Build for the present with clean, modifiable code rather than attempting to predict future requirements. This doesn't mean avoiding extensibility entirely, but rather ensuring that every line of code has a clear purpose that serves immediate needs.

**Comment Skepticism**: Approach comments with healthy skepticism. Well-written code should largely speak for itself. Skip comments unless they provide genuine value beyond what the code expresses. Reserve function docstrings for complex logic that's difficult to grasp from the implementation alone. Never include comments about the development process or change history - these belong in commit messages. If you find yourself writing a comment to explain confusing code, consider refactoring the code instead. Remember that comments create maintenance burden, as they must be updated whenever the code changes.

**Whitelist Over Blacklist**: Include what you need rather than excluding what you don't. Define boundaries by explicitly listing valid inputs, valid states, or supported features. This approach scales better, makes edge cases obvious, and leads to more robust code.
