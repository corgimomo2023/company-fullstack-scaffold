import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Button } from '../../components/Button'
import { Field } from '../../components/Field'
import { createProjectSchema, type ProjectFormValues } from './schema'

interface Props { onSubmit:(values:ProjectFormValues)=>Promise<void>; busy:boolean; serverError:string|null }
export function CreateProjectForm({onSubmit,busy,serverError}:Props) {
 const {register,handleSubmit,formState:{errors},reset}=useForm<ProjectFormValues>({resolver:zodResolver(createProjectSchema),defaultValues:{name:'',description:''}})
 const submit=handleSubmit(async values=>{await onSubmit(values);reset()})
 return <form className="project-form" onSubmit={event=>void submit(event)} noValidate>
  <h2>Create a project</h2><p className="muted">This feature is a reference vertical slice. Replace its domain, not its engineering boundaries.</p>
  <Field name="name" label="Project name" error={errors.name?.message} inputProps={{...register('name'),autoComplete:'off'}}/>
  <Field multiline name="description" label="Description" error={errors.description?.message} inputProps={{...register('description'),rows:4}}/>
  {serverError&&<div className="error-banner" role="alert">{serverError}</div>}
  <Button type="submit" pending={busy} pendingLabel="Creating project">Create project</Button>
 </form>
}
