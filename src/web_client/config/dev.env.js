var merge = require('webpack-merge')
var prodEnv = require('./prod.env')
const { spawnSync } = require('child_process')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"http://localhost:3003/"',
  GIT_LATEST_MASTER_COMMIT: spawnSync('git', ['rev-parse', 'origin/master'])
})
