const { defineConfig } = require('@vue/cli-service');
const path = require('path');

module.exports = defineConfig({
  assetsDir: 'static',
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src') // 设置 @ 别名指向 src 目录
      }
    }
  },
});