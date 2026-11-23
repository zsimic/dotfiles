# Code design

For repos that hold domain state and will grow (not config, glue, or one-off scripts):

- Model each domain concept as a class that owns its data and the behavior on it, in the spirit of
  Meyer's *Object-Oriented Software Construction*: callers ask the object, they don't reach into it.
- A dict with fixed keys, or a cluster of functions passing the same dict or tuple around, is a
  missing class. So is a function that mostly reads one object's attributes: make it a method.
- Free functions suit stateless helpers. Entry points a framework requires as functions (CLI
  commands, task or operation decorators) stay thin: parse input, ask the model, report.
- The object model earns a docs page (written per [`repo-docs.md`](./repo-docs.md)): the main
  concepts, which class owns what, how they collaborate.
