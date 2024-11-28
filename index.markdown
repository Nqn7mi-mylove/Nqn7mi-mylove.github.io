---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: base
---

<div class="main-content index-page clearfix">
    <div class="post-list">
        {% for post in site.posts %}
        <article class="post-item">
            <div class="post-item-wrapper">
                <div class="post-item-header">
                    <h2 class="post-item-title">
                        <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
                    </h2>
                </div>
                <div class="post-item-meta">
                    <span class="post-date">
                        <i class="fa fa-calendar"></i>
                        {{ post.date | date: '%Y-%m-%d' }}
                    </span>
                    {% if post.categories.size > 0 %}
                    <span class="post-categories">
                        <i class="fa fa-folder"></i>
                        {% for category in post.categories %}
                            <a href="{{ site.baseurl }}/category/#{{ category }}">{{ category }}</a>
                        {% endfor %}
                    </span>
                    {% endif %}
                    {% if post.tags.size > 0 %}
                    <span class="post-tags">
                        <i class="fa fa-tags"></i>
                        {% for tag in post.tags %}
                            <a href="{{ site.baseurl }}/tags/#{{ tag }}">{{ tag }}</a>
                        {% endfor %}
                    </span>
                    {% endif %}
                </div>
                <div class="post-item-content">
                    <p>{{ post.excerpt | strip_html | truncate: 160 }}</p>
                </div>
            </div>
        </article>
        {% endfor %}
    </div>
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
