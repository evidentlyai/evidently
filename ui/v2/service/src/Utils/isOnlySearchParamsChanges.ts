import { ShouldRevalidateFunctionArgs } from 'react-router-dom'

export function isOnlySearchParamsChanges({ currentUrl, nextUrl }: ShouldRevalidateFunctionArgs) {
  if (currentUrl.pathname === nextUrl.pathname && currentUrl.search !== nextUrl.search) {
    return true
  }

  return false
}
