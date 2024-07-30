export type ID = { id: string }
export type OptionalID = { id?: string | null | undefined }
export type StrictID<T extends OptionalID> = Omit<T, 'id'> & ID

// This version supports for NaN, -Infinity and Infinity.
export type JSONStrExtended = string

export type ErrorResponse = { status_code: number | false; detail: string }

export type ErrorData = { error: ErrorResponse }

///////////////////////////////
// TYPES TEST
// see details here:
// https://frontendmasters.com/blog/testing-types-in-typescript/
///////////////////////////////

export type Expect<T extends true> = T
type ShapesMatch<T, U> = [T] extends [U] ? true : false

export type TYPE_SATISFIED<T, U> = ShapesMatch<T, U> extends true
  ? ShapesMatch<keyof T, keyof U> extends true
    ? true
    : false
  : false
