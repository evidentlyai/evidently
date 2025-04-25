type IPanelProps = { type: string; size: 'full' | 'half' }

export type MakePanel<T extends IPanelProps> = T
