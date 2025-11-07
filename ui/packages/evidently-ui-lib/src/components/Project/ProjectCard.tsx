import { zodResolver } from '@hookform/resolvers/zod'
import { Add as AddIcon } from '@mui/icons-material'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'
import {
  Box,
  Button,
  Collapse,
  IconButton,
  Paper,
  TextField,
  ToggleButton,
  Tooltip,
  Typography
} from '@mui/material'
import type React from 'react'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Form } from 'react-router-dom'
import { z } from 'zod'
import type { ProjectModel } from '~/api/types'
import type { StrictID } from '~/api/types/utils'

// validation here
const editProjectInfoSchema = z.object({
  name: z.string().min(3),
  description: z.string()
})

export const EditProjectInfoForm = ({
  defaultValues,
  onSuccess,
  disabled
}: {
  defaultValues: z.infer<typeof editProjectInfoSchema>
  onSuccess: (v: z.infer<typeof editProjectInfoSchema>) => void
  disabled?: boolean
}) => {
  const {
    setFocus,
    register,
    handleSubmit,
    formState: { errors, dirtyFields }
  } = useForm<z.infer<typeof editProjectInfoSchema>>({
    resolver: zodResolver(editProjectInfoSchema),
    defaultValues: defaultValues
  })

  // focus on the firs input
  useEffect(() => setFocus('name'), [setFocus])

  return (
    <>
      <Form onSubmit={handleSubmit(onSuccess)} style={{ opacity: disabled ? 0.5 : 1 }}>
        {/* name */}
        <TextField
          {...register('name')}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          placeholder='Name'
          disabled={disabled}
          slotProps={{ input: { sx: { fontSize: '1.25rem', fontWeight: '500' } } }}
          variant='standard'
        />
        {/* description */}
        <TextField
          {...register('description')}
          error={Boolean(errors.description)}
          helperText={errors.description?.message}
          placeholder='Description'
          disabled={disabled}
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
              disabled ||
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

export const ProjectInfoCard = ({
  project,
  LinkToProject
}: {
  project: StrictID<ProjectModel>
  LinkToProject: (props: { name: string; projectId: string }) => JSX.Element
}) => {
  return (
    <>
      <LinkToProject projectId={project.id} name={project.name} />
      <Typography style={{ whiteSpace: 'pre-line' }} variant='body1'>
        {project.description}
      </Typography>
    </>
  )
}

interface ProjectProps {
  project: StrictID<ProjectModel>
  mode: 'edit' | 'view'
  onAlterMode: () => void
  onDeleteProject: (id: string) => void
  onEditProject: (args: { name: string; description: string }) => void
  disabled?: boolean
  LinkToProject: (props: { name: string; projectId: string }) => JSX.Element
}

export const ProjectCard: React.FC<ProjectProps> = ({
  project,
  mode,
  disabled,
  onAlterMode,
  onDeleteProject,
  onEditProject,
  LinkToProject
}) => {
  return (
    <Paper
      sx={{
        m: 1,
        p: 2,
        border: '1px solid',
        borderColor: 'divider',
        position: 'relative',
        '&:hover .action-buttons': {
          opacity: 1
        }
      }}
    >
      <Box style={{ position: 'absolute', top: '5px', right: '5px' }}>
        <Box
          sx={(theme) => ({
            opacity: 0,
            transition: theme.transitions.create('opacity', {
              duration: theme.transitions.duration.enteringScreen
            })
          })}
          className={'action-buttons'}
          display={'flex'}
          columnGap={1}
        >
          <IconButton
            disabled={disabled || mode === 'edit'}
            onClick={() => {
              if (confirm('Are you sure you want to delete this project?') === true) {
                onDeleteProject(project.id)
              }
            }}
          >
            <DeleteIcon />
          </IconButton>

          <ToggleButton
            disabled={disabled}
            color='primary'
            value={'edit-mode'}
            selected={mode === 'edit'}
            size='small'
            sx={{ border: 'none', borderRadius: '50%' }}
            onChange={onAlterMode}
          >
            <EditIcon data-testid='EditIcon' />
          </ToggleButton>
        </Box>
      </Box>
      {mode === 'edit' ? (
        <EditProjectInfoForm
          defaultValues={{ name: project.name ?? '', description: project.description ?? '' }}
          onSuccess={onEditProject}
          disabled={disabled}
        />
      ) : (
        <ProjectInfoCard project={project} LinkToProject={LinkToProject} />
      )}
    </Paper>
  )
}

type AddNewProjectButtonProps = {
  opened: boolean
  alterOpened: () => void
  disabled?: boolean
  onEditProject: (args: { name: string; description: string }) => void
}

export const AddNewProjectButton = ({
  opened,
  alterOpened,
  disabled,
  onEditProject
}: AddNewProjectButtonProps) => {
  return (
    <Box py={2}>
      <Box display={'flex'} justifyContent={'center'}>
        <Tooltip title='Create new project'>
          <ToggleButton
            size='small'
            selected={opened}
            disabled={disabled}
            color='primary'
            value={'check'}
            sx={{ border: 'none', borderRadius: '50%' }}
            onChange={alterOpened}
          >
            <AddIcon />
          </ToggleButton>
        </Tooltip>
      </Box>

      <Collapse in={opened} unmountOnExit>
        <Box p={3} display={'flex'} flexDirection={'column'} rowGap={1}>
          <EditProjectInfoForm
            disabled={disabled}
            defaultValues={{ name: '', description: '' }}
            onSuccess={onEditProject}
          />
        </Box>
      </Collapse>
    </Box>
  )
}
