import React from 'react'

type CreateErrors<K extends string> = Record<K, { isError: boolean; errorMessage: string }>
const ErrorsContext = React.createContext<CreateErrors<string> | null>(null)
const PrefixContext = React.createContext<string>('')

const NO_ERROR = { isError: false, errorMessage: '' } as const

export const createContextForErrors = <K extends string>() => {
  type WithErrorsProps = { children: React.ReactNode; errors: CreateErrors<K>; showErrors: boolean }
  type WithPrefixProps = { children: React.ReactNode; prefix: string }

  const WithErrors = (props: WithErrorsProps) => (
    <ErrorsContext.Provider value={props.showErrors ? props.errors : null}>
      {props.children}
    </ErrorsContext.Provider>
  )

  const WithPrefix = (props: WithPrefixProps) => (
    <PrefixContext.Provider value={props.prefix}>{props.children}</PrefixContext.Provider>
  )

  const useErrors = () => {
    const errors = React.useContext(ErrorsContext)
    const prefix = React.useContext(PrefixContext)

    const providePrefix = (key: string) => `${prefix}${key}`

    return new Proxy(errors ?? {}, {
      get(target, prop) {
        const value = target?.[providePrefix(prop as string)] ?? NO_ERROR

        if (value.isError) {
          return value
        }

        return NO_ERROR
      }
    }) as CreateErrors<K>
  }

  const createErrors = (errors: CreateErrors<K>) => errors

  const isValid = (errors: CreateErrors<K>) => {
    for (const key in errors) {
      if (errors?.[key]?.isError) {
        return false
      }
    }

    return true
  }

  return { WithErrors, useErrors, createErrors, isValid, WithPrefix }
}
