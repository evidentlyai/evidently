import { readFileSync, writeFileSync, lstatSync } from 'node:fs'

const filePath = process.argv[2]

if (!lstatSync(filePath).isFile()) {
  throw `${filePath} is not a file`
}

const pythonFile = readFileSync(filePath, { encoding: 'utf-8' })

const pythonFileTransformed = pythonFile
  .replace(/^(.+) = (.+.run\(.+)\n^\1/gm, '$1 = $2\n$1.save_html("$1.html")')

writeFileSync(filePath, pythonFileTransformed)
