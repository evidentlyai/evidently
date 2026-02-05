import { apiReferenceIndex } from '@lib/use-cases/api-reference-index'
import { ci } from '@lib/use-cases/ci'
import { index } from '@lib/use-cases/index'
import { consoleGroup, consoleGroupEnd } from '@lib/utils'

const action = process.argv[2]

switch (action) {
  case 'run-all':
    ci.copyNewCIArtifacts()
    apiReferenceIndex.copyNewApiReferences()
    apiReferenceIndex.deleteOldBranchFolders()
    apiReferenceIndex.writeApiReferenceIndex()
    ci.writeCIndex()
    index.writeIndex()

    consoleGroup('index')
    index.printIndex()
    consoleGroupEnd()

    consoleGroup('api-reference')
    apiReferenceIndex.printApiReferenceIndex()
    consoleGroupEnd()

    consoleGroup('ci')
    ci.printCIIndex()
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
