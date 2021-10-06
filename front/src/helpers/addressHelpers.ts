import { AddressSuggestion } from '~/service/api'

export function getOptionString(suggestion?: AddressSuggestion) {
  if (!suggestion) return ''

  let optionString = suggestion.street || ''
  if (suggestion.number) optionString += ` ${suggestion.number}`
  if (suggestion.city) optionString += `, ${suggestion.city}`
  if (suggestion.post_code) optionString += ` ${suggestion.post_code}`
  return optionString
}
