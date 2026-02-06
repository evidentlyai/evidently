// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  blue: '\x1b[34m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  orange: '\x1b[38;5;208m',
  red: '\x1b[31m',
  magenta: '\x1b[35m',
  gray: '\x1b[90m'
} as const

export const consoleGroup = (message: string) => {
  console.group(`${colors.blue}${colors.bright}${message.toUpperCase()}${colors.reset}`)
}

export const consoleGroupEnd = () => console.groupEnd()

export const colorize = {
  branch: (text: string) => `${colors.cyan}${colors.bright}${text}${colors.reset}`,
  time: (text: string) => `${colors.yellow}${text}${colors.reset}`,
  date: (text: string) => `${colors.gray}${text}${colors.reset}`,
  deleted: (text: string) => `${colors.red}${colors.bright}✓ ${text}${colors.reset}`,
  kept: (text: string) => `${colors.green}${colors.dim}→ ${text}${colors.reset}`,
  age: (days: number) => {
    if (days < 1) return `${colors.green}${days}${colors.reset}`
    if (days < 3) return `${colors.yellow}${days}${colors.reset}`
    if (days < 7) return `${colors.orange}${days}${colors.reset}`
    return `${colors.red}${days}${colors.reset}`
  }
}
