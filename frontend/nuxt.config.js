module.exports = {
  // SSR IS DISABLED!
  // Due to issue: https://github.com/nuxt-community/auth-module/issues/478
  ssr: false,
  /*
  ** Headers of the page
  */
  head: {
    title: 'FLRChain',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Nuxt.js project' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://use.typekit.net/gdw2tmn.css'}
    ]
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend(config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  },
  buildModules: [
    '@nuxtjs/vuetify',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/moment',
  ],
  plugins: [
    { src: '@/plugins/vue-timers', mode: 'client' },
    { src: '@/plugins/v-mask', mode: 'client'}
  ],
  publicRuntimeConfig: {
    axios: {
      baseURL: process.env.BASE_URL + 'api/v1/'
    },
    baseUrl: process.env.BASE_URL
  },
  router: {
    middleware: ['auth']
  },
  auth: {
    cookie: false,
    strategies: {
      local: {
        token: {
          property: 'token',
          type: 'Token',
          name: 'Authorization',
          global: true
        },
        refreshToken: {
          required: false,
          maxAge: false
        },
        user: {
          property: false
        },
        endpoints: {
          login: {
            url: 'login/',
            method: 'post',
          },
          logout: false,
          user: {
            url: 'info/',
            method: 'get',
          }
        },
      }
    }
  },
  vuetify: {
    treeShake: true,
    customVariables: ['@/assets/variables.scss'],
    theme: {
      options: { customProperties: true },
      dark: false,
      themes: {
        light: {
          primary: '#06BCC1',
          secondary: '#23BC3D',
          tertiary: '#F7F9FB',
          quaternary: "#778699",
          quinary: "#414D55",
          senary: "#71809C",
          septenary: "#FFC423",
          octonary: "#253f50",
          nonary: "#72809D",
          accent: '#FAFAFD',
          error: '#C50505',
          info: '#2196F3',
          success: '#25B81F',
          warning: '#FFC107',
        }
      }
    }
  },
}

