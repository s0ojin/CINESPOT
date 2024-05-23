export const getStarStatus = (rating, index) => {
  if (index <= rating) {
    return 'pi pi-star-fill'
  } else if (index - rating === 0.5) {
    return 'half'
  } else {
    return 'pi pi-star'
  }
}
