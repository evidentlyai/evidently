import {
  CustomDatasetToolbar,
  type CustomDatasetToolbarComponentProps
} from 'evidently-ui-lib/components/Datasets/Toolbar/Impl'
import type { GridSlotProps } from 'evidently-ui-lib/shared-dependencies/mui-x-date-grid'
import React, { useContext } from 'react'
import {
  DownloadDatasetButton,
  type DownloadDatasetButtonProps
} from './Components/DownloadDatasetButton'

const CustomDatasetToolbarContext = React.createContext<{
  toolbarComponentProps: CustomDatasetToolbarComponentProps
  downloadDatasetButtonProps: DownloadDatasetButtonProps
}>({
  toolbarComponentProps: {
    filters: [],
    setFilters: () => {},
    sortModel: [],
    clearFiltersAndSortModel: () => {},
    columns: []
  },
  downloadDatasetButtonProps: { datasetId: '' }
})

const useCustomDatasetToolbarContext = () => useContext(CustomDatasetToolbarContext)

type DatasetToolbarProps = GridSlotProps['toolbar']

const DatasetToolbar = (standartGridToolbarProps: DatasetToolbarProps) => {
  const { downloadDatasetButtonProps, toolbarComponentProps } = useCustomDatasetToolbarContext()

  return (
    <CustomDatasetToolbar
      toolbarComponentProps={toolbarComponentProps}
      standartGridToolbarProps={standartGridToolbarProps}
      slotOne={<DownloadDatasetButton {...downloadDatasetButtonProps} />}
    />
  )
}

export const Toolbar = {
  Component: DatasetToolbar,
  Context: CustomDatasetToolbarContext,
  useContext: useCustomDatasetToolbarContext
}
