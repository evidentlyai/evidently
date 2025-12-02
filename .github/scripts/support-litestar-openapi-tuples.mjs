import { readFileSync, writeFileSync, lstatSync } from 'node:fs'

const filePath = process.argv[2]

if (!lstatSync(filePath).isFile()) {
  throw `${filePath} is not a file`
}

const openapiSchema = readFileSync(filePath, { encoding: 'utf-8' })

const openapiSchemaWithoutStrangeTuples = openapiSchema
  .replace(/\n^\s*default: !!python\/tuple.*(\n\s*-.+)*/gm, '')
  .replace(/- default: !!python\/tuple(.*)(\n\s*-.+)*/gm, "- default: '!!python/tuple$1'")

writeFileSync(filePath, openapiSchemaWithoutStrangeTuples)

console.log('transform tuples done!'.toUpperCase())
