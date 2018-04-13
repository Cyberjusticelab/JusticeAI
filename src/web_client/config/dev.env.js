var merge = require('webpack-merge')
var prodEnv = require('./prod.env')
var spawnSync = require('child_process').spawnSync

var gitMasterSHA = spawnSync('git', ['rev-parse', 'origin/master'], {encoding: 'utf-8'}).stdout.trim()
module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"http://localhost:3003/"',
  GIT_LATEST_MASTER_COMMIT: '"' + gitMasterSHA + '"'
})
