import type { GridSlotProps } from '@mui/x-data-grid'
import React, { useContext } from 'react'
import { CustomDatasetToolbar, type CustomDatasetToolbarComponentProps } from './Impl'

const CustomDatasetToolbarContext = React.createContext<CustomDatasetToolbarComponentProps>({
  filters: [],
  setFilters: () => {},
  sortModel: [],
  clearFiltersAndSortModel: () => {},
  columns: []
})

const useCustomDatasetToolbarContext = () => useContext(CustomDatasetToolbarContext)

type DatasetToolbarProps = GridSlotProps['toolbar']

const DatasetToolbar = (standartGridToolbarProps: DatasetToolbarProps) => {
  const toolbarComponentProps = useCustomDatasetToolbarContext()

  return (
    <CustomDatasetToolbar
      toolbarComponentProps={toolbarComponentProps}
      standartGridToolbarProps={standartGridToolbarProps}
    />
  )
}

export const Toolbar = { Component: DatasetToolbar, Context: CustomDatasetToolbarContext }
