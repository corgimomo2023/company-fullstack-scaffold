import { apiRequest } from '../../lib/api'
import type { CreateProjectInput, Project, ProjectList } from './types'
export const listProjects = () => apiRequest<ProjectList>('/projects')
export const createProject = (input: CreateProjectInput) => apiRequest<Project>('/projects', {method:'POST',body:JSON.stringify(input)})
