import { useEffect, useState } from 'react'

import { Form, Link as RouterLink, useNavigation, useSubmit } from 'react-router-dom'

import { Box, Button, Fade, IconButton, Link, Paper, TextField, Typography } from '@mui/material'

import EditIcon from '@mui/icons-material/Edit'

import { useHover } from '@uidotdev/usehooks'

import { ProjectInfo } from '~/api'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

// validation here
const editProjectInfoSchema = z.object({
  id: z.string(),
  name: z.string().min(3),
  description: z.string()
})

const EditProjectInfoForm = ({
  project,
  disabled
}: {
  project: ProjectInfo
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
      name: project.name,
      description: project.description,
      id: project.id
    }
  })

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
            {
              ...project,
              name,
              description
            },
            { method: 'put', replace: true, encType: 'application/json' }
          )
        )}
        style={{ opacity: disabled ? 0.5 : 1 }}
      >
        {/* hidden input here for project id */}
        <input {...register('id')} hidden />
        {/* name */}
        <TextField
          {...register('name')}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          InputProps={{
            style: { color: 'red', fontSize: '20px', fontWeight: '500' }
          }}
          disabled={disabled}
          variant="standard"
        ></TextField>
        {/* description */}
        <TextField
          {...register('description')}
          error={Boolean(errors.description)}
          helperText={errors.description?.message}
          disabled={disabled}
          fullWidth
          // this `multiline` below causes Material-UI: Too many re-renders
          // multiline
          variant="standard"
        ></TextField>
        {/* Submit button */}
        <Box sx={{ display: 'flex', justifyContent: 'right' }}>
          <Button
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
}

export const ProjectCard = ({ project }: projectProps) => {
  const [ref, hovering] = useHover()
  const [isEditMode, setEditMode] = useState(false)

  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'

  // project has changed -> set edit mode to false
  useEffect(() => setEditMode(false), [project])

  return (
    <Box ref={ref}>
      <Fade in={hovering}>
        <IconButton
          disabled={isDisabled}
          style={{ position: 'absolute', top: '3px', right: '3px' }}
          onClick={() => setEditMode((mode) => !mode)}
        >
          <EditIcon />
        </IconButton>
      </Fade>

      {isEditMode ? (
        <EditProjectInfoForm project={project} disabled={isDisabled} />
      ) : (
        <ProjectInfoCard project={project} />
      )}
    </Box>
  )
}
