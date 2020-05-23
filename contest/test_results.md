{% if report.broken_tests -%}
# Broken Tests

| Target | | Message |
| --- | --- | --- |
{% for _, test in report.broken_tests|dictsort -%}
| {{ test.target }} | 🔥 | {{ test.message }} |
{% endfor -%}
{% endif -%}

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

{% for _, matrix in report.judge_matrices|dictsort -%}
## {{ matrix.judge_target }}

| Test case |{% for t in matrix.test_targets %} {{ t.split(':')[-1] }} |{% endfor %}
| --- |{% for t in matrix.test_targets %} --- |{% endfor %}
{% for case_name, row in matrix.cases|dictsort -%}
| **{{ case_name }}** |{% for t in matrix.test_targets %}{% set case = row[t] %} {% if case and case.result != 'skipped' %}{% if case.result == 'accepted' %}{{ "%.1fs"|format(case.solution_time) }}{% else %}{{ case.message }}{% endif %}{% endif %} |{% endfor %}
{% endfor -%}
{% endfor -%}
