HTML_LINK_TO_REPORT_TEMPLATE = """
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
    <a target="_blank" href="{url_to_report}">View report</a>
    <p>
        <b>Report ID:</b> <span>{report_id}</span>
    </p>
</div>
"""


def get_html_link_to_report(*, url_to_report: str, report_id: str) -> str:
    return HTML_LINK_TO_REPORT_TEMPLATE.format(url_to_report=url_to_report, report_id=report_id)
