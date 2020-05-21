# Test Results

{% if report.other_tests -%}
## Unit Tests

| Target | | Message |
| --- | --- | --- |
{% for _, test in report.other_tests|dictsort -%}
| {{ test.target }} | {{ test.result == 'success' and '🍀' or '🔥' }} | {{ test.message }} |
{% endfor -%}
{% endif %}

{% if report.solution_tests -%}
## Solution Tests

| Target | | Message |
| --- | --- | --- |
{% for _, test in report.solution_tests|dictsort -%}
| {{ test.target }} | {{ test.result == 'success' and '🍀' or '🔥' }} | {{ test.message }} |
{% endfor -%}
{% endif %}
