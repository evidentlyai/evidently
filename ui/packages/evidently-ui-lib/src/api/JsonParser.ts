// Adapted from Crockford's JSON.parse (see https://github.com/douglascrockford/JSON-js)
// This version adds support for NaN, -Infinity and Infinity.

export class JsonParser {
  at = 0
  ch = ''
  text = ''
  escapee = {
    '"': '"',
    '\\': '\\',
    '/': '/',
    b: '\b',
    f: '\f',
    n: '\n',
    r: '\r',
    t: '\t'
  }

  constructor() {}

  error(message: string) {
    throw {
      name: 'SyntaxError',
      message: message,
      at: this.at,
      text: this.text
    }
  }

  next(): string {
    return (this.ch = this.text.charAt(this.at++))
  }

  check(character: string) {
    if (character !== this.ch) {
      this.error(`Expected '${character}' instead of '${this.ch}'`)
    }
    this.ch = this.text.charAt(this.at++)
  }

  number() {
    var string = ''
    if (this.ch === '-') {
      string = '-'
      this.check('-')
    }
    if (this.ch === 'I') {
      this.check('I')
      this.check('n')
      this.check('f')
      this.check('i')
      this.check('n')
      this.check('i')
      this.check('t')
      this.check('y')
      return Number.NEGATIVE_INFINITY
    }
    while (this.ch >= '0' && this.ch <= '9') {
      string += this.ch
      this.next()
    }
    if (this.ch === '.') {
      string += '.'
      while (this.next() && this.ch >= '0' && this.ch <= '9') {
        string += this.ch
      }
    }
    if (this.ch === 'e' || this.ch === 'E') {
      string += this.ch
      this.next()
      // @ts-ignore
      if (this.ch === '-' || this.ch === '+') {
        string += this.ch
        this.next()
      }
      while (this.ch >= '0' && this.ch <= '9') {
        string += this.ch
        this.next()
      }
    }
    return +string
  }

  string() {
    var hex,
      i,
      string = '',
      uffff
    if (this.ch === '"') {
      while (this.next()) {
        if (this.ch === '"') {
          this.next()
          return string
        }
        if (this.ch === '\\') {
          this.next()
          if (this.ch === 'u') {
            uffff = 0
            for (i = 0; i < 4; i++) {
              hex = Number.parseInt(this.next(), 16)
              if (!isFinite(hex)) {
                break
              }
              uffff = uffff * 16 + hex
            }
            string += String.fromCharCode(uffff)
          } else if (this.escapee[this.ch]) {
            string += this.escapee[this.ch]
          } else {
            break
          }
        } else {
          string += this.ch
        }
      }
    }
    this.error('Bad string')
  }

  white() {
    // Skip whitespace.
    while (this.ch && this.ch <= ' ') {
      this.next()
    }
  }

  word() {
    switch (this.ch) {
      case 't':
        this.check('t')
        this.check('r')
        this.check('u')
        this.check('e')
        return true
      case 'f':
        this.check('f')
        this.check('a')
        this.check('l')
        this.check('s')
        this.check('e')
        return false
      case 'n':
        this.check('n')
        this.check('u')
        this.check('l')
        this.check('l')
        return null
      case 'N':
        this.check('N')
        this.check('a')
        this.check('N')
        return Number.NaN
      case 'I':
        this.check('I')
        this.check('n')
        this.check('f')
        this.check('i')
        this.check('n')
        this.check('i')
        this.check('t')
        this.check('y')
        return Number.POSITIVE_INFINITY
    }
    this.error("Unexpected '" + this.ch + "'")
  }

  // @ts-ignore
  array() {
    // @ts-ignore
    var array = []
    if (this.ch === '[') {
      this.check('[')
      this.white()
      // @ts-ignore
      if (this.ch === ']') {
        this.check(']')
        // @ts-ignore
        return array // empty array
      }
      while (this.ch) {
        array.push(this.value())
        this.white()
        // @ts-ignore
        if (this.ch === ']') {
          this.check(']')
          return array
        }
        this.check(',')
        this.white()
      }
    }
    this.error('Bad array')
  }

  object() {
    var key,
      object = {}
    if (this.ch === '{') {
      this.check('{')
      this.white()
      // @ts-ignore
      if (this.ch === '}') {
        this.check('}')
        return object // empty object
      }
      while (this.ch) {
        key = this.string()
        this.white()
        this.check(':')
        // @ts-ignore
        if (Object.hasOwnProperty.call(object, key)) {
          this.error('Duplicate key "' + key + '"')
        }
        // @ts-ignore
        object[key] = this.value()
        this.white()
        // @ts-ignore
        if (this.ch === '}') {
          this.check('}')
          return object
        }
        this.check(',')
        this.white()
      }
    }
    this.error('Bad object')
  }

  // @ts-ignore
  value() {
    this.white()
    switch (this.ch) {
      case '{':
        return this.object()
      case '[':
        return this.array()
      case '"':
        return this.string()
      case '-':
        return this.number()
      default:
        return this.ch >= '0' && this.ch <= '9' ? this.number() : this.word()
    }
  }

  parse(source: string, reviver?: (this: any, key: string, value: any) => any) {
    let result
    this.text = source
    this.at = 0
    this.ch = ' '
    result = this.value()
    this.white()
    if (this.ch) {
      this.error('Syntax error')
    }
    return reviver !== undefined
      ? (function walk(holder, key) {
          var k,
            v,
            // @ts-ignore
            value = holder[key]
          if (value && typeof value === 'object') {
            for (k in value) {
              if (Object.prototype.hasOwnProperty.call(value, k)) {
                v = walk(value, k)
                if (v !== undefined) {
                  value[k] = v
                } else {
                  delete value[k]
                }
              }
            }
          }
          return reviver.call(holder, key, value)
        })({ '': result }, '')
      : result
  }
}

export const JSONParseExtended = <T extends Object>(str: string) => new JsonParser().parse(str) as T
