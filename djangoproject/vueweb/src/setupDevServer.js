// src/setupDevServer.js
const { createProxyMiddleware } = require('http-proxy-middleware');
const mocks = require('./mock/user'); // 引入 user.js 文件

module.exports = function(app) {
  // 应用 Mock 规则
  mocks.forEach(({ url, method, response }) => {
    app[method](url, (req, res) => {
      res.json(response(req));
    });
  });
};