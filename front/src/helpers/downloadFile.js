import FileSaver from 'file-saver'

export default async function downloadFile(axios, toast, link, fileName='download') {
  try {
    const response = await axios.get(link, { responseType: 'blob' })
    FileSaver.saveAs(response.data, fileName)
  } catch (e) {
    toast.error(e.message || 'Cannot download the file')
    // toast(e.message || $t('errors.cannotDownloadFile'))
  }
}
