const { defineConfig } = require('@vue/cli-service')
const static_dir = '../static/poems/'
const template_path = '../../templates/poems/index.html'

module.exports = defineConfig({
  transpileDependencies: true,
  // outputDir: process.env.NODE_ENV === 'production' ? static_dir : 'dist/', 
  // indexPath: process.env.NODE_ENV === 'production' ? template_path : 'index.html',
  // assetsDir: '',
  // publicPath: process.env.NODE_ENV === 'production' ? '/static/poems/' : '/'
  // publicPath: process.env.NODE_ENV === 'production' ? '/poems/' : '/'
  // outputDir: process.env.NODE_ENV === 'production' ? 'dist/poems' : 'dist/',
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/'
})
