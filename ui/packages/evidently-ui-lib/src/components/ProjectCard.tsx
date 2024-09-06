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
import type React from 'react'
import { useEffect, useState } from 'react'
import { Form, Link as RouterLink, useNavigation, useSubmit } from 'react-router-dom'

import { Add as AddIcon } from '@mui/icons-material'

import { zodResolver } from '@hookform/resolvers/zod'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'
import { useTheme } from '@mui/material/styles'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import type { ProjectModel } from '~/api/types'
import type { StrictID } from '~/api/types/utils'

// validation here
const editProjectInfoSchema = z.object({
  name: z.string().min(3),
  description: z.string()
})

export const EditProjectInfoForm = ({
  project,
  action
}:
  | {
      action: 'edit-project'
      project: StrictID<ProjectModel>
    }
  | {
      action: 'create-new-project'
      project: Omit<ProjectModel, 'id'>
    }) => {
  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'

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
            // @ts-ignore
            {
              ...project,
              name,
              description,
              action: action
            },
            { method: 'put', replace: true, encType: 'application/json' }
          )
        )}
        style={{ opacity: isDisabled ? 0.5 : 1 }}
      >
        {/* name */}
        <TextField
          {...register('name')}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          placeholder='Name'
          InputProps={{
            style: { color: palette.primary.main, fontSize: '20px', fontWeight: '500' }
          }}
          disabled={isDisabled}
          variant='standard'
        />
        {/* description */}
        <TextField
          {...register('description')}
          error={Boolean(errors.description)}
          helperText={errors.description?.message}
          placeholder='Description'
          disabled={isDisabled}
          fullWidth
          // this `multiline` below causes Material-UI: Too many re-renders
          // multiline
          variant='standard'
        />
        {/* Submit button */}
        <Box sx={{ display: 'flex', justifyContent: 'right' }}>
          <Button
            variant='outlined'
            disabled={
              isDisabled ||
              // we didn't touch any fields
              Object.keys(dirtyFields).length === 0 ||
              // error here
              Object.keys(errors).length > 0
            }
            style={{ marginTop: '10px' }}
            color='primary'
            type='submit'
          >
            Save
          </Button>
        </Box>
      </Form>
    </>
  )
}

export const ProjectInfoCard = ({ project }: { project: StrictID<ProjectModel> }) => {
  return (
    <>
      <Link component={RouterLink} to={`projects/${project.id}`}>
        <Typography variant={'h6'}>{project.name}</Typography>
      </Link>
      <Typography style={{ whiteSpace: 'pre-line' }} variant='body1'>
        {project.description}
      </Typography>
    </>
  )
}

interface ProjectProps {
  project: StrictID<ProjectModel>
}

export const ProjectCard: React.FC<ProjectProps> = ({ project }) => {
  const [isEditMode, setEditMode] = useState(false)

  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'
  const submit = useSubmit()

  // biome-ignore lint: project has changed -> set edit mode to false
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
            disabled={isDisabled}
            color='primary'
            value={'edit-mode'}
            selected={isEditMode}
            size='small'
            sx={{ border: 'none', borderRadius: '50%' }}
            onChange={() => setEditMode((mode) => !mode)}
          >
            <EditIcon />
          </ToggleButton>
        </Box>
      </Box>

      {isEditMode ? (
        <EditProjectInfoForm project={project} action={'edit-project'} />
      ) : (
        <ProjectInfoCard project={project} />
      )}
    </Paper>
  )
}

export const AddNewProjectButton = () => {
  const [on, toggle] = useState(false)
  const [wasSubmitting, toggleWasSubmitting] = useState(false)
  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'

  if (!wasSubmitting && navigation.state === 'submitting') {
    toggleWasSubmitting(true)
  }

  if (wasSubmitting && navigation.state === 'idle') {
    toggleWasSubmitting(false)
    toggle(false)
  }

  return (
    <Box py={2}>
      <Box display={'flex'} justifyContent={'center'}>
        <Tooltip title='Create new project'>
          <ToggleButton
            size='small'
            selected={on}
            disabled={isDisabled}
            color='primary'
            value={'check'}
            sx={{ border: 'none', borderRadius: '50%' }}
            onChange={() => toggle((prev) => !prev)}
          >
            <AddIcon />
          </ToggleButton>
        </Tooltip>
      </Box>

      {on && (
        <Box p={3} display={'flex'} flexDirection={'column'} rowGap={1}>
          <EditProjectInfoForm
            project={{ name: '', description: '' }}
            action='create-new-project'
          />
        </Box>
      )}
    </Box>
  )
}
