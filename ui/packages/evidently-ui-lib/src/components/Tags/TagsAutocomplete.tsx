import { Autocomplete, Chip, TextField, createFilterOptions } from '@mui/material'

type FilterOptionItem = {
  value: string
  title: string
  existing: boolean
}

export type TagsAutocompleteProps = {
  availableTags: string[]
  tags: string[]
  onTagsChange: (tags: string[]) => void
}

const filter = createFilterOptions<FilterOptionItem>()

export const TagsAutocomplete = (props: TagsAutocompleteProps) => {
  return (
    <Autocomplete
      size={'small'}
      multiple
      renderValue={(value) => {
        return (
          <>
            {value.map((v) => (
              <Chip
                size='small'
                sx={{ mr: 1 }}
                key={v.value}
                label={v.value}
                onClick={() => {
                  props.onTagsChange([...props.tags.filter((it) => it !== v.value)])
                }}
              />
            ))}
          </>
        )
      }}
      renderInput={(params) => <TextField {...params} variant='outlined' />}
      options={props.availableTags.map((v) => ({ value: v, title: v, existing: true }))}
      filterOptions={(options, params) => {
        const filtered = filter(options, params)
        const { inputValue } = params
        const isExisting = options.some((option) => inputValue === option.value)
        if (inputValue !== '' && !isExisting) {
          filtered.push({
            value: inputValue,
            title: `Add "${inputValue}"`,
            existing: false
          })
        }
        return filtered
      }}
      getOptionLabel={(option) => {
        if (typeof option === 'string') {
          return option
        }
        if (!option.existing) {
          return option.title
        }
        return option.value
      }}
      value={props.tags.map((t) => ({ value: t, title: t, existing: true }))}
      onChange={(_, value) => {
        props.onTagsChange(value.map((v) => v.value))
      }}
    />
  )
}

type TagsAutocompleteSingleOptionProps = {
  availableTags: string[]
  tag: string
  onTagChange: (tag: string) => void
}

export const TagsAutocompleteSingleOption = (props: TagsAutocompleteSingleOptionProps) => {
  return (
    <Autocomplete
      size={'small'}
      renderValue={(value) => <Chip size='small' sx={{ mr: 1 }} label={value.value} />}
      renderInput={(params) => <TextField {...params} variant='outlined' />}
      options={props.availableTags.map((v) => ({ value: v, title: v, existing: true }))}
      filterOptions={(options, params) => {
        const filtered = filter(options, params)
        const { inputValue } = params
        const isExisting = options.some((option) => inputValue === option.value)
        if (inputValue !== '' && !isExisting) {
          filtered.push({
            value: inputValue,
            title: `Add "${inputValue}"`,
            existing: false
          })
        }
        return filtered
      }}
      getOptionLabel={(option) => {
        if (typeof option === 'string') {
          return option
        }
        if (!option.existing) {
          return option.title
        }
        return option.value
      }}
      value={props.tag ? { value: props.tag, title: props.tag, existing: true } : undefined}
      onChange={(_, value) => {
        if (!value?.value) {
          return
        }

        props.onTagChange(value.value)
      }}
    />
  )
}
