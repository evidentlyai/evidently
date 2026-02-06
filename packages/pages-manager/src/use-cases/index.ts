import fs from 'node:fs'

import { produceMainIndex } from '@lib/produce-pages'
import { getRootPath, join } from '@lib/utils/paths'

const writeIndex = (): void => {
  const indexPath = join(getRootPath(), 'docs', 'index.html')

  const result = produceMainIndex()
  fs.writeFileSync(indexPath, result)
}

const printIndex = (): void => {
  const result = produceMainIndex()

  console.log(result)
}

export const index = {
  writeIndex,
  printIndex
}
