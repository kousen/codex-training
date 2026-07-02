import { describe, expect, it } from 'vitest'

import { checkUsernameAvailability } from './usernameService'

describe('checkUsernameAvailability', () => {
  it('reports reserved usernames as unavailable', async () => {
    await expect(checkUsernameAvailability('admin')).resolves.toEqual({
      available: false,
    })
  })

  it('reports non-reserved usernames as available', async () => {
    await expect(checkUsernameAvailability('morgan_lee')).resolves.toEqual({
      available: true,
    })
  })

  it('supports aborting an in-flight username check', async () => {
    const abortController = new AbortController()
    const result = checkUsernameAvailability(
      'morgan_lee',
      abortController.signal,
    )

    abortController.abort()

    await expect(result).rejects.toThrow('Username check aborted')
  })
})
