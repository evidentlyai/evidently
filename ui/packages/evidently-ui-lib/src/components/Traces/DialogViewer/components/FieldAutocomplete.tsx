import { Autocomplete, TextField, createFilterOptions } from '@mui/material'

type FieldAutocompleteProps = {
  value: string
  setValue: (value: string) => void
  options: string[]
}

export const FieldAutocomplete = (props: FieldAutocompleteProps) => {
  const { value, setValue, options } = props

  return (
    <Autocomplete
      size='small'
      onChange={(_, value) => {
        setValue(value?.value ?? '')
      }}
      value={{ value: value, title: value }}
      ListboxProps={{ sx: { maxHeight: 200 } }}
      options={options.map((x) => ({ value: x, title: x }))}
      getOptionLabel={(opt) => opt.title}
      getOptionKey={(opt) => opt.value}
      renderInput={(params) => <TextField {...params} fullWidth />}
      selectOnFocus
      clearOnBlur
      filterOptions={(options, params) => {
        const filtered = createFilterOptions<{ value: string; title: string }>()(options, params)

        const { inputValue } = params
        // Suggest the creation of a new value
        const isExisting = options.some((option) => inputValue === option.value)
        if (inputValue !== '' && !isExisting) {
          filtered.push({ value: inputValue, title: `Add: ${inputValue}` })
        }

        return filtered
      }}
    />
  )
}
