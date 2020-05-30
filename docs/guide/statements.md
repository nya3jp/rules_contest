# Managing Problem Statements

`rules_contest` provides some utilities to manage problem statements.

## Rendering Jinja2 templates

Problem statements usually contain problem constraints and sample datasets.
As described in previous sections, `rules_contest` provides rules to manage them
for problems, such as [`cc_yaml_library`] and [`dataset_derive`]. Thus it is
best to avoid managing them in a different way for problem statements.

[`jinja2_template`] rule allows rendering [Jinja2 templates] substituting
variables derived from constraint YAML files, static files and datasets.

Templates have access to the following variables:

| Variable | Description | Example |
| --- | --- | --- |
| `vars` | Constraints from YAML files | `vars.VALUE_MAX` |
| `files` | Content of static files | `files["00_sample1.out"]` |
| `dataset` | Content of the dataset | `dataset["00_sample1.in"]` |

[`cc_yaml_library`]: constraints.html
[`dataset_derive`]: datasets.html
[`jinja2_template`]: ../reference/rules.html#jinja2-template
[Jinja2 templates]: https://jinja.palletsprojects.com/

## Rendering Markdown to HTML

[`markdown`] rule renders a [Markdown] document to a HTML document. This rule
might be useful to build a file to upload to online judge systems.

[`markdown`]: ../reference/rules.html#markdown
[Markdown]: https://en.wikipedia.org/wiki/Markdown
