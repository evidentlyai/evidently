import { useState } from 'react'

type onClickFunc<T> = T extends void ? () => void : (args: T) => void

type CustomFormValidatorProps<T> = {
  isStateValid: boolean | string | undefined | null
  onSubmitWithValidState: onClickFunc<T>
  forceShowErrors?: boolean
}

export const useCustomFormValidator = <T = void>(props: CustomFormValidatorProps<T>) => {
  const { isStateValid, onSubmitWithValidState, forceShowErrors } = props

  const [submitButtonWasClicked, setSubmitButtonWasClicked] = useState(false)

  // Shows errors after first click on submit button
  const showErrors = Boolean(submitButtonWasClicked || forceShowErrors)

  const onClick = ((args) => {
    setSubmitButtonWasClicked(true)

    if (!isStateValid) {
      return
    }

    onSubmitWithValidState(args)
  }) as onClickFunc<T>

  const submitButtonProps = {
    variant: 'outlined' as const,
    disabled: showErrors && !isStateValid,
    onClick
  }

  return { submitButtonProps, showErrors }
}
