import { Add as AddIcon } from '@mui/icons-material'
import { Button, Stack, TextField, Typography } from '@mui/material'
import { useState } from 'react'
import { TagsAutocomplete } from '~/components/Tags/TagsAutocomplete'
import { MetadataEditor } from './MetadataEditor'

export type UpdateMetadataArgs = {
  name: string
  description: string
  tags: string[]
  metadata: { [p: string]: string }
}

type EditDatasetMetadataProps = {
  name: string
  description: string
  availableTags: string[]
  tags: string[]
  metadata: { [p: string]: { [p: string]: string } | string[] | string }
  onSave: (args: UpdateMetadataArgs) => void
}

export const EditDatasetMetadataComponent = (props: EditDatasetMetadataProps) => {
  const [name, setName] = useState<string>(props.name)
  const [description, setDescription] = useState<string>(props.description)
  const [tags, setTags] = useState<string[]>(props.tags)
  const [metadataItems, setMetadataItems] = useState<{ key: string; value: string }[]>(
    Object.entries(props.metadata).map((it) => {
      const val = typeof it[1] === 'string' ? it[1] : JSON.stringify(it[1])
      return { key: it[0], value: val }
    })
  )

  return (
    <>
      <Stack direction={'column'} spacing={2}>
        <Typography variant={'body1'}>Name</Typography>
        <TextField size='small' value={name} onChange={(e) => setName(e.target.value)} />
        <Typography variant={'body1'}>Description</Typography>
        <TextField
          size='small'
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <Typography variant={'body1'}>Tags</Typography>
        <TagsAutocomplete availableTags={props.availableTags} tags={tags} onTagsChange={setTags} />
        <Typography variant={'body1'}>Metadata</Typography>
        <MetadataEditor items={metadataItems} onMetadataChange={setMetadataItems} />
        <Stack direction={'row'}>
          <Button
            startIcon={<AddIcon />}
            variant='outlined'
            onClick={() => setMetadataItems((prev) => [...prev, { key: '', value: '' }])}
          >
            Add metadata item
          </Button>
        </Stack>
        <Stack direction={'row'} justifyContent={'flex-end'}>
          <Button
            variant='outlined'
            onClick={() => {
              props.onSave({
                name,
                description,
                tags,
                metadata: Object.fromEntries(
                  metadataItems
                    .filter((v) => v.key !== '' && v.value !== '')
                    .map((v) => [v.key, v.value])
                )
              })
            }}
          >
            Save
          </Button>
        </Stack>
      </Stack>
    </>
  )
}
