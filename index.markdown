---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: base
---

<div class="main-content index-page clearfix">
    {% for post in paginator.posts %}
    <article class="post">
        <div class="post-header">
            <h2 class="post-title">
                <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </h2>
        </div>
        <div class="post-content">
            <p>{{ post.excerpt | strip_html | truncate: 160 }}</p>
        </div>
        <div class="post-meta">
            <span class="post-time">{{ post.date | date: '%Y-%m-%d' }}</span>
        </div>
    </article>
    {% endfor %}
</div>

{% if paginator.total_pages > 1 %}
<div class="pagination">
    {% if paginator.previous_page %}
        <a href="{{ paginator.previous_page_path | prepend: site.baseurl }}">&laquo; Prev</a>
    {% endif %}

    {% for page in (1..paginator.total_pages) %}
        {% if page == paginator.page %}
            <span class="current">{{ page }}</span>
        {% elsif page == 1 %}
            <a href="{{ site.baseurl }}/">{{ page }}</a>
        {% else %}
            <a href="{{ site.baseurl }}/page{{ page }}">{{ page }}</a>
        {% endif %}
    {% endfor %}

    {% if paginator.next_page %}
        <a href="{{ paginator.next_page_path | prepend: site.baseurl }}">Next &raquo;</a>
    {% endif %}
</div>
{% endif %}
