import { useEffect, useState } from 'react'
import {
  ActionFunctionArgs,
  Form,
  Link as RouterLink,
  useLoaderData,
  useNavigation,
  useSubmit
} from 'react-router-dom'
import {
  Box,
  Button,
  Fade,
  Grid,
  IconButton,
  Link,
  Paper,
  TextField,
  Typography
} from '@material-ui/core'
import Edit from '@material-ui/icons/Edit'
import { useHover } from '../hooks/useHover'
import { ProjectInfo } from '../lib/api/Api'
import { api } from '../api/RemoteApi'
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
    resolver: zodResolver(editProjectInfoSchema)
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
        {/* hidden input here for projectId */}
        <input {...register('id')} hidden defaultValue={project.id} />
        {/* name */}
        <TextField
          {...register('name')}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          InputProps={{
            style: { color: 'red', fontSize: '20px', fontWeight: '500' }
          }}
          defaultValue={project.name}
          disabled={disabled}
        ></TextField>
        {/* description */}
        <TextField
          {...register('description')}
          error={Boolean(errors.description)}
          helperText={errors.description?.message}
          disabled={disabled}
          fullWidth
          multiline
          defaultValue={project.description}
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

const Project = ({ project }: projectProps) => {
  const { hovered, hoverEventHandlers } = useHover()
  const [isEditMode, setEditMode] = useState(false)

  const navigation = useNavigation()
  const isDisabled = navigation.state !== 'idle'

  // project has changed -> set edit mode to false
  useEffect(() => setEditMode(false), [project])

  return (
    <Paper
      elevation={3}
      {...hoverEventHandlers}
      style={{
        margin: '5px',
        padding: '15px',
        position: 'relative'
      }}
    >
      <Fade in={hovered}>
        <IconButton
          disabled={isDisabled}
          style={{ position: 'absolute', top: '3px', right: '3px' }}
          onClick={() => setEditMode((mode) => !mode)}
        >
          <Edit />
        </IconButton>
      </Fade>

      {isEditMode ? (
        <EditProjectInfoForm project={project} disabled={isDisabled} />
      ) : (
        <ProjectInfoCard project={project} />
      )}
    </Paper>
  )
}

export const action = async ({ request }: ActionFunctionArgs) => {
  // for safety
  if (request.headers.get('Content-type') !== 'application/json') {
    throw new Response('Unsupported Media Type', { status: 415 })
  }

  const json = await request.json()
  return api.editProjectInfo(json)
}

export const loader = async () => api.getProjects()

export const ProjectList = () => {
  // take projects from loader above
  const projects = useLoaderData() as ProjectInfo[]

  return (
    <>
      <Typography align="center" variant="h5">
        Project List
      </Typography>
      <Box m="auto" mt={2} maxWidth={600}>
        <Grid container direction="column" justifyContent="center" alignItems="stretch">
          {projects.map((project) => (
            <Box key={project.id}>
              <Project project={project} />
            </Box>
          ))}
        </Grid>
      </Box>
    </>
  )
}
