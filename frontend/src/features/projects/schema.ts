import { z } from 'zod'
export const createProjectSchema = z.object({
  name: z.string().trim().min(2, 'Name must be at least 2 characters').max(120),
  description: z.string().trim().max(2000).optional(),
})
export type ProjectFormValues = z.infer<typeof createProjectSchema>
