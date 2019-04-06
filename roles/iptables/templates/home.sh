{% extends "extends/service-filter.sh" %}

{% block rules %}
{{ super() }}
{% include "includes/part_ssh.sh" %}

{% endblock %}
