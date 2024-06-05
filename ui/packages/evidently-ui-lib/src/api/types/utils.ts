export type ID = { id: string }
export type StrictID<T> = Omit<T, 'id'> & ID

// This version supports for NaN, -Infinity and Infinity.
export type JSONStrExtended = string

export type ErrorResponse = { status_code: number; detail: string }

export type ErrorData = { error: ErrorResponse }

export type CreateCRUD<Entity extends { id?: string | null | undefined }> = {
  // loaders
  list(): Promise<StrictID<Entity>[]>
  get(args: ID): Promise<StrictID<Entity>>

  // actions
  delete(id: ID): Promise<ErrorData | null>
  update({ body }: { body: StrictID<Entity> }): Promise<StrictID<Entity> | ErrorData | null>
  create({ body }: { body: Entity }): Promise<StrictID<Entity> | ErrorData | null>
}
