# Unit Tests

| Target | | Message |
| --- | --- | --- |
{% for _, test in report.other_tests|dictsort -%}
| {{ test.target }} | {{ test.result == 'success' and '🍀' or '🔥' }} | {{ test.message }} |
{% endfor -%}

# Solution Tests

| Target | | Message |
| --- | --- | --- |
{% for _, test in report.solution_tests|dictsort -%}
| {{ test.target }} | {{ test.result == 'success' and '🍀' or '🔥' }} | {{ test.message }} |
{% endfor -%}

# Solution Details

{% for _, test in report.solution_tests|dictsort -%}
## {{ test.target }} {{ test.result == 'success' and '🍀' or '🔥' }}

{{ test.message }}

| Test case | Result | Time | Message |
| --- | --- | ---: | --- |
{% for case in test.cases -%}
{% if case.result != 'skipped' -%}
| {{ case.name }} | {{ case.result }} | {{ "%.1fs"|format(case.solution_time) }} | {{ case.message }} |
{% endif -%}
{% endfor -%}
{% endfor -%}
