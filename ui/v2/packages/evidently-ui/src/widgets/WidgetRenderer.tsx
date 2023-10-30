import {
  BigGraphWidgetParams,
  BigTableWidgetParams,
  CounterWidgetParams,
  RichDataParams,
  MultiTabGraphWidgetParams,
  MultiTabWidgetParams,
  PercentWidgetParams,
  TableWidgetParams,
  WidgetGroupParams,
  WidgetListParams,
  WidgetInfo,
  WidgetSize,
  TextWidgetParams,
  TestSuiteWidgetParams
} from '../api'

import Widget from './Widget'
import CounterWidgetContent from './CounterWidgetContent'
import ProgressWidgetContent from './ProgressWidgetContent'
import BigGraphWidgetContent from './BigGraphWidgetContent'
import WidgetPanel from './WidgetPanel'
import NotImplementedWidgetContent from './NotImplementedWidgetContent'
import TabbedGraphWidgetContent from './TabbedGraphWidgetContent'
import TableWidgetContent from './TableWidgetContent'
import BigTableWidgetContent from './BigTableWidget/BigTableWidgetContent'
import TabbedWidgetContent from './TabbedWidgetContent'
import RichDataWidget from './RichDataWidget'
import WidgetList from './WidgetList'
import TextWidgetContent from './TextWidgetContent'
import TestSuiteWidgetContent from './TestSuiteWidget/TestSuiteWidgetContent'

function sizeTransform(size: WidgetSize): 1 | 3 | 6 | 12 {
  if (size === WidgetSize.Small) {
    return 3
  } else if (size === WidgetSize.Medium) {
    return 6
  } else if (size === WidgetSize.Big) {
    return 12
  }
  return 12
}

export function WidgetRenderer(key: string, info: WidgetInfo) {
  let content = <NotImplementedWidgetContent />
  if (info.type === 'counter') {
    content = <CounterWidgetContent {...(info.params as CounterWidgetParams)} />
  } else if (info.type === 'percent') {
    content = <ProgressWidgetContent {...(info.params as PercentWidgetParams)} />
  } else if (info.type === 'big_graph') {
    content = (
      <BigGraphWidgetContent {...(info.params as BigGraphWidgetParams)} widgetSize={info.size} />
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
    <Widget key={key} size={sizeTransform(info.size)}>
      {{
        ...info,
        content: content
      }}
    </Widget>
  )
}
