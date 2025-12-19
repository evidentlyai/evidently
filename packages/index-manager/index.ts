import { apiReferenceIndex } from '@lib/use-cases/api-reference-index'
import { index } from '@lib/use-cases/index'
import { consoleGroup, consoleGroupEnd } from '@lib/utils'

const action = process.argv[2]

switch (action) {
  case 'index:write':
    index.writeIndex()
    break
  case 'index:print':
    index.printIndex()
    break
  case 'copy-new-api-references':
    apiReferenceIndex.copyNewApiReferences()
    break
  case 'delete-old-branch-folders':
    apiReferenceIndex.deleteOldBranchFolders()
    break
  case 'run-all':
    apiReferenceIndex.copyNewApiReferences()
    apiReferenceIndex.deleteOldBranchFolders()
    apiReferenceIndex.writeApiReferenceIndex()
    index.writeIndex()

    consoleGroup('index')
    index.printIndex()
    consoleGroupEnd()

    consoleGroup('api-reference')
    apiReferenceIndex.printApiReferenceIndex()
    consoleGroupEnd()
    break
  default:
    console.error(`Unknown action: ${action}`)
    console.error('Available actions:')
    console.error('- index:write')
    console.error('- index:print')
    console.error('- index:prepare-api-reference')
    console.error('- run-all')
    process.exit(1)
}
