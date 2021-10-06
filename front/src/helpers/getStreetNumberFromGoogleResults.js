export default function getStreetNumberFromGoogleResults(addressResult, placeResult) {
  let streetNumber = addressResult.street_number

  if (!streetNumber) {
    const formattedAddress = placeResult.formatted_address
    const firstNumberPosition = formattedAddress.search(/\d/)
    const firstCommaPosition = formattedAddress.indexOf(',')

    if (firstNumberPosition && firstNumberPosition < firstCommaPosition) {
      return formattedAddress.substring(firstNumberPosition, firstCommaPosition)
    } else {
      return ''
    }
  } else {
    return streetNumber
  }
}
