HTML_LINK_WITH_ID_TEMPLATE = """
<style>
.evidently-links.container {{
    padding: 10px;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        Segoe UI,
        Roboto,
        Oxygen,
        Ubuntu,
        Cantarell,
        Fira Sans,
        Droid Sans,
        Helvetica Neue,
        sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

    display: flex;
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
}}

.evidently-links.container > p {{
    margin: 0;
    font-size: 0.85rem;
}}

.evidently-links.container > a {{
    font-size: 1rem;
    font-weight: bold;
    padding: 10px 15px;
    border-radius: 5px;
    background-color: #202830;
    color: #fff;
    border: 0;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;
}}

.evidently-links.container > a:hover {{
    background-color: #455565;
    color: #fff;
}}
</style>

<div class="evidently-links container">
    <a target="_blank" href="{button_url}">{button_title}</a>
    <p>
        <b>{id_title}:</b> <span>{id}</span>
    </p>
</div>
"""


def html_link_template(*, id: str, button_url: str, button_title: str, id_title: str) -> str:
    params = dict(
        id=id,
        id_title=id_title,
        button_title=button_title,
        button_url=button_url,
    )

    return HTML_LINK_WITH_ID_TEMPLATE.format(**params)


def get_html_link_to_report(*, url_to_report: str, report_id: str):
    return html_link_template(
        id=report_id,
        id_title="Report ID",
        button_title="View report",
        button_url=url_to_report,
    )
