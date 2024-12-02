import type { DashboardInfoModel } from '~/api/types'
import {
  DateFilter,
  type DateFilterProps,
  ShowInOrderSwitch,
  type ShowInOrderSwitchProps
} from '~/components/DashboardDateFilter'
import { DashboardWidgets } from '~/components/DashboardWidgets'
import { DashboardViewParamsContext } from '~/contexts/DashboardViewParams'

export const ProjectDashboard = ({
  data,
  dateFilterProps,
  showInOrderProps
}: {
  data: DashboardInfoModel
  dateFilterProps: DateFilterProps
  showInOrderProps: ShowInOrderSwitchProps
}) => {
  return (
    <>
      <DateFilter {...dateFilterProps} flexEnd>
        <ShowInOrderSwitch {...showInOrderProps} />
      </DateFilter>

      <DashboardViewParamsContext.Provider
        value={{ isXaxisAsCategorical: showInOrderProps.isXaxisAsCategorical }}
      >
        <DashboardWidgets widgets={data.widgets} />
      </DashboardViewParamsContext.Provider>
    </>
  )
}
