import { createContext, createRef, useContext } from 'react'

const ref = createRef<HTMLDivElement | null>()

export const TraceToolbarRefContext = createContext<typeof ref>(ref)
export const useTraceToolbarRef = () => useContext(TraceToolbarRefContext)
