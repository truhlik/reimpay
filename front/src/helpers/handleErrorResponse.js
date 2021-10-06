export default function handleErrorResponse(response) {

  if (response.status === 401) {
    window.location.href = '/app/#/auth/login/'
  }

  if (response.status === 409 && response.data.message) {
    return {message: `Confict: ${response.data.message}`, errorObject: {}}
  }

  if (response.status === 403) {
    return {message: response.data.message || 'You are not allowed to perform this action', errorObject: {}}
  }

  if (response.status !== 400 || !response.data) {
    return {message: 'Server error', errorObject: {}}
  }

  let message = ''
  for (let key in response.data) {
    message += `${key}: ${response.data[key][0]}\n`
  }

  return {
    message: response.data.non_field_errors || message || 'Invalid request',
    errorObject: response.data
  }
}
