import {
  type AdditionalGraphInfo,
  type BigTableWidgetParams,
  type CounterWidgetParams,
  type MultiTabGraphWidgetParams,
  type MultiTabWidgetParams,
  type PercentWidgetParams,
  type RichDataParams,
  type TableWidgetParams,
  type TestSuiteWidgetParams,
  type TextWidgetParams,
  type WidgetGroupParams,
  type WidgetInfo,
  type WidgetListParams,
  WidgetSize
} from '~/api'

import BigGraphWidgetContent from './BigGraphWidgetContent'
import BigTableWidgetContent from './BigTableWidget/BigTableWidgetContent'
import CounterWidgetContent from './CounterWidgetContent'
import NotImplementedWidgetContent from './NotImplementedWidgetContent'
import ProgressWidgetContent from './ProgressWidgetContent'
import RichDataWidget from './RichDataWidget'
import TabbedGraphWidgetContent from './TabbedGraphWidgetContent'
import TabbedWidgetContent from './TabbedWidgetContent'
import TableWidgetContent from './TableWidgetContent'
import TestSuiteWidgetContent from './TestSuiteWidget/TestSuiteWidgetContent'
import TextWidgetContent from './TextWidgetContent'
import Widget from './Widget'
import WidgetList from './WidgetList'
import WidgetPanel from './WidgetPanel'

function sizeTransform(size: WidgetSize): 1 | 3 | 6 | 12 {
  if (size === WidgetSize.Small) {
    return 3
  }

  if (size === WidgetSize.Medium) {
    return 6
  }

  if (size === WidgetSize.Big) {
    return 12
  }

  return 12
}

export function WidgetRenderer(
  key: string,
  info: WidgetInfo,
  ItemWrapper?: ({ id, children }: { id: string; children: React.ReactNode }) => React.ReactNode
) {
  let content = <NotImplementedWidgetContent />
  if (info.type === 'counter') {
    content = <CounterWidgetContent {...(info.params as CounterWidgetParams)} />
  } else if (info.type === 'percent') {
    content = <ProgressWidgetContent {...(info.params as PercentWidgetParams)} />
  } else if (info.type === 'big_graph') {
    content = (
      <BigGraphWidgetContent {...(info.params as AdditionalGraphInfo)} widgetSize={info.size} />
    )
  } else if (info.type === 'tabbed_graph') {
    content = (
      <TabbedGraphWidgetContent
        {...(info.params as MultiTabGraphWidgetParams)}
        widgetSize={info.size}
      />
    )
  } else if (info.type === 'tabs') {
    content = (
      <TabbedWidgetContent
        {...(info as unknown as MultiTabWidgetParams)}
        widgetSize={info.size}
        id={'twc_'}
      />
    )
  } else if (info.type === 'table') {
    content = <TableWidgetContent {...(info.params as TableWidgetParams)} />
  } else if (info.type === 'big_table') {
    content = (
      <BigTableWidgetContent {...(info.params as BigTableWidgetParams)} widgetSize={info.size} />
    )
  } else if (info.type === 'group') {
    content = (
      <WidgetPanel>
        {(info as unknown as WidgetGroupParams).widgets.map((wi, idx) =>
          WidgetRenderer(`wi_${idx}`, wi)
        )}
      </WidgetPanel>
    )
  } else if (info.type === 'rich_data') {
    content = <RichDataWidget {...(info.params as RichDataParams)} widgetSize={info.size} />
  } else if (info.type === 'list') {
    const listInfo = info as unknown as WidgetListParams
    content = (
      <WidgetList widgets={listInfo.widgets} pageSize={listInfo.pageSize} widgetSize={info.size} />
    )
  } else if (info.type === 'text') {
    content = <TextWidgetContent {...(info.params as TextWidgetParams)} />
  } else if (info.type === 'test_suite') {
    content = <TestSuiteWidgetContent {...(info.params as TestSuiteWidgetParams)} />
  }
  return (
    <Widget key={key} size={sizeTransform(info.size)} ItemWrapper={ItemWrapper}>
      {{
        ...info,
        content: content
      }}
    </Widget>
  )
}
