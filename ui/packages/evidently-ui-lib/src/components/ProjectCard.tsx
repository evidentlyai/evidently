import React, { useEffect, useState } from 'react'
import { Form, Link as RouterLink, useNavigation, useSubmit } from 'react-router-dom'
import {
  Box,
  Button,
  IconButton,
  Link,
  Paper,
  TextField,
  ToggleButton,
  Tooltip,
  Typography
} from '@mui/material'

import { Add as AddIcon } from '@mui/icons-material'

import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import { useToggle } from '@uidotdev/usehooks'
import { ProjectInfo } from '~/api'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useTheme } from '@mui/material/styles'

// validation here
const editProjectInfoSchema = z.object({
  name: z.string().min(3),
  description: z.string()
})

export const EditProjectInfoForm = ({
  project,
  disabled,
  action
}: {
  action?: string
  project: Partial<ProjectInfo>
  disabled: boolean
}) => {
  const {
    setFocus,
    register,
    handleSubmit,
    formState: { errors, dirtyFields }
  } = useForm<z.infer<typeof editProjectInfoSchema>>({
    resolver: zodResolver(editProjectInfoSchema),
    defaultValues: {
      name: project.name || '',
      description: project.description || ''
    }
  })

  const { palette } = useTheme()

  // for form submitting
  const submit = useSubmit()

  // focus on the firs input
  useEffect(() => setFocus('name'), [setFocus])

  return (
    <>
      <Form
        onSubmit={handleSubmit(({ name, description }) =>
          // here we inject the new `name` and `description`
          // to project object, then it goes to the action

          submit(
            Object.assign(
              {
                ...project,
                name,
                description
              },
              // we use `action` string to identify action type (like `create new` or edit existing)
              (action && { action }) || null
            ),
            { method: 'put', replace: true, encType: 'application/json' }
          )
        )}
        style={{ opacity: disabled ? 0.5 : 1 }}
      >
        {/* name */}
        <TextField
          {...register('name')}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          placeholder="Name"
          InputProps={{
            style: { color: palette.primary.main, fontSize: '20px', fontWeight: '500' }
          }}
          disabled={disabled}
          variant="standard"
        ></TextField>
        {/* description */}
        <TextField
          {...register('description')}
          error={Boolean(errors.description)}
          helperText={errors.description?.message}
          placeholder="Description"
          disabled={disabled}
          fullWidth
          // this `multiline` below causes Material-UI: Too many re-renders
          // multiline
          variant="standard"
        ></TextField>
        {/* Submit button */}
        <Box sx={{ display: 'flex', justifyContent: 'right' }}>
          <Button
            variant="outlined"
            disabled={
              disabled ||
              // we didn't touch any fields
              Object.keys(dirtyFields).length === 0 ||
              // error here
              Object.keys(errors).length > 0
            }
            style={{ marginTop: '10px' }}
            color="primary"
            type="submit"
          >
            Save
          </Button>
        </Box>
      </Form>
    </>
  )
}

const ProjectInfoCard = ({ project }: { project: ProjectInfo }) => {
  return (
    <>
      <Link component={RouterLink} to={`/projects/${project.id}`}>
        <Typography variant={'h6'}>{project.name}</Typography>
      </Link>
      <Typography style={{ whiteSpace: 'pre-line' }} variant="body1">
        {project.description}
      </Typography>
    </>
  )
}

interface projectProps {
  project: ProjectInfo
  children?: React.ReactNode
}

export const ProjectCard: React.FC<projectProps> = ({ project, children }) => {
  const [isEditMode, setEditMode] = useState(false)

  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'
  const submit = useSubmit()

  // project has changed -> set edit mode to false
  useEffect(() => setEditMode(false), [project])

  return (
    <Paper
      sx={{
        m: 1,
        p: 2,
        position: 'relative',
        '&:hover .action-buttons': {
          opacity: 1
        }
      }}
    >
      <Box style={{ position: 'absolute', top: '5px', right: '5px' }}>
        <Box
          sx={{
            opacity: 0,
            transition: (theme) =>
              theme.transitions.create('opacity', {
                duration: theme.transitions.duration.enteringScreen
              })
          }}
          className={'action-buttons'}
          display={'flex'}
          columnGap={1}
        >
          <IconButton
            disabled={isDisabled || isEditMode}
            onClick={() => {
              if (confirm('Are you sure you want to delete this project?') === true) {
                submit(
                  {
                    projectId: project.id,
                    action: 'delete-project'
                  },
                  { method: 'post', replace: true, encType: 'application/json' }
                )
              }
            }}
          >
            <DeleteIcon />
          </IconButton>

          <ToggleButton
            color="primary"
            value={'edit-mode'}
            selected={isEditMode}
            size="small"
            disabled={isDisabled}
            sx={{ border: 'none', borderRadius: '50%' }}
            onChange={() => setEditMode((mode) => !mode)}
          >
            <EditIcon />
          </ToggleButton>
        </Box>
      </Box>

      {children}

      {isEditMode ? (
        <EditProjectInfoForm project={project} disabled={isDisabled} />
      ) : (
        <ProjectInfoCard project={project} />
      )}
    </Paper>
  )
}

export const AddNewProjectButton = ({
  project,
  children
}: {
  project?: Partial<ProjectInfo>
  children?: React.ReactNode
}) => {
  const [on, toggle] = useToggle(false)
  const [wasSubmitting, toggleSubmitting] = useToggle(false)
  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'

  useEffect(() => {
    if (navigation.state === 'submitting') {
      toggleSubmitting(true)
    }
  }, [navigation.state === 'submitting'])

  useEffect(() => {
    if (wasSubmitting && navigation.state === 'idle') {
      toggle(false)
      toggleSubmitting(false)
    }
  }, [wasSubmitting, navigation.state === 'idle'])

  return (
    <Box py={2}>
      <Box display={'flex'} justifyContent={'center'}>
        <Tooltip title="Create new project">
          <ToggleButton
            disabled={isDisabled}
            color="primary"
            value={'check'}
            selected={on}
            size="small"
            sx={{ border: 'none', borderRadius: '50%' }}
            onChange={() => toggle()}
          >
            <AddIcon />
          </ToggleButton>
        </Tooltip>
      </Box>

      {on && (
        <Box p={3} display={'flex'} flexDirection={'column'} rowGap={1}>
          {children}
          <EditProjectInfoForm
            project={project || { name: '', description: '' }}
            disabled={isDisabled}
            action="create-new-project"
          />
        </Box>
      )}
    </Box>
  )
}
