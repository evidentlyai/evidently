import React, { useContext } from 'react'

export type WidgetWrapper = {
  WidgetWrapper: ({ id, children }: { id: string; children: React.ReactNode }) => JSX.Element
}

const EmptyWidgetWrapper: WidgetWrapper['WidgetWrapper'] = ({ children }) => <>{children}</>

export const widgetWrapperContext = React.createContext<WidgetWrapper>({
  WidgetWrapper: EmptyWidgetWrapper
})

export const useWidgetWrapper = () => useContext(widgetWrapperContext)
