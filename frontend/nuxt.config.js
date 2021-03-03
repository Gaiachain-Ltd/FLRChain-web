module.exports = {
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
    // Simple usage
    '@nuxtjs/vuetify',
    '@nuxtjs/axios',
    '@nuxtjs/auth',
  ],
  axios: {
    baseURL: process.env.BASE_URL
  },
  router: {
    middleware: ['auth']
  },
  auth: {
    strategies: {
      local: {
        autoFetch: false,
        endpoints: {
          login: {
            url: '/api/v1/login/',
            method: 'post',
            property: 'token'
          },
          user: {
            url: '/api/v1/info/',
            method: 'get',
            property: false,
          }
        },
        tokenType: 'Token',
        tokenName: 'Authorization',
      },
      redirect: {
        login: '/login',
        home: '/',
      },
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
          primary: '#23BC3D',
          secondary: '#06BCC1',
          tertiary: '#F7F9FB',
          quaternary: "#778699",
          accent: '#FAFAFD',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        }
      }
    }
  }
}

