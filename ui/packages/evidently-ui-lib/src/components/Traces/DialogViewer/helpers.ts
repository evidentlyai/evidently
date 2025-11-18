export function SplitField(field: string): [string, string] {
  const split = field.split(':', 2)
  if (split.length > 1) {
    return [split[0], split[1]]
  }
  return ['', field]
}
