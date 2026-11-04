import type { CodegenConfig } from '@graphql-codegen/cli'

// The backend must be running. One output per service: services reuse type names.
const base = 'http://127.0.0.1:8060/telecom-tmf-bss'

const service = (path: string) => ({
  schema: `${base}/${path}/graphql`,
  documents: `src/api/${path}/**/*.graphql`,
  preset: 'client' as const,
  presetConfig: { fragmentMasking: false },
  // useTypeImports: the Vite TypeScript template enables verbatimModuleSyntax.
  config: { useTypeImports: true, scalars: { DateTime: 'string', Decimal: 'string' } },
})

const config: CodegenConfig = {
  generates: {
    'src/api/generated/product-catalog/': service('product-catalog'),
    'src/api/generated/resource/': service('resource'),
    'src/api/generated/shopping-cart/': service('shopping-cart'),
  },
}

export default config
