const unavailableUsernames = new Set([
  'admin',
  'codex',
  'root',
  'support',
  'test_user',
])

export type UsernameAvailabilityResult = {
  available: boolean
}

export async function checkUsernameAvailability(
  username: string,
  signal?: AbortSignal,
): Promise<UsernameAvailabilityResult> {
  await new Promise<void>((resolve, reject) => {
    const timeoutId = window.setTimeout(resolve, 650)

    signal?.addEventListener(
      'abort',
      () => {
        window.clearTimeout(timeoutId)
        reject(new DOMException('Username check aborted', 'AbortError'))
      },
      { once: true },
    )
  })

  return {
    available: !unavailableUsernames.has(username.toLowerCase()),
  }
}
