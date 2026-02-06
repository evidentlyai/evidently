export const CI_ARTIFACTS_VARS = {
  UI_SERVICE_PLAYWRIGHT_REPORT: 'ui-service-playwright-report',
  UI_HTML_VISUAL_TESTING_PLAYWRIGHT_REPORT: 'ui-html-visual-testing-playwright-report',
  PYTEST_HTML_REPORT: 'pytest-html-report'
} as const

export const CI_ARTIFACTS = [
  CI_ARTIFACTS_VARS.UI_SERVICE_PLAYWRIGHT_REPORT,
  CI_ARTIFACTS_VARS.UI_HTML_VISUAL_TESTING_PLAYWRIGHT_REPORT,
  CI_ARTIFACTS_VARS.PYTEST_HTML_REPORT
] as const

export type CIArtifact = (typeof CI_ARTIFACTS)[number]
