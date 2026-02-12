export const CONFIG = {
  GITHUB_REPO_URL: 'https://github.com/evidentlyai/evidently',
  getLinkToGithubPR: (prNumber: number) => `${CONFIG.GITHUB_REPO_URL}/pull/${prNumber}`
}
