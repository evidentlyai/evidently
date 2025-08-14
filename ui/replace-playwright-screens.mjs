import { execSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import readline from 'node:readline'

async function confirm(question)  {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout })

  return new Promise((resolve) => {
    rl.question(`${question} (Y/n): `, (answer) => {
      rl.close()
      const trimmedAnswer = answer.trim().toLowerCase()

      if (trimmedAnswer === '' || trimmedAnswer === 'y') {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

const PREFIX = 'data:application/zip;base64,'
const PLW_PATH = 'playwright-report'

// Get service path from command line arguments, default to 'service'
const servicePath = process.argv[2] || 'service'

async function main() {
  console.log(`Using service path: ${servicePath}`)

  const data = readFileSync(`./${PLW_PATH}/index.html`, { encoding: 'utf8' })
  const base64 = [
    ...data.matchAll(/<script>\n\s*window\.playwrightReportBase64\s*=\s*"(.+)"/g)
  ][0][1].replace(PREFIX, '')

  execSync(`mkdir -p ${PLW_PATH}/tmp`)
  writeFileSync(`${PLW_PATH}/tmp/tmp_arc.zip`, base64, { encoding: 'base64' })
  execSync(`unzip ${PLW_PATH}/tmp/tmp_arc.zip -d ${PLW_PATH}/tmp`)

  const report = readFileSync(`./${PLW_PATH}/tmp/report.json`, { encoding: 'utf8' })

  execSync(`rm -r ${PLW_PATH}/tmp || true`)

  const failedTests =
    JSON.parse(report)
      .files.find((e) => e.fileName === 'visual.spec.ts')
      ?.tests?.filter(({ ok }) => !ok) || []


  const attachments = failedTests.map((e) => e.results[0].attachments)

  const actualFailedFilesInfo = attachments.map((e) =>
    e.find(({ name }) => name.endsWith('actual.png'))
  )

  const actualFailedFilesInfoReplaced = actualFailedFilesInfo.map((e) => ({name: e.name.replace('actual.png', 'chromium-linux.png'), path: e.path}))

  console.log('Use this files to replace:')

  console.log(
    actualFailedFilesInfoReplaced.map(({ name }) => name)
  )

  const yes = await confirm('Do you want to continue?')
  if (yes) {
    for (const { name, path } of actualFailedFilesInfoReplaced) {
      execSync(`cp ./${PLW_PATH}/${path} ${servicePath}/tests/visual.spec.ts-snapshots/${name}`)
    }
  }

}

////////////////
//  main
////////////////

main()
