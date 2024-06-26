export function formatDate(date: any): string {
  if (typeof date !== typeof new Date()) {
    console.log(`not a date ${typeof date}: ${date}`)
    return date
  }
  return (
    `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}` +
    `-${date.getDate().toString().padStart(2, '0')}` +
    `T${date.getHours().toString().padStart(2, '0')}:${date
      .getMinutes()
      .toString()
      .padStart(2, '0')}`
  )
}
