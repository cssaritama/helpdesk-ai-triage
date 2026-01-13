/* This file is generated via `npm run gen:api` from ../docs/api/openapi.yaml.
 * A minimal placeholder is committed to keep the repo runnable before generation.
 */

export type paths = {
  '/health': {
    get: {
      responses: { 200: { content: { 'application/json': { status: string } } } }
    }
  },
  '/tickets': {
    get: { responses: { 200: { content: { 'application/json': { items: any[] } } } } },
    post: { responses: { 200: { content: { 'application/json': any } } } }
  },
  '/kb/articles': {
    get: { responses: { 200: { content: { 'application/json': any[] } } } },
    post: { responses: { 200: { content: { 'application/json': any } } } }
  }
}
