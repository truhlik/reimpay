export default function updateObjectTitle(obj, langCode, value) {
    if(!obj || !obj.title || !langCode || !value) return;

    if(obj.title.filter(title => title.lang === langCode).length) {
      obj.title = obj.title.map(title => {

        if(title.lang === langCode) {
          title = {lang: title.lang, value: value};
        }

        return title
      });
    } else {
      obj.title.push({lang: langCode, value: value})
    }

    return obj;
}
