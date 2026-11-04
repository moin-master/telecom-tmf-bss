import { ClientError } from 'graphql-request'

export type ApiError = {
  code: string
  status: number | null
  message: string
}

// The backend puts the TM Forum error fields in `extensions`.
export function apiError(error: unknown): ApiError {
  if (error instanceof ClientError) {
    const first = error.response.errors?.[0]
    const extensions = (first?.extensions ?? {}) as { code?: string; status?: number }
    return {
      code: extensions.code ?? 'Error',
      status: extensions.status ?? error.response.status ?? null,
      message: first?.message ?? error.message,
    }
  }
  if (error instanceof Error) {
    return { code: 'Network', status: null, message: error.message }
  }
  return { code: 'Error', status: null, message: 'Something went wrong' }
}
