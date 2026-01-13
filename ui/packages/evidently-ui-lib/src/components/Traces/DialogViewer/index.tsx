import { Box, Card, CardActionArea, CardContent, Divider, Stack, Typography } from '@mui/material'
import type { TraceModel } from 'api/types'
import { useEffect, useRef, useState } from 'react'
import { FieldAutocomplete } from './components/FieldAutocomplete'
import { SessionCardContent } from './components/SessionCardContent'
import { TraceComponent } from './components/TraceComponent'
import type { Description } from './types'

type DialogViewerProps = {
  data: Record<string, TraceModel[]>
  description: Description
  traceHeader: (props: { trace: TraceModel }) => React.ReactNode
}

export const DialogViewer = (props: DialogViewerProps) => {
  const { data, description, traceHeader } = props

  const ref = useRef<HTMLElement>(null)

  const input = description.inputAttribute || ''
  const output = description.outputAttribute || ''

  const sessions = Object.keys(data)

  const isSingleSession = sessions.length === 1

  const [sessionId, setSessionId] = useState({ sessionId: sessions.length > 0 ? sessions[0] : '' })

  const isAFewSessions = !isSingleSession && sessionId.sessionId

  useEffect(() => {
    if (sessionId.sessionId && ref?.current) {
      const element = ref.current
      const rect = element.getBoundingClientRect()
      const isTopVisible =
        rect.top >= 0 && rect.top < (window.innerHeight || document.documentElement.clientHeight)

      if (!isTopVisible) {
        element.scrollIntoView()
      }
    }
  }, [sessionId.sessionId])

  let [selectedSessionId, selectedTraces] = Object.entries(data)[0]

  if (
    sessionId.sessionId !== '' &&
    !isSingleSession &&
    Object.keys(data).findIndex((value) => value === sessionId.sessionId) >= 0
  ) {
    selectedSessionId = sessionId.sessionId
    selectedTraces = data[sessionId.sessionId ?? 'undefined']
  }

  const dataValues = Object.values(data)
  let fields: string[] = []
  if (dataValues.length > 0 && dataValues[0].length > 0) {
    const firstTrace = dataValues[0][0]
    fields = [
      ...new Set(
        firstTrace.spans.flatMap((s) =>
          Object.keys(s.attributes).map((attr) => `${s.span_name}:${attr}`)
        )
      )
    ]
  }

  return (
    <Box
      ref={ref}
      display={'grid'}
      gridTemplateColumns={isAFewSessions ? 'min(25%, 400px) 1fr' : '0 1fr'}
      sx={{ transition: '625ms ease-in-out' }}
    >
      <Box borderRight={isAFewSessions ? '1px solid' : 'none'} borderColor='divider'>
        <Box position='sticky' top={0} left={0} zIndex={3}>
          {isAFewSessions && (
            <Box p={3} maxHeight={'100vh'} overflow={'scroll'}>
              <Stack gap={1}>
                {sessions.map((sessionId) => (
                  <Card
                    key={sessionId}
                    sx={[
                      { border: '1px solid', borderColor: 'divider' },
                      selectedSessionId === sessionId && {
                        borderColor: 'primary.main'
                      }
                    ]}
                  >
                    <CardActionArea onClick={() => setSessionId({ sessionId })}>
                      <CardContent>
                        <SessionCardContent
                          traces={data[sessionId ?? 'undefined']}
                          description={{
                            ...description,
                            inputAttribute: input,
                            outputAttribute: output
                          }}
                        />
                      </CardContent>
                    </CardActionArea>
                  </Card>
                ))}
              </Stack>
            </Box>
          )}
        </Box>
      </Box>

      <Box maxWidth={'lg'} mx={'auto'} px={1} width='100%' minWidth={0} overflow='scroll'>
        <Stack direction={'row'} gap={2} justifyContent={'center'} alignItems={'flex-end'} pb={1}>
          <Box maxWidth={300} width={1}>
            <Typography variant='subtitle2' gutterBottom>
              User message field
            </Typography>

            <FieldAutocomplete
              value={description.inputAttribute}
              setValue={description.setInputAttribute}
              options={fields}
            />
          </Box>

          <Box maxWidth={300} width={1}>
            <Typography variant='subtitle2' gutterBottom>
              Assistant message field
            </Typography>

            <FieldAutocomplete
              value={description.outputAttribute}
              setValue={description.setOutputAttribute}
              options={fields}
            />
          </Box>
        </Stack>

        <Stack mt={2} gap={2} direction={'column'} divider={<Divider />}>
          {selectedTraces.map((trace) => (
            <Box key={trace.trace_id} width='100%' maxWidth={0.95} mx={'auto'}>
              <TraceComponent
                data={trace}
                traceHeader={traceHeader({ trace })}
                description={{ ...description, inputAttribute: input, outputAttribute: output }}
              />
            </Box>
          ))}
        </Stack>
      </Box>
    </Box>
  )
}
