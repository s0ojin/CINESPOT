// utils/countryUtils.js
import countries from 'i18n-iso-countries'
import koLocale from 'i18n-iso-countries/langs/ko.json'

countries.registerLocale(koLocale)

export const getCountryNameInKorean = (countryCode) => {
  return countries.getName(countryCode, 'ko') || countryCode
}
