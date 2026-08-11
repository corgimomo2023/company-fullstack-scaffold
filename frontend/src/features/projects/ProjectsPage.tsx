import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ApiError } from '../../lib/api'
import { createProject, listProjects } from './api'
import { CreateProjectForm } from './CreateProjectForm'
import type { ProjectFormValues } from './schema'

const projectKeys={all:['projects'] as const}
export function ProjectsPage(){
 const client=useQueryClient()
 const projects=useQuery({queryKey:projectKeys.all,queryFn:listProjects})
 const create=useMutation({mutationFn:createProject,onSuccess:async()=>{await client.invalidateQueries({queryKey:projectKeys.all})}})
 const submit=async(values:ProjectFormValues)=>{await create.mutateAsync(values)}
 const error=create.error instanceof ApiError?`${create.error.message}. Request ID: ${create.error.requestId??'unavailable'}`:create.error?'Could not create project':null
 return <div className="content-grid"><section aria-labelledby="projects-heading"><div className="section-heading"><div><p className="eyebrow">Reference feature</p><h1 id="projects-heading">Projects</h1></div>{projects.data&&<span className="count">{projects.data.total} total</span>}</div>
  {projects.isPending&&<p role="status">Loading projects...</p>}
  {projects.isError&&<div className="error-banner" role="alert">Projects could not be loaded. <button onClick={()=>void projects.refetch()}>Retry</button></div>}
  {projects.data?.items.length===0&&<div className="empty"><h2>No projects yet</h2><p>Create the first project using the form.</p></div>}
  <ul className="project-list">{projects.data?.items.map(project=><li key={project.id} className="project-card"><div><h2>{project.name}</h2><p>{project.description||'No description'}</p></div><span className={`status status-${project.status}`}>{project.status}</span></li>)}</ul>
 </section><aside><CreateProjectForm onSubmit={submit} busy={create.isPending} serverError={error}/></aside></div>
}
