import { Box, Card, CardActionArea, CardContent, Divider, Stack, Typography } from '@mui/material'
import type { TraceModel } from 'api/types'
import { useRef, useState } from 'react'
import { FieldAutocomplete } from './components/FieldAutocomplete'
import { SessionCardContent } from './components/SessionCardContent'
import { TraceComponent } from './components/TraceComponent'
import type { Description } from './types'

type DialogViewerProps = {
  data: Record<string, TraceModel[]>
  description: Description
  LinkToTrace: (props: { traceId: string }) => JSX.Element
}

export const DialogViewer = (props: DialogViewerProps) => {
  const { data, description, LinkToTrace } = props

  const ref = useRef<HTMLElement>(null)
  let input = description.inputAttribute
  let output = description.outputAttribute

  if (input === null || input === '') {
    if (Object.values(data).flat().length > 0) {
      const rootSpan = Object.values(data)
        .flat()[0]
        .spans.find((x) => x.parent_span_id === '')
      if (rootSpan) {
        input = Object.keys(rootSpan.attributes).filter((x) => x !== 'result')[0]
      }
    }
  }

  if (output === null || output === '') {
    output = 'result'
  }

  const sessions = Object.keys(data)

  const isSingleSession = sessions.length === 1

  const [sessionId, setSessionId] = useState({ sessionId: sessions.length > 0 ? sessions[0] : '' })

  let [selectedSessionId, selectedTraces] = Object.entries(data)[0]

  if (
    sessionId.sessionId !== '' &&
    !isSingleSession &&
    Object.keys(data).findIndex((value) => value === sessionId.sessionId) >= 0
  ) {
    selectedSessionId = sessionId.sessionId
    selectedTraces = data[sessionId.sessionId ?? 'undefined']
  }

  const isAFewSessions = !isSingleSession && sessionId.sessionId

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
      gridTemplateColumns={`${isAFewSessions ? 400 : 0}px  calc(100% - ${isAFewSessions ? 400 : 0}px)`}
      alignItems={'start'}
      sx={{ transition: '625ms ease-in-out' }}
    >
      <Box
        sx={{
          height: 1,
          borderRightStyle: 'solid',
          borderRightWidth: isAFewSessions ? '1px' : '0px',
          borderRightColor: 'divider'
        }}
      >
        <Box sx={{ position: 'sticky', top: 0, left: 0, overflowX: 'hidden', zIndex: 3 }}>
          {isAFewSessions && (
            <Box p={3} maxHeight={'100vh'} overflow={'scroll'}>
              <Stack gap={1}>
                {sessions.map((sessionId) => (
                  <Card
                    key={sessionId}
                    sx={[
                      {
                        border: '1px solid',
                        borderColor: 'divider'
                      },
                      selectedSessionId === sessionId && {
                        borderColor: 'primary.main'
                      }
                    ]}
                  >
                    <CardActionArea
                      onClick={() => {
                        setSessionId({ sessionId })
                        ref?.current?.scrollIntoView()
                      }}
                    >
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

      <Box>
        <Box maxWidth={'lg'} mx={'auto'}>
          <Stack direction={'row'} gap={2} justifyContent={'center'} alignItems={'flex-end'} pb={1}>
            <Box sx={{ minWidth: 300 }}>
              <Typography variant='subtitle2' gutterBottom>
                User message field
              </Typography>

              <FieldAutocomplete
                value={description.inputAttribute}
                setValue={description.setInputAttribute}
                options={fields}
              />
            </Box>

            <Box sx={{ minWidth: 300 }}>
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

          <Stack gap={2} direction={'column'} divider={<Divider sx={{ my: 3 }} />}>
            {selectedTraces.map((v) => (
              <Box key={v.trace_id} width={0.95} mx={'auto'}>
                <TraceComponent
                  data={v}
                  LinkToTrace={LinkToTrace}
                  description={{
                    ...description,
                    inputAttribute: input,
                    outputAttribute: output
                  }}
                />
              </Box>
            ))}
          </Stack>
        </Box>
      </Box>
    </Box>
  )
}
