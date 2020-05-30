# Managing Problem Constraints

Managing problem constraints in a central place is important to avoid
disagreement among problem statements, generator, validator, judge etc.
`rules_contest` supports describing problem constraints in a [YAML] file.

[YAML]: https://en.wikipedia.org/wiki/YAML

## Constraint YAML files

Constraint YAML files describe problem constraints in [the YAML format].
Constraint YAML files should be a simple key-value mapping, such as:

```yaml
VALUE_MAX: 1000000  # Maximum input number
ERROR_MAX: 0.001    # Permitted error in outputs
```

[the YAML format]: https://yaml.org/

## Generating source code from constraint YAML files

[`cc_yaml_library`] rule generates a C++ header file from a YAML file.

For example, the example YAML file above is converted to the following C++
header file.

```cc
#define VALUE_MAX 1000000
#define ERROR_MAX 0.001
```

There are other language variants such as [`py_yaml_library`].
See [the reference] for the complete list of available language variants.

[`cc_yaml_library`]: ../reference/rules.html#cc-yaml-library
[`py_yaml_library`]: ../reference/rules.html#py-yaml-library
[the reference]: ../reference/rules.html

## Referencing problem constraints in problem statements

It is also possible to reference problem constraints in YAML files in problem
statements. See [Managing Problem Statements] section for details.

[Managing Problem Statements]: statements.html
