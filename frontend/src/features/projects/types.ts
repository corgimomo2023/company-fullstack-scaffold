export interface Project { id:number; name:string; description:string|null; status:'active'|'archived'; version:number; created_at:string; updated_at:string }
export interface ProjectList { items:Project[]; total:number; limit:number; offset:number }
export interface CreateProjectInput { name:string; description?:string|undefined }
