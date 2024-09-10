export function formatDate(date: Date): string {
  return (
    `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}` +
    `-${date.getDate().toString().padStart(2, '0')}` +
    `T${date.getHours().toString().padStart(2, '0')}:${date
      .getMinutes()
      .toString()
      .padStart(2, '0')}`
  )
}
